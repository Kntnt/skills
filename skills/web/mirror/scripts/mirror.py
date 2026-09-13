# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx==0.28.1",
#     "selectolax==0.4.11",
#     "tinycss2==1.5.1",
# ]
# ///
"""Copy a web page and everything it needs to display to disk, browsable offline.

The engine owns the three things a mirror is made of — fetching, the mapping
from a URL to a file, and the rewriting of references — because a fetcher added
later produces pages no external tool has seen, and a rewrite needs the mapping
to be its own (ADR-0196). Fetching sits behind the `Fetcher` protocol, so a
second fetcher is added beside `HttpFetcher` rather than threaded through it.

A run has three passes. The fetch pass follows the start page's redirects and
fetches, one request at a time, every resource the page and its stylesheets
reference that `--resources` admits. The placement pass maps every fetched URL
to a path, keeps HTML and CSS as served under `.mirror/raw/`, and puts every
other file straight into the tree. The rewrite pass derives the tree's HTML and
CSS from the raw copies, so a later run can rewrite again without fetching.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import shutil
import sys
import tempfile
import time
from collections import deque
from collections.abc import Callable, Iterable, Iterator
from contextlib import nullcontext
from dataclasses import dataclass, field
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from pathlib import Path, PurePosixPath
from typing import Protocol
from urllib.parse import quote, unquote_to_bytes, urljoin, urlsplit, urlunsplit

import httpx
import tinycss2
import tinycss2.ast
import tinycss2.bytes
from selectolax.lexbor import LexborHTMLParser, LexborNode
from tinycss2.serializer import serialize_string_value, serialize_url

# The identity every request carries unless `--user-agent` replaces it.
IDENTITY = "kntnt-mirror (+https://github.com/Kntnt/skills)"
FETCHER_NAME = "http"

# Connection handling: timeouts in seconds, and what is retried after which wait.
CONNECT_TIMEOUT = 30.0
READ_TIMEOUT = 30.0
RETRIED_STATUSES = frozenset({429, 500, 502, 503, 504})
RETRY_WAITS = (1.0, 2.0, 4.0)

# What normalisation removes from a URL before it is compared.
DEFAULT_PORTS = {"http": 80, "https": 443}
INDEX_NAMES = ("index.html", "index.php")
TRACKING_PREFIX = "utm_"
TRACKING_PARAMETERS = frozenset({"fbclid", "gclid", "mc_cid", "mc_eid"})
UNRESERVED = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)
PATH_SAFE = "/!$&'()*+,;=:@"
QUERY_SAFE = "/?!$&'()*+,;=:@"
HEX_PAIR = re.compile(r"[0-9A-Fa-f]{2}")

# The characters a file name cannot hold on macOS or Linux, percent-encoded.
FORBIDDEN_IN_NAMES = frozenset('/\x00?#%\\:*"<>|')
DIRECTORY_INDEX = "index.html"
HTML_SUFFIX = ".html"
FILE_SUFFIX = "~file"

# The vocabularies the manifest and the flags use.
RESOURCE_POLICIES = ("all", "in-scope", "none")
KIND_PAGE = "page"
KIND_RESOURCE = "resource"
SOURCE_START = "start"
SOURCE_RESOURCE = "resource"
OUTCOME_FETCHED = "fetched"
OUTCOME_OUT_OF_SCOPE = "out-of-scope"
OUTCOME_FAILED = "failed"

# Exit statuses.
EXIT_CLEAN = 0
EXIT_FAILED = 1
EXIT_REFUSED = 2

# Content types the rewrite reads.
HTML_TYPES = frozenset({"text/html", "application/xhtml+xml"})
CSS_TYPE = "text/css"

# Where the run keeps what is not part of the browsable tree.
STATE_DIRECTORY = ".mirror"
RAW_DIRECTORY = "raw"
MANIFEST_NAME = "manifest.ndjson"
LOG_NAME = "run.log"

# Attributes whose value is one URL, and those that hold a candidate list.
URL_ATTRIBUTES = ("href", "src", "poster", "data", "action")
SRCSET_ATTRIBUTES = ("srcset", "imagesrcset")

# Which of those references name something the page needs to display.
RESOURCE_SOURCES = frozenset(
    {
        ("img", "src"),
        ("script", "src"),
        ("iframe", "src"),
        ("frame", "src"),
        ("embed", "src"),
        ("video", "src"),
        ("video", "poster"),
        ("audio", "src"),
        ("source", "src"),
        ("track", "src"),
        ("input", "src"),
        ("object", "data"),
    }
)
RESOURCE_LINK_RELATIONS = frozenset(
    {
        "stylesheet",
        "icon",
        "apple-touch-icon",
        "apple-touch-icon-precomposed",
        "mask-icon",
        "preload",
        "modulepreload",
        "manifest",
    }
)

# CSS functions whose string arguments are URLs.
CSS_IMAGE_SETS = frozenset({"image-set", "-webkit-image-set"})

HERE = Path(__file__).resolve().parent.parent


# --- URLs -----------------------------------------------------------------------


def normalise(url: str) -> str | None:
    """Return *url* in the one form it is compared, deduplicated and fetched in.

    Scheme and host go to lower case; credentials, fragment and default port
    go; percent-encoding is made canonical before dot segments are resolved,
    so `%2E%2E` is resolved too; `index.html` and `index.php` become their
    directory; the tracking parameters go and every other parameter stays in
    its order. A URL that is not `http` or `https` has no such form: None.
    """

    # Refuse what cannot be fetched over HTTP.
    parts = urlsplit(url.strip())
    scheme = parts.scheme.lower()
    if scheme not in DEFAULT_PORTS or not parts.hostname:
        return None
    try:
        port = parts.port
    except ValueError:
        return None

    # The authority: lower-case host, no credentials, no default port.
    host = parts.hostname.lower()
    if ":" in host:
        host = f"[{host}]"
    netloc = host if port in (None, DEFAULT_PORTS[scheme]) else f"{host}:{port}"

    # The path: canonical escapes, no dot segments, no index file name.
    path = _remove_dot_segments(_canonical_escapes(parts.path or "/", PATH_SAFE))
    for index in INDEX_NAMES:
        if path.endswith(f"/{index}"):
            path = path[: -len(index)]

    # The query: tracking parameters removed, the rest kept in order.
    kept = [
        _canonical_escapes(pair, QUERY_SAFE)
        for pair in parts.query.split("&")
        if pair and not _is_tracking(pair)
    ]

    return urlunsplit((scheme, netloc, path, "&".join(kept), ""))


def _is_tracking(pair: str) -> bool:
    name = pair.partition("=")[0].lower()
    return name.startswith(TRACKING_PREFIX) or name in TRACKING_PARAMETERS


def _canonical_escapes(text: str, safe: str) -> str:
    """Decode escaped unreserved characters, upper-case the rest, escape the unsafe."""

    out: list[str] = []
    index = 0
    while index < len(text):
        character = text[index]
        pair = text[index + 1 : index + 3]
        if character == "%" and HEX_PAIR.fullmatch(pair):
            decoded = chr(int(pair, 16))
            out.append(decoded if decoded in UNRESERVED else f"%{pair.upper()}")
            index += 3
            continue
        out.append(quote(character, safe=safe))
        index += 1
    return "".join(out)


def _remove_dot_segments(path: str) -> str:
    """Resolve `.` and `..` segments as RFC 3986 section 5.2.4 does."""

    output: list[str] = []
    for segment in path.split("/")[1:]:
        if segment == "..":
            if output:
                output.pop()
        elif segment != ".":
            output.append(segment)
    resolved = "/" + "/".join(output)
    if path.rsplit("/", 1)[-1] in (".", "..") and not resolved.endswith("/"):
        resolved += "/"
    return resolved


@dataclass(frozen=True)
class Scope:
    """What belongs to the site under the start page's directory.

    The scope predicate is written once, here. This engine applies it to
    resources under `--resources=in-scope`; a later fetch of pages applies the
    same predicate to them.
    """

    start: str
    scheme_hosts: frozenset[str]
    port: int | None
    prefix: str

    @classmethod
    def of(cls, start: str) -> Scope:
        """The scope rooted at the normalised start page *start*."""

        # The root prefix is the start page's directory.
        parts = urlsplit(start)
        prefix = parts.path[: parts.path.rfind("/") + 1]

        # The host with and without `www.` is one site.
        host = parts.hostname or ""
        bare = host.removeprefix("www.")
        return cls(start, frozenset({bare, f"www.{bare}"}), parts.port, prefix)

    def admits(self, url: str) -> bool:
        """Whether the normalised *url* is in scope."""

        if url == self.start:
            return True
        parts = urlsplit(url)
        return (
            parts.scheme in DEFAULT_PORTS
            and (parts.hostname or "") in self.scheme_hosts
            and parts.port == self.port
            and parts.path.startswith(self.prefix)
        )


# --- The tree -----------------------------------------------------------------


def escape_name(text: str) -> str:
    """Percent-encode every character a file name cannot hold."""

    return "".join(
        f"%{ord(character):02X}"
        if character in FORBIDDEN_IN_NAMES
        or ord(character) < 0x20
        or ord(character) == 0x7F
        else character
        for character in text
    )


def _decoded(text: str) -> str:
    """Decode percent-escapes where they spell UTF-8, and keep them otherwise."""

    try:
        return unquote_to_bytes(text).decode("utf-8")
    except UnicodeDecodeError:
        return text


def natural_path(url: str, is_html: bool) -> PurePosixPath:
    """The path a normalised *url* maps to, before collisions are settled.

    One directory per host, the port kept where it is not the default, and
    under it the path as on the site. A directory URL is `index.html`; an HTML
    page with no extension gets `.html`; a query string stays in the name,
    before the extension, so the file keeps its type.
    """

    # The host directory and the directories on the way to the file.
    parts = urlsplit(url)
    segments = parts.path.split("/")[1:]
    directories = [escape_name(_decoded(segment)) for segment in segments[:-1]]

    # The name, with its extension and query string placed.
    name = _decoded(segments[-1]) if segments and segments[-1] else DIRECTORY_INDEX
    if is_html and not PurePosixPath(name).suffix:
        name += HTML_SUFFIX
    suffix = PurePosixPath(name).suffix
    stem = name[: len(name) - len(suffix)]
    query = f"?{_decoded(parts.query)}" if parts.query else ""
    file_name = escape_name(stem) + escape_name(query) + escape_name(suffix)

    return PurePosixPath(escape_name(parts.netloc), *directories, file_name)


def assign_paths(files: dict[str, bool]) -> dict[str, PurePosixPath]:
    """Map every normalised final URL to its path, collisions settled.

    *files* says of each URL whether it is HTML. Where a file's natural path is
    a directory another file needs, the file moves inside it as `index.html`
    when it is HTML and that name is free, and takes `~file` otherwise.
    """

    natural = {url: natural_path(url, is_html) for url, is_html in files.items()}
    taken = set(natural.values())
    directories = {parent for path in taken for parent in path.parents}

    assigned: dict[str, PurePosixPath] = {}
    for url, path in natural.items():
        if path not in directories:
            assigned[url] = path
        elif files[url] and path / DIRECTORY_INDEX not in taken:
            assigned[url] = path / DIRECTORY_INDEX
        else:
            assigned[url] = path.with_name(path.name + FILE_SUFFIX)
    return assigned


# --- Fetching -----------------------------------------------------------------


@dataclass
class Fetched:
    """What one fetch of a URL came back with, redirects followed."""

    final_url: str
    status: int | None = None
    content_type: str | None = None
    charset: str | None = None
    etag: str | None = None
    last_modified: str | None = None
    size: int | None = None
    sha256: str | None = None
    body: bytes | None = None
    staged: Path | None = None
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return (
            self.error is None and self.status is not None and 200 <= self.status < 300
        )


class Fetcher(Protocol):
    """Fetches one URL. The engine names the fetcher in every manifest row."""

    name: str

    def fetch(self, url: str, staging: Path | None) -> Fetched:
        """Fetch *url*, following redirects.

        The body of an HTML or CSS answer is returned in `body`. Any other body
        is written to *staging* and named in `staged`, or only counted when
        *staging* is None.
        """
        ...


class RunLog:
    """The lines `run.log` receives, kept until the run writes them."""

    def __init__(self) -> None:
        self.lines: list[str] = []

    def request(self, method: str, url: str, status: str, elapsed: float) -> None:
        self.lines.append(
            f"{timestamp()} {method} {url} {status} {elapsed * 1000:.0f}ms"
        )

    def decision(self, outcome: str, url: str, detail: str = "") -> None:
        self.lines.append(
            f"{timestamp()} {outcome} {url}{f' {detail}' if detail else ''}"
        )


class HttpFetcher:
    """Plain HTTP, one request at a time, retrying what a moment may fix."""

    name = FETCHER_NAME

    def __init__(
        self,
        headers: list[tuple[str, str]],
        user_agent: str,
        credentials: tuple[str, str, str] | None,
        log: RunLog,
    ) -> None:
        self.credentials = credentials
        self.log = log
        self.started: dict[int, float] = {}
        self.client = httpx.Client(
            headers=[("User-Agent", user_agent), *headers],
            timeout=httpx.Timeout(READ_TIMEOUT, connect=CONNECT_TIMEOUT),
            follow_redirects=True,
            event_hooks={"request": [self._sent], "response": [self._answered]},
        )

    def _sent(self, request: httpx.Request) -> None:
        self.started[id(request)] = time.monotonic()

    def _answered(self, response: httpx.Response) -> None:
        began = self.started.pop(id(response.request), time.monotonic())
        self.log.request(
            response.request.method,
            str(response.request.url),
            str(response.status_code),
            time.monotonic() - began,
        )

    def fetch(self, url: str, staging: Path | None) -> Fetched:
        """Fetch *url*, retrying connection errors, timeouts and busy answers."""

        attempts = len(RETRY_WAITS) + 1
        for attempt in range(attempts):
            last = attempt == attempts - 1
            began = time.monotonic()
            try:
                with self.client.stream("GET", url, auth=self._auth(url)) as response:
                    if response.status_code in RETRIED_STATUSES and not last:
                        wait = retry_after(response.headers.get("Retry-After"))
                        time.sleep(RETRY_WAITS[attempt] if wait is None else wait)
                        continue
                    return self._receive(response, staging)
            except (httpx.TimeoutException, httpx.NetworkError) as error:
                self.log.request("GET", url, "error", time.monotonic() - began)
                if last:
                    return Fetched(url, error=f"{type(error).__name__}: {error}")
                time.sleep(RETRY_WAITS[attempt])
            except httpx.HTTPError as error:
                # Too many redirects, a protocol violation, an unusable URL:
                # nothing a retry can change.
                return Fetched(url, error=f"{type(error).__name__}: {error}")
        raise AssertionError("the last attempt always returns")

    def _auth(self, url: str) -> httpx.BasicAuth | None:
        """Basic auth from the start URL, for the start page's host only."""

        if self.credentials is None or urlsplit(url).hostname != self.credentials[0]:
            return None
        return httpx.BasicAuth(self.credentials[1], self.credentials[2])

    def _receive(self, response: httpx.Response, staging: Path | None) -> Fetched:
        """Read one final answer: keep HTML and CSS, stage or count the rest."""

        # What the headers say.
        media_type, _, parameters = response.headers.get("Content-Type", "").partition(
            ";"
        )
        content_type = media_type.strip().lower() or None
        charset_match = re.search(r"charset=\"?([^\";\s]+)", parameters, re.IGNORECASE)
        fetched = Fetched(
            final_url=str(response.url),
            status=response.status_code,
            content_type=content_type,
            charset=charset_match.group(1) if charset_match else None,
            etag=response.headers.get("ETag"),
            last_modified=response.headers.get("Last-Modified"),
        )
        if not fetched.succeeded:
            return fetched

        # The body: kept where the rewrite reads it, staged or counted otherwise.
        digest = hashlib.sha256()
        size = 0
        kept = bytearray() if is_rewritable(content_type, fetched.final_url) else None
        staged = staging if staging and kept is None else None
        with open(staged, "wb") if staged else nullcontext() as sink:
            for chunk in response.iter_bytes():
                digest.update(chunk)
                size += len(chunk)
                if kept is not None:
                    kept.extend(chunk)
                elif sink is not None:
                    sink.write(chunk)

        fetched.size = size
        fetched.sha256 = digest.hexdigest()
        fetched.body = bytes(kept) if kept is not None else None
        fetched.staged = staged
        return fetched


def retry_after(value: str | None) -> float | None:
    """The wait a `Retry-After` header asks for, in seconds, or None."""

    if value is None:
        return None
    if value.strip().isdigit():
        return float(value.strip())
    try:
        moment = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    return max(0.0, (moment - datetime.now(UTC)).total_seconds())


def is_html(content_type: str | None, url: str) -> bool:
    if content_type:
        return content_type in HTML_TYPES
    return urlsplit(url).path.lower().endswith((".html", ".htm"))


def is_css(content_type: str | None, url: str) -> bool:
    if content_type:
        return content_type == CSS_TYPE
    return urlsplit(url).path.lower().endswith(".css")


def is_rewritable(content_type: str | None, url: str) -> bool:
    return is_html(content_type, url) or is_css(content_type, url)


def timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


# --- References -----------------------------------------------------------------

# A reference rewriter: given the absolute URL a reference resolves to, the
# value to write in its place, or None to leave the reference as written.
Replace = Callable[[str], str | None]


def css_tokens(text: str) -> list[tinycss2.ast.Node]:
    return tinycss2.parse_component_value_list(text)


def _css_url_tokens(
    tokens: Iterable[tinycss2.ast.Node],
) -> Iterator[tinycss2.ast.URLToken | tinycss2.ast.StringToken]:
    """Every token in a CSS component list that holds a URL, at any depth."""

    expecting_import = False
    for token in tokens:
        if isinstance(token, tinycss2.ast.AtKeywordToken):
            expecting_import = token.lower_value == "import"
            continue
        if isinstance(token, tinycss2.ast.WhitespaceToken | tinycss2.ast.Comment):
            continue
        if isinstance(token, tinycss2.ast.URLToken) or (
            isinstance(token, tinycss2.ast.StringToken) and expecting_import
        ):
            yield token
        elif isinstance(token, tinycss2.ast.FunctionBlock):
            if token.lower_name == "url" or token.lower_name in CSS_IMAGE_SETS:
                yield from (
                    argument
                    for argument in token.arguments
                    if isinstance(argument, tinycss2.ast.StringToken)
                )
            yield from _css_url_tokens(token.arguments)
        elif isinstance(
            token,
            tinycss2.ast.CurlyBracketsBlock
            | tinycss2.ast.ParenthesesBlock
            | tinycss2.ast.SquareBracketsBlock,
        ):
            yield from _css_url_tokens(token.content)
        expecting_import = False


def css_references(text: str, base: str) -> list[str]:
    """The absolute URLs a stylesheet's `url()` and `@import` name."""

    return [
        urljoin(base, token.value.strip())
        for token in _css_url_tokens(css_tokens(text))
    ]


def rewrite_css(text: str, base: str, replace: Replace) -> str | None:
    """*text* with every URL it names replaced, or None where nothing changed."""

    tokens = css_tokens(text)
    changed = False
    for token in _css_url_tokens(tokens):
        written = token.value.strip()
        if not written or written.startswith(("data:", "#")):
            continue
        replacement = replace(urljoin(base, written))
        if replacement is None or replacement == token.value:
            continue
        token.value = replacement
        token.representation = (
            f"url({serialize_url(replacement)})"
            if isinstance(token, tinycss2.ast.URLToken)
            else f'"{serialize_string_value(replacement)}"'
        )
        changed = True
    return tinycss2.serialize(tokens) if changed else None


def parse_srcset(value: str) -> list[tuple[str, str]]:
    """Split a `srcset` into its candidates: each URL and its descriptors."""

    candidates: list[tuple[str, str]] = []
    position = 0
    while position < len(value):
        # Skip the separators before the next URL.
        while position < len(value) and (
            value[position].isspace() or value[position] == ","
        ):
            position += 1
        start = position
        while position < len(value) and not value[position].isspace():
            position += 1
        url = value[start:position]
        if not url:
            break

        # A URL that ends in a comma has no descriptors.
        if url.endswith(","):
            candidates.append((url.rstrip(","), ""))
            continue
        start = position
        depth = 0
        while position < len(value) and (value[position] != "," or depth):
            depth += {"(": 1, ")": -1}.get(value[position], 0)
            position += 1
        candidates.append((url, value[start:position].strip()))
    return candidates


def document_base(tree: LexborHTMLParser, url: str) -> str:
    """The URL a page's relative references resolve against."""

    base = tree.css_first("base[href]")
    href = base.attributes.get("href") if base is not None else None
    return urljoin(url, href.strip()) if href else url


def is_resource_reference(node: LexborNode, attribute: str) -> bool:
    """Whether a reference names something the page needs to display."""

    tag = node.tag or ""
    if attribute in SRCSET_ATTRIBUTES:
        return True
    if (tag, attribute) in RESOURCE_SOURCES:
        return True
    if tag == "link" and attribute == "href":
        relations = set((node.attributes.get("rel") or "").lower().split())
        return bool(relations & RESOURCE_LINK_RELATIONS)
    return False


def html_references(tree: LexborHTMLParser, url: str) -> list[str]:
    """The absolute URLs of every resource a page needs to display."""

    base = document_base(tree, url)
    found: list[str] = []
    for node in tree.css("*"):
        attributes = node.attributes
        for attribute in URL_ATTRIBUTES:
            value = attributes.get(attribute)
            if value and is_resource_reference(node, attribute):
                found.append(urljoin(base, value.strip()))
        for attribute in SRCSET_ATTRIBUTES:
            value = attributes.get(attribute)
            if value:
                found.extend(
                    urljoin(base, candidate) for candidate, _ in parse_srcset(value)
                )
        style = attributes.get("style")
        if style:
            found.extend(css_references(style, base))
        if node.tag == "style":
            found.extend(css_references(node.text(deep=True), base))
    return found


def decode_html(body: bytes, charset: str | None) -> str:
    """Decode a page as a browser would: BOM, then header, then meta, then UTF-8."""

    for bom, encoding in (
        (b"\xef\xbb\xbf", "utf-8-sig"),
        (b"\xff\xfe", "utf-16"),
        (b"\xfe\xff", "utf-16"),
    ):
        if body.startswith(bom):
            return body.decode(encoding, errors="replace")
    declared = re.search(
        rb"<meta[^>]+charset=[\"']?\s*([A-Za-z0-9_.:-]+)", body[:4096], re.IGNORECASE
    )
    for candidate in (charset, declared.group(1).decode("ascii") if declared else None):
        if candidate:
            try:
                return body.decode(candidate, errors="replace")
            except LookupError:
                continue
    return body.decode("utf-8", errors="replace")


def rewrite_html(
    text: str, url: str, replace: Replace, changed_targets: Callable[[str], bool]
) -> str:
    """The page with its references rewritten, `base` gone, and UTF-8 declared.

    *changed_targets* says of an absolute URL whether the mirror changed the
    bytes of the file it names; an `integrity` attribute guarding such a file
    no longer holds and is removed.
    """

    tree = LexborHTMLParser(text)
    base = document_base(tree, url)

    def rewritten(value: str) -> str:
        written = value.strip()
        if not written or (written.startswith("#") and base == url):
            return value
        return replace(urljoin(base, written)) or value

    for node in tree.css("*"):
        attributes = node.attributes

        # Integrity no longer holds where the guarded bytes changed.
        guarded = attributes.get("src") or attributes.get("href")
        if (
            "integrity" in attributes
            and guarded
            and changed_targets(urljoin(base, guarded.strip()))
        ):
            del node.attrs["integrity"]

        # Single URLs, candidate lists, and inline CSS.
        for attribute in URL_ATTRIBUTES:
            value = attributes.get(attribute)
            if value:
                node.attrs[attribute] = rewritten(value)
        for attribute in SRCSET_ATTRIBUTES:
            value = attributes.get(attribute)
            if value:
                node.attrs[attribute] = ", ".join(
                    f"{rewritten(candidate)} {descriptors}".strip()
                    for candidate, descriptors in parse_srcset(value)
                )
        style = attributes.get("style")
        if style:
            node.attrs["style"] = rewrite_css(style, base, replace) or style
        if node.tag == "style":
            css = rewrite_css(node.text(deep=True), base, replace)
            if css is not None:
                node.inner_html = css

    # The base is honoured above, and removed now.
    for node in tree.css("base"):
        node.decompose()

    declare_utf8(tree)
    return tree.html or ""


def declare_utf8(tree: LexborHTMLParser) -> None:
    """Declare the encoding the saved page is written in."""

    declared = False
    for node in tree.css("meta[charset]"):
        node.attrs["charset"] = "utf-8"
        declared = True
    for node in tree.css("meta[http-equiv]"):
        if (node.attributes.get("http-equiv") or "").lower() == "content-type":
            node.attrs["content"] = "text/html; charset=utf-8"
            declared = True
    head = tree.head
    if declared or head is None:
        return
    meta = LexborHTMLParser('<meta charset="utf-8">').css_first("meta")
    assert meta is not None
    if head.child is None:
        head.insert_child(meta)
    else:
        head.child.insert_before(meta)


# --- The run ------------------------------------------------------------------


@dataclass
class Record:
    """One URL the run took a position on, and what came of it."""

    url: str
    kind: str
    source: str
    discovered_from: str | None
    outcome: str = OUTCOME_FETCHED
    fetched: Fetched | None = None
    timestamp: str = field(default_factory=timestamp)
    local_path: PurePosixPath | None = None

    @property
    def final(self) -> str | None:
        """The normalised URL this record's bytes live at."""

        if self.fetched is None or not self.fetched.succeeded:
            return None
        return normalise(self.fetched.final_url)

    def row(self, fetcher: str) -> dict[str, object]:
        """The manifest row: every field on every row, null where nothing is known."""

        fetched = self.fetched
        attempted = fetched is not None
        return {
            "url": self.url,
            "final_url": normalise(fetched.final_url) if fetched else None,
            "kind": self.kind,
            "source": self.source,
            "discovered_from": self.discovered_from,
            "fetcher": fetcher if attempted else None,
            "status": fetched.status if fetched else None,
            "content_type": fetched.content_type if fetched else None,
            "size": fetched.size if fetched else None,
            "local_path": str(self.local_path) if self.local_path else None,
            "sha256": fetched.sha256 if fetched else None,
            "etag": fetched.etag if fetched else None,
            "last_modified": fetched.last_modified if fetched else None,
            "timestamp": self.timestamp,
            "outcome": self.outcome,
        }


@dataclass
class Options:
    """The invocation, its values already refused where the Skill rejects them."""

    url: str
    output: Path | None
    resources: str
    headers: list[tuple[str, str]]
    user_agent: str
    dry_run: bool
    credentials: tuple[str, str, str] | None


class Mirror:
    """One run: fetch, place, rewrite, and account for it."""

    def __init__(self, options: Options, fetcher: Fetcher, log: RunLog) -> None:
        self.options = options
        self.fetcher = fetcher
        self.log = log
        self.records: dict[str, Record] = {}
        self.queue: deque[Record] = deque()
        self.fetches = 0
        self.by_final: dict[str, Record] = {}
        self.scope: Scope | None = None
        self.start = normalise(options.url) or options.url
        self.output = options.output or Path(".")

    def run(self, staging: Path | None) -> int:
        """Mirror the start page; return the exit status."""

        # The start page, where its redirects end, is the root of the scope.
        start_url = self.start
        start = Record(start_url, KIND_PAGE, SOURCE_START, None)
        self.records[start_url] = start
        self._fetch(start, staging)
        if start.final is None:
            assert start.fetched is not None
            why = start.fetched.error or f"the server answered {start.fetched.status}"
            print(
                f"Could not fetch the start page {start_url}: {why}. Nothing was written."
            )
            return EXIT_FAILED
        self.scope = Scope.of(start.final)
        self.output = self.options.output or Path(urlsplit(start.final).hostname or "")
        self._discover(start)

        # Every resource the fetched documents need, breadth first.
        while self.queue:
            record = self.queue.popleft()
            self._fetch(record, staging)
            self._discover(record)

        if not self.options.dry_run:
            self._write()
        print(self._report())
        failed = any(
            record.outcome == OUTCOME_FAILED for record in self.records.values()
        )
        return EXIT_FAILED if failed else EXIT_CLEAN

    def _fetch(self, record: Record, staging: Path | None) -> None:
        self.fetches += 1
        place = staging / str(self.fetches) if staging else None
        record.fetched = self.fetcher.fetch(record.url, place)
        record.timestamp = timestamp()
        if record.final is None:
            record.outcome = OUTCOME_FAILED
            detail = record.fetched.error or str(record.fetched.status)
            self.log.decision(OUTCOME_FAILED, record.url, detail)

    def _discover(self, record: Record) -> None:
        """Take a position on every resource a fetched document references."""

        fetched = record.fetched
        if fetched is None or fetched.body is None:
            return
        if is_html(fetched.content_type, fetched.final_url):
            tree = LexborHTMLParser(decode_html(fetched.body, fetched.charset))
            found = html_references(tree, fetched.final_url)
        else:
            text, _ = decode_css(fetched.body, fetched.charset)
            found = css_references(text, fetched.final_url)

        for reference in found:
            url = normalise(reference)
            if url is None or url in self.records:
                continue
            resource = Record(url, KIND_RESOURCE, SOURCE_RESOURCE, record.url)
            self.records[url] = resource
            if self._admits(url):
                self.queue.append(resource)
            else:
                resource.outcome = OUTCOME_OUT_OF_SCOPE
                self.log.decision(OUTCOME_OUT_OF_SCOPE, url)

    def _admits(self, url: str) -> bool:
        policy = self.options.resources
        if policy == "all":
            return True
        return (
            policy == "in-scope" and self.scope is not None and self.scope.admits(url)
        )

    # --- Placement and rewriting ----------------------------------------------

    def _fetched(self) -> list[Record]:
        return [record for record in self.records.values() if record.final is not None]

    def _write(self) -> None:
        """Place every fetched file, rewrite from the raw copies, write the state."""

        output = self.output
        state = output / STATE_DIRECTORY
        raw = state / RAW_DIRECTORY

        # One path per final URL, and one file there, however many URLs led to it.
        by_final: dict[str, Record] = {}
        for record in self._fetched():
            by_final.setdefault(record.final or "", record)
        paths = assign_paths(
            {
                final: is_html(record.fetched.content_type, final)
                for final, record in by_final.items()
                if record.fetched is not None
            }
        )
        for record in self._fetched():
            record.local_path = paths[record.final or ""]
        self.by_final = by_final

        # HTML and CSS go to raw as served; everything else straight to the tree.
        for final, record in by_final.items():
            fetched = record.fetched
            assert fetched is not None
            if fetched.body is not None:
                write_bytes(raw / str(paths[final]), fetched.body)
            elif fetched.staged is not None:
                target = output / str(paths[final])
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(fetched.staged, target)

        # The rewrite pass derives the tree's HTML and CSS from raw, CSS first
        # so each page knows which stylesheets' bytes changed.
        rewritable = [
            (final, record)
            for final, record in by_final.items()
            if record.fetched and record.fetched.body is not None
        ]
        changed: set[str] = set()
        for final, record in rewritable:
            fetched = record.fetched
            assert fetched is not None
            if is_html(fetched.content_type, final):
                continue
            served = (raw / str(paths[final])).read_bytes()
            text, codec = decode_css(served, fetched.charset)
            css = rewrite_css(text, fetched.final_url, self._replacer(paths[final]))
            write_bytes(
                output / str(paths[final]),
                served if css is None else css.encode(codec, errors="replace"),
            )
            if css is not None:
                changed.add(final)
        for final, record in rewritable:
            fetched = record.fetched
            assert fetched is not None
            if not is_html(fetched.content_type, final):
                continue
            served = (raw / str(paths[final])).read_bytes()
            page = rewrite_html(
                decode_html(served, fetched.charset),
                fetched.final_url,
                self._replacer(paths[final]),
                lambda url: (
                    (target := self._located(url)) is not None
                    and target.final in changed
                ),
            )
            write_bytes(output / str(paths[final]), page.encode("utf-8"))

        # The manifest and the log.
        rows = "".join(
            json.dumps(record.row(self.fetcher.name), ensure_ascii=False) + "\n"
            for record in self.records.values()
        )
        write_bytes(state / MANIFEST_NAME, rows.encode("utf-8"))
        write_bytes(
            state / LOG_NAME,
            "".join(f"{line}\n" for line in self.log.lines).encode("utf-8"),
        )

    def _located(self, url: str) -> Record | None:
        """The fetched record an absolute URL leads to, by its own URL or where it ended."""

        normalised = normalise(url)
        if normalised is None:
            return None
        record = self.records.get(normalised) or self.by_final.get(normalised)
        return record if record is not None and record.final is not None else None

    def _replacer(self, document: PurePosixPath) -> Replace:
        """Rewrite a reference from *document*: relative in the mirror, absolute outside."""

        def replace(url: str) -> str | None:
            if normalise(url) is None:
                return None
            record = self._located(url)
            if record is None or record.local_path is None:
                return url
            relative = posixpath.relpath(str(record.local_path), str(document.parent))
            fragment = urlsplit(url).fragment
            return quote(relative, safe="/!$&'()*+,;=@~") + (
                f"#{fragment}" if fragment else ""
            )

        return replace

    # --- The report -------------------------------------------------------------

    def _report(self) -> str:
        """What the Skill relays: counts, size, and every failure."""

        fetched = [
            record for record in self.records.values() if record.final is not None
        ]
        pages = sum(1 for record in fetched if record.kind == KIND_PAGE)
        resources = sum(1 for record in fetched if record.kind == KIND_RESOURCE)
        size = sum((record.fetched.size or 0) for record in fetched if record.fetched)
        failures = [
            record
            for record in self.records.values()
            if record.outcome == OUTCOME_FAILED
        ]

        lines: list[str] = []
        if self.options.dry_run:
            lines.append(f"Dry run of {self.start}: nothing was written. Would fetch:")
            lines.extend(
                f"  {record.url}"
                for record in self.records.values()
                if record.fetched is not None
            )
        else:
            lines.append(f"Mirrored {self.start} to {self.output}.")
        lines.append(f"Pages fetched: {pages}")
        lines.append(f"Resources fetched: {resources}")
        lines.append(f"Total size: {human_size(size)}")
        if failures:
            lines.append(f"Failures: {len(failures)}")
            for record in failures:
                assert record.fetched is not None
                status = record.fetched.status or f"no answer ({record.fetched.error})"
                lines.append(f"  {status} {record.url}")
        return "\n".join(lines)


def decode_css(body: bytes, charset: str | None) -> tuple[str, str]:
    """Decode a stylesheet as CSS Syntax says: BOM, header, `@charset`, UTF-8.

    Returns the text and the codec it was decoded with, which a rewritten
    stylesheet is encoded back into so that its `@charset` stays true.
    """

    text, encoding = tinycss2.bytes.decode_stylesheet_bytes(
        body, protocol_encoding=charset
    )
    return text, encoding.codec_info.name


def write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def human_size(size: int) -> str:
    """A byte count as a person reads it."""

    amount = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if amount < 1000 or unit == "GB":
            return f"{size} B" if unit == "B" else f"{amount:.1f} {unit}"
        amount /= 1000
    raise AssertionError("the last unit always returns")


# --- The command line -----------------------------------------------------------


def refusal(problem: str) -> int:
    """Refuse a value in the collection's shape: the problem, the SYNOPSIS, the route."""

    page = (HERE / "help.md").read_text(encoding="utf-8")
    synopsis = page.partition("\n## SYNOPSIS\n")[2].partition("\n## ")[0].strip()
    print(f"{problem}\n\n{synopsis}\n\nsee '/mirror --help'")
    return EXIT_REFUSED


def main(argv: list[str] | None = None) -> int:
    """Read the invocation, refuse what the Skill rejects, and run the mirror."""

    # The grammar is the invocation engine's; this reads what it let through.
    parser = argparse.ArgumentParser(prog="mirror.py")
    parser.add_argument("--output")
    parser.add_argument("--resources", default="all")
    parser.add_argument("--header", action="append", default=[])
    parser.add_argument("--user-agent", default=IDENTITY)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("url")
    arguments = parser.parse_args(argv)

    # A value whose form the page admits and whose meaning the Skill rejects.
    parts = urlsplit(arguments.url)
    if parts.scheme.lower() not in DEFAULT_PORTS or not parts.hostname:
        return refusal(f"'{arguments.url}' is not an absolute http or https URL")
    if arguments.resources not in RESOURCE_POLICIES:
        return refusal(
            f"'--resources' takes all, in-scope or none, not '{arguments.resources}'"
        )
    headers: list[tuple[str, str]] = []
    for header in arguments.header:
        name, colon, value = header.partition(":")
        if not colon or not name.strip():
            return refusal(f"'--header={header}' is not written 'name: value'")
        headers.append((name.strip(), value.strip()))

    # Credentials in the URL are sent to the start page's host.
    credentials = (
        (parts.hostname.lower(), parts.username or "", parts.password or "")
        if parts.username
        else None
    )
    options = Options(
        url=arguments.url,
        output=Path(arguments.output) if arguments.output else None,
        resources=arguments.resources,
        headers=headers,
        user_agent=arguments.user_agent,
        dry_run=arguments.dry_run,
        credentials=credentials,
    )

    # Run; a real run stages the files it downloads outside the output directory.
    log = RunLog()
    fetcher = HttpFetcher(headers, options.user_agent, credentials, log)
    run = Mirror(options, fetcher, log)
    if options.dry_run:
        return run.run(None)
    with tempfile.TemporaryDirectory(prefix="kntnt-mirror-") as staging:
        return run.run(Path(staging))


if __name__ == "__main__":
    sys.exit(main())
