# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx==0.28.1",
#     "regex==2026.9.10",
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
crawls from there, one request at a time and breadth first: every page and file
in scope that a link, a sitemap or a feed names, as far as `robots.txt`
and the page cap allow, and every resource those pages and their stylesheets
reference that `--resources` admits; sitemaps and feeds are read, never saved.
The placement pass maps every fetched URL to a path, keeps HTML and CSS as
served under `.mirror/raw/`, and puts every other file straight into the tree. The rewrite pass derives the tree's HTML and CSS from the raw
copies, so a later run can rewrite again without fetching.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import posixpath
import re
import shutil
import sys
import tempfile
import time
import zlib
from collections import deque
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass, field
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from pathlib import Path, PurePosixPath
from typing import Protocol
from urllib.parse import quote, unquote_to_bytes, urljoin, urlsplit, urlunsplit
from xml.etree import ElementTree

import httpx
import regex
import tinycss2
import tinycss2.ast
import tinycss2.bytes
from selectolax.lexbor import LexborHTMLParser, LexborNode
from tinycss2.serializer import serialize_string_value, serialize_url

# The identity every request carries unless `--user-agent` replaces it, and the
# product token `robots.txt` groups are matched against.
IDENTITY = "kntnt-mirror (+https://github.com/Kntnt/skills)"
FETCHER_NAME = "http"

# Connection handling: timeouts in seconds, and what is retried after which wait.
CONNECT_TIMEOUT = 30.0
READ_TIMEOUT = 30.0
RETRIED_STATUSES = frozenset({429, 500, 502, 503, 504})
RETRY_WAITS = (1.0, 2.0, 4.0)
REDIRECT_STATUSES = frozenset({301, 302, 303, 307, 308})
MAX_REDIRECTS = 20

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
KIND_FILE = "file"  # Linked from a page, or the start page, and no HTML itself.
KIND_ROBOTS = "robots"
KIND_SITEMAP = "sitemap"
KIND_FEED = "feed"
SOURCE_START = "start"
SOURCE_RESOURCE = "resource"
SOURCE_LINK = "link"
SOURCE_ROBOTS = "robots"
SOURCE_SITEMAP = "sitemap"
SOURCE_FEED = "feed"
SOURCE_PROBE = "probe"  # A well-known location, tried whatever names it.
OUTCOME_FETCHED = "fetched"
OUTCOME_OUT_OF_SCOPE = "out-of-scope"
OUTCOME_FAILED = "failed"
OUTCOME_REDIRECT_OUT = "redirect-out"
OUTCOME_ROBOTS = "robots"
OUTCOME_OVER_CAP = "over-cap"
OUTCOME_MISSING = "missing"
OUTCOME_EXCLUDED = "excluded"

# What names a page or file the crawl may take, and the documents read, not saved.
PAGE_SOURCES = (SOURCE_LINK, SOURCE_SITEMAP, SOURCE_FEED)
READ_KINDS = (KIND_SITEMAP, KIND_FEED)

# The crawl: its default cap on pages and files, and the pace between requests.
DEFAULT_MAX_PAGES = 5000
DEFAULT_DELAY = 0.0

# `robots.txt`: where it is, and the file it is never saved as.
ROBOTS_PATH = "/robots.txt"

# Sitemaps and feeds: the well-known locations tried every run, the answers
# that say one is not there, the media types that make an `alternate` a feed,
# and the most a compressed sitemap or feed is inflated to, the sitemap
# protocol's own limit.
SITEMAP_PATHS = ("/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml")
FEED_PATH = "feed/"
MISSING_STATUSES = frozenset({404, 410})
FEED_TYPES = frozenset({"application/rss+xml", "application/atom+xml"})
GZIP_MAGIC = b"\x1f\x8b"
INFLATED_LIMIT = 50 * 1024 * 1024

# A suspected JavaScript shell: scripts, and less text than this outside them.
SHELL_TEXT_LIMIT = 200
SHELL_HIDDEN_TAGS = ("script", "style", "noscript", "template")

# The mark a file takes when a case-folding file system already holds its name.
CASE_MARK = "~"
CASE_PROBE_PREFIX = ".mirror-case-probe-"

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

# The references a crawl follows to other pages and files.
LINK_TAGS = ("a", "area")
LINK_RELATIONS = frozenset({"next", "prev", "canonical", "alternate"})

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


def fold_host(url: str, root_host: str) -> str:
    """*url* with the other form of the root host, `www.` added or removed, folded onto it.

    Only the root host folds: `www.` on any other host is left alone.
    """

    parts = urlsplit(url)
    host = parts.hostname or ""
    if host == root_host or root_host.removeprefix("www.") != host.removeprefix("www."):
        return url
    netloc = root_host if parts.port is None else f"{root_host}:{parts.port}"
    return urlunsplit(parts._replace(netloc=netloc))


def origin(url: str) -> str:
    """The scheme and authority of a normalised *url*: where its `robots.txt` is."""

    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}"


@dataclass(frozen=True)
class Scope:
    """What belongs to the site under the start page's directory, as widened and narrowed.

    The scope predicate is written once, here. The crawl applies it to every
    candidate it finds, and `--resources=in-scope` to every resource. An
    `--include` widens the root's subtree and an `--exclude` narrows
    everything, the root and the includes alike; both are matched, unanchored,
    against the normalised URL.
    """

    start: str
    scheme_hosts: frozenset[str]
    port: int | None
    prefix: str
    includes: tuple[regex.Pattern[str], ...] = ()
    excludes: tuple[regex.Pattern[str], ...] = ()

    @classmethod
    def of(
        cls,
        start: str,
        includes: tuple[regex.Pattern[str], ...] = (),
        excludes: tuple[regex.Pattern[str], ...] = (),
    ) -> Scope:
        """The scope rooted at the normalised start page *start*."""

        # The root prefix is the start page's directory.
        parts = urlsplit(start)
        prefix = parts.path[: parts.path.rfind("/") + 1]

        # The host with and without `www.` is one site.
        host = parts.hostname or ""
        bare = host.removeprefix("www.")
        hosts = frozenset({bare, f"www.{bare}"})
        return cls(start, hosts, parts.port, prefix, includes, excludes)

    def excluded(self, url: str) -> bool:
        """Whether an `--exclude` matches the normalised *url*."""

        return matches(self.excludes, url)

    def admits(self, url: str) -> bool:
        """Whether the normalised *url* is in scope."""

        if self.excluded(url):
            return False
        if url == self.start:
            return True
        parts = urlsplit(url)
        if parts.scheme not in DEFAULT_PORTS:
            return False
        under_root = (
            (parts.hostname or "") in self.scheme_hosts
            and parts.port == self.port
            and parts.path.startswith(self.prefix)
        )
        return under_root or matches(self.includes, url)


def matches(patterns: Iterable[regex.Pattern[str]], url: str) -> bool:
    """Whether any of *patterns* matches *url* anywhere: unanchored."""

    return any(pattern.search(url) is not None for pattern in patterns)


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


def assign_paths(
    files: dict[str, bool], folds_case: bool = False
) -> dict[str, PurePosixPath]:
    """Map every normalised final URL to its path, collisions settled.

    *files* says of each URL whether it is HTML, in the order the run fetched
    them. Where a file's natural path is a directory another file needs, the
    file moves inside it as `index.html` when it is HTML and that name is free,
    and takes `~file` otherwise. Where *folds_case*, the later of two paths
    that differ only in case takes `~2`, `~3` and so on before its extension.
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
    return separate_cases(assigned) if folds_case else assigned


def separate_cases(assigned: dict[str, PurePosixPath]) -> dict[str, PurePosixPath]:
    """Give the later of two paths that differ only in case a numbered name."""

    folded = {str(path).lower() for path in assigned.values()}
    held: set[str] = set()
    separated: dict[str, PurePosixPath] = {}
    for url, path in assigned.items():
        suffix = path.suffix
        stem = path.name[: len(path.name) - len(suffix)]
        candidate = path
        number = 1
        # A numbered name is also kept clear of every path another URL has.
        while str(candidate).lower() in held or (
            candidate != path and str(candidate).lower() in folded
        ):
            number += 1
            candidate = path.with_name(f"{stem}{CASE_MARK}{number}{suffix}")
        held.add(str(candidate).lower())
        separated[url] = candidate
    return separated


def folds_case(directory: Path) -> bool:
    """Whether the file system under *directory* holds names differing in case as one."""

    directory.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix=CASE_PROBE_PREFIX, dir=directory)
    os.close(handle)
    probe = Path(name)
    try:
        return (probe.parent / probe.name.swapcase()).exists()
    finally:
        probe.unlink()


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
    redirected_out: bool = False

    @property
    def succeeded(self) -> bool:
        return (
            self.error is None and self.status is not None and 200 <= self.status < 300
        )


class Fetcher(Protocol):
    """Fetches one URL. The engine names the fetcher in every manifest row."""

    name: str

    def fetch(
        self,
        url: str,
        staging: Path | None,
        follow: Callable[[str], bool] | None = None,
        keep: bool = False,
    ) -> Fetched:
        """Fetch *url*, following redirects.

        The body of an HTML or CSS answer, or of any answer when *keep*, is
        returned in `body`. Any other body is written to *staging* and named in
        `staged`, or only counted when *staging* is None. Where *follow* says
        no to a redirect's target, the fetch stops there: `final_url` is that
        target, `status` the redirect's, and `redirected_out` is set.
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
        # The client follows no redirect itself: on each hop httpx drops
        # `Cookie` and cross-origin `Authorization`, and every header the
        # caller gave belongs on every request, so `_send` follows them.
        self.headers = [("User-Agent", user_agent), *headers]
        self.client = httpx.Client(
            timeout=httpx.Timeout(READ_TIMEOUT, connect=CONNECT_TIMEOUT),
            follow_redirects=False,
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

    def fetch(
        self,
        url: str,
        staging: Path | None,
        follow: Callable[[str], bool] | None = None,
        keep: bool = False,
    ) -> Fetched:
        """Fetch *url*, retrying connection errors, timeouts and busy answers."""

        attempts = len(RETRY_WAITS) + 1
        for attempt in range(attempts):
            last = attempt == attempts - 1
            began = time.monotonic()
            try:
                with self._send(url, follow) as (response, declined):
                    if declined is not None:
                        return Fetched(
                            declined,
                            status=response.status_code,
                            redirected_out=True,
                        )
                    if response.status_code in RETRIED_STATUSES and not last:
                        wait = retry_after(response.headers.get("Retry-After"))
                        time.sleep(RETRY_WAITS[attempt] if wait is None else wait)
                        continue
                    return self._receive(response, staging, keep)
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

    @contextmanager
    def _send(
        self, url: str, follow: Callable[[str], bool] | None
    ) -> Iterator[tuple[httpx.Response, str | None]]:
        """GET *url*, following redirects with every header on every hop.

        Yields the final answer, and the redirect target *follow* declined, if any.
        """

        for _ in range(MAX_REDIRECTS + 1):
            request = self.client.build_request("GET", url, headers=self.headers)
            response = self.client.send(request, auth=self._auth(url), stream=True)
            location = response.headers.get("Location")
            redirected = response.status_code in REDIRECT_STATUSES and location
            target = urljoin(str(response.url), location) if redirected else None
            declined = target if target and follow and not follow(target) else None
            if target is None or declined is not None:
                try:
                    yield response, declined
                finally:
                    response.close()
                return
            response.close()
            url = target
        raise httpx.TooManyRedirects(
            f"more than {MAX_REDIRECTS} redirects", request=request
        )

    def _auth(self, url: str) -> httpx.BasicAuth | None:
        """Basic auth from the start URL, for the start page's host only."""

        if self.credentials is None or urlsplit(url).hostname != self.credentials[0]:
            return None
        return httpx.BasicAuth(self.credentials[1], self.credentials[2])

    def _receive(
        self, response: httpx.Response, staging: Path | None, keep: bool
    ) -> Fetched:
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
        rewritable = is_rewritable(content_type, fetched.final_url)
        kept = bytearray() if keep or rewritable else None
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


def html_links(tree: LexborHTMLParser, url: str) -> list[str]:
    """The absolute URLs of every page and file a page links to.

    `a` and `area` with `href`, and `link` whose `rel` is `next`, `prev`,
    `canonical` or `alternate`. An `alternate` that names a feed is a feed
    and only a feed, and is left to `html_feeds`.
    """

    base = document_base(tree, url)
    found: list[str] = []
    selector = ", ".join(f"{tag}[href]" for tag in (*LINK_TAGS, "link"))
    for node in tree.css(selector):
        if node.tag == "link":
            relations = set((node.attributes.get("rel") or "").lower().split())
            if not relations & LINK_RELATIONS or is_feed_link(node):
                continue
        href = (node.attributes.get("href") or "").strip()
        if href:
            found.append(urljoin(base, href))
    return found


def is_feed_link(node: LexborNode) -> bool:
    """Whether a `link` is an `alternate` whose type is RSS or Atom."""

    relations = set((node.attributes.get("rel") or "").lower().split())
    media_type = (node.attributes.get("type") or "").partition(";")[0]
    return "alternate" in relations and media_type.strip().lower() in FEED_TYPES


def html_feeds(tree: LexborHTMLParser, url: str) -> list[str]:
    """The absolute URLs of every feed a page names through `link rel="alternate"`."""

    base = document_base(tree, url)
    return [
        urljoin(base, href)
        for node in tree.css("link[href]")
        if is_feed_link(node) and (href := (node.attributes.get("href") or "").strip())
    ]


# --- Sitemaps and feeds -----------------------------------------------------------


def xml_root(body: bytes) -> ElementTree.Element | None:
    """The root element of a sitemap or feed, inflated where it is gzip, or None.

    A document that is no XML, a soft 404 answering with a page for instance,
    names nothing rather than failing the run.
    """

    if body.startswith(GZIP_MAGIC):
        try:
            body = zlib.decompressobj(wbits=31).decompress(body, INFLATED_LIMIT)
        except zlib.error:
            return None
    try:
        return ElementTree.fromstring(body)
    except ElementTree.ParseError:
        return None


def local_name(element: ElementTree.Element) -> str:
    """An element's name without its namespace."""

    return str(element.tag).rpartition("}")[2]


def sitemap_entries(body: bytes, base: str) -> tuple[list[str], list[str]]:
    """The sitemaps an index names and the URLs a URL set names, each absolute."""

    root = xml_root(body)
    if root is None:
        return [], []
    wanted = {"sitemapindex": "sitemap", "urlset": "url"}.get(local_name(root))
    locations = [
        urljoin(base, child.text.strip())
        for entry in root
        if local_name(entry) == wanted
        for child in entry
        if local_name(child) == "loc" and child.text and child.text.strip()
    ]
    return (locations, []) if wanted == "sitemap" else ([], locations)


def feed_entries(body: bytes, base: str) -> list[str]:
    """The link of every item in an RSS feed and every entry in an Atom feed."""

    root = xml_root(body)
    if root is None:
        return []
    found: list[str] = []
    for element in root.iter():
        name = local_name(element)
        if name not in ("item", "entry"):
            continue
        for child in element:
            if local_name(child) != "link":
                continue
            text = (child.text or "").strip()
            href = (child.get("href") or "").strip()
            if name == "item" and text:
                found.append(urljoin(base, text))
            elif (
                name == "entry"
                and href
                and child.get("rel", "alternate") == "alternate"
            ):
                found.append(urljoin(base, href))
    return found


def is_suspected_shell(text: str) -> bool:
    """Whether a page carries scripts but almost no text a reader would see.

    At least one `script` element, and fewer than 200 characters of text
    outside `script`, `style`, `noscript` and `template`, whitespace collapsed.
    """

    tree = LexborHTMLParser(text)
    if tree.css_first("script") is None:
        return False
    tree.strip_tags(list(SHELL_HIDDEN_TAGS))
    root = tree.root
    visible = root.text(deep=True, separator=" ") if root is not None else ""
    return len(" ".join(visible.split())) < SHELL_TEXT_LIMIT


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


# --- robots.txt -----------------------------------------------------------------


def product_token(user_agent: str) -> str:
    """The product token of an identity: its first word, without a version."""

    words = user_agent.split()
    return words[0].partition("/")[0].lower() if words else ""


@dataclass(frozen=True)
class Robots:
    """The rules one host's `robots.txt` sets for this run's product token."""

    rules: tuple[tuple[bool, re.Pattern[str], int], ...] = ()
    crawl_delay: float | None = None
    unreadable: bool = False
    sitemaps: tuple[str, ...] = ()  # As written; they belong to no group.

    @classmethod
    def parse(cls, text: str, token: str) -> Robots:
        """Read *text* as RFC 9309 does, for the product token *token*.

        The groups whose user-agent line most specifically matches *token* are
        combined and apply; the `*` groups apply only where none matches.
        """

        # Group the records: user-agent lines open a group, rules fill it.
        groups: list[tuple[list[str], list[tuple[bool, str]], list[float]]] = []
        sitemaps: list[str] = []
        opening = False
        for raw in text.splitlines():
            line = raw.partition("#")[0].strip()
            key, colon, value = line.partition(":")
            if not colon:
                continue
            key, value = key.strip().lower(), value.strip()
            if key == "sitemap":
                if value:
                    sitemaps.append(value)
            elif key == "user-agent":
                if not opening:
                    groups.append(([], [], []))
                    opening = True
                groups[-1][0].append(value.partition("/")[0].strip().lower())
            elif key in ("allow", "disallow") and groups:
                opening = False
                if value:
                    groups[-1][1].append((key == "allow", value))
            elif key == "crawl-delay" and groups:
                opening = False
                try:
                    delay = float(value)
                except ValueError:
                    continue
                if math.isfinite(delay) and delay >= 0:
                    groups[-1][2].append(delay)

        # The most specific match for the token, else `*`, else nothing.
        def specificity(agent: str) -> int:
            return len(agent) if agent != "*" and token.startswith(agent) else -1

        best = max(
            (specificity(agent) for agents, _, _ in groups for agent in agents),
            default=-1,
        )
        if best > 0:
            chosen = [
                group
                for group in groups
                if any(specificity(agent) == best for agent in group[0])
            ]
        else:
            chosen = [group for group in groups if "*" in group[0]]

        rules = tuple(
            (allow, robots_pattern(pattern), len(pattern))
            for _, group_rules, _ in chosen
            for allow, pattern in group_rules
        )
        delays = [delay for _, _, group_delays in chosen for delay in group_delays]
        return cls(rules, max(delays) if delays else None, sitemaps=tuple(sitemaps))

    def allows(self, url: str) -> bool:
        """Whether the normalised *url* may be fetched: the longest match decides.

        Where an `Allow` and a `Disallow` match equally long, `Allow` wins, and
        `robots.txt` itself is always allowed.
        """

        parts = urlsplit(url)
        target = parts.path + (f"?{parts.query}" if parts.query else "")
        if target == ROBOTS_PATH:
            return True
        decisive: tuple[int, bool] | None = None
        for allow, pattern, length in self.rules:
            if pattern.match(target) and (
                decisive is None or (length, allow) > decisive
            ):
                decisive = (length, allow)
        return decisive is None or decisive[1]


def robots_pattern(pattern: str) -> re.Pattern[str]:
    """A robots.txt path pattern as a regular expression: `*` any run, `$` the end."""

    anchored = pattern.endswith("$")
    body = _canonical_escapes(pattern.removesuffix("$"), QUERY_SAFE)
    expression = ".*".join(re.escape(piece) for piece in body.split("*"))
    return re.compile(expression + ("$" if anchored else ""))


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
    final_url: str | None = None  # Where the fetch ended, in its compared form.

    @property
    def final(self) -> str | None:
        """The normalised URL this record's bytes live at."""

        if self.fetched is None or not self.fetched.succeeded:
            return None
        return self.final_url

    def row(self, fetcher: str) -> dict[str, object]:
        """The manifest row: every field on every row, null where nothing is known."""

        fetched = self.fetched
        attempted = fetched is not None
        return {
            "url": self.url,
            "final_url": self.final_url if fetched else None,
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
    delay: float = DEFAULT_DELAY
    max_pages: int = DEFAULT_MAX_PAGES
    ignore_robots: bool = False
    links: bool = True
    sitemaps: bool = True
    feeds: bool = True
    includes: tuple[regex.Pattern[str], ...] = ()
    excludes: tuple[regex.Pattern[str], ...] = ()


class Mirror:
    """One run: crawl, place, rewrite, and account for it."""

    def __init__(self, options: Options, fetcher: Fetcher, log: RunLog) -> None:
        self.options = options
        self.fetcher = fetcher
        self.log = log
        self.records: dict[str, Record] = {}
        self.queue: deque[Record] = deque()
        self.fetches = 0
        self.by_final: dict[str, Record] = {}
        self.scope: Scope | None = None
        self.root_host: str | None = None
        self.start = normalise(options.url) or options.url
        self.output = options.output or Path(".")
        self.robots: dict[str, tuple[Record, Robots]] = {}
        self.token = product_token(options.user_agent)
        self.admitted = 0
        self.shells = 0
        self.last_request: float | None = None

    def run(self, staging: Path | None) -> int:
        """Mirror everything under the start page; return the exit status."""

        # The start page is a page robots.txt governs, like every other.
        start_url = self.start
        start = Record(start_url, KIND_PAGE, SOURCE_START, None)
        self.records[start_url] = start
        if not self._robots_allow(start_url):
            print(
                f"robots.txt disallows the start page {start_url}; --ignore-robots"
                " fetches it anyway. Nothing was written."
            )
            return EXIT_FAILED

        # The start page, where its redirects end, is the root of the scope.
        self._fetch(start, staging)
        if start.final is None:
            assert start.fetched is not None
            why = start.fetched.error or f"the server answered {start.fetched.status}"
            print(
                f"Could not fetch the start page {start_url}: {why}. Nothing was written."
            )
            return EXIT_FAILED
        self.root_host = urlsplit(start.final).hostname or ""
        self.scope = Scope.of(start.final, self.options.includes, self.options.excludes)
        for pattern in self.options.excludes:
            if pattern.search(start.final):
                return excludes_start(pattern, start.final)
        self.output = self.options.output or Path(self.root_host)
        self.admitted = 1
        self._settle_kind(start)

        # Sitemaps and the well-known feeds before the crawl, then the start page.
        if self.options.sitemaps:
            self._read_sitemaps()
        if self.options.feeds:
            self._read_well_known_feeds()
        self._discover(start)

        # Every page, file and resource, breadth first, one request at a time.
        while self.queue:
            record = self.queue.popleft()
            self._fetch(record, staging)
            self._settle_kind(record)
            self._discover(record)

        if not self.options.dry_run:
            self._write()
        print(self._report())
        failed = any(
            record.outcome == OUTCOME_FAILED for record in self.records.values()
        )
        return EXIT_FAILED if failed else EXIT_CLEAN

    # --- URLs, pace and robots.txt ----------------------------------------------

    def _normal(self, url: str) -> str | None:
        """*url* in its compared form, the other form of the root host folded onto it."""

        normalised = normalise(url)
        if normalised is None or not self.root_host:
            return normalised
        return fold_host(normalised, self.root_host)

    def _pace(self, url: str) -> None:
        """Wait what `--delay`, or a longer `Crawl-delay` for *url*'s host, asks."""

        delay = self.options.delay
        robots = self.robots.get(origin(url))
        if robots and robots[1].crawl_delay and not self.options.ignore_robots:
            delay = max(delay, robots[1].crawl_delay)
        if self.last_request is not None and delay > 0:
            remaining = self.last_request + delay - time.monotonic()
            if remaining > 0:
                time.sleep(remaining)

    def _request(
        self,
        url: str,
        staging: Path | None,
        follow: Callable[[str], bool] | None = None,
        keep: bool = False,
    ) -> Fetched:
        self._pace(url)
        try:
            return self.fetcher.fetch(url, staging, follow, keep)
        finally:
            self.last_request = time.monotonic()

    def _robots(self, url: str) -> Robots:
        """The rules for *url*'s host, its `robots.txt` read the first time it is asked."""

        host = origin(url)
        if host in self.robots:
            return self.robots[host][1]
        robots_url = host + ROBOTS_PATH
        record = Record(robots_url, KIND_ROBOTS, SOURCE_ROBOTS, None)
        fetched = self._request(robots_url, None, keep=True)
        record.fetched = fetched
        record.final_url = normalise(fetched.final_url)
        record.timestamp = timestamp()

        # 2xx is read; any 4xx allows everything; 5xx or no answer does too, unread.
        if fetched.succeeded and fetched.body is not None:
            robots = Robots.parse(fetched.body.decode("utf-8", "replace"), self.token)
        elif fetched.error is None and fetched.status and fetched.status < 500:
            robots = Robots()
        else:
            robots = Robots(unreadable=True)
            record.outcome = OUTCOME_FAILED
            detail = fetched.error or str(fetched.status)
            self.log.decision(OUTCOME_FAILED, robots_url, detail)
        self.robots[host] = (record, robots)
        return robots

    def _robots_allow(self, url: str) -> bool:
        robots = self._robots(url)
        return self.options.ignore_robots or robots.allows(url)

    # --- Fetching and discovery -------------------------------------------------

    def _fetch(self, record: Record, staging: Path | None) -> None:
        self.fetches += 1
        place = staging / str(self.fetches) if staging else None
        follow = self._in_scope if record.source in PAGE_SOURCES else self._not_excluded
        record.fetched = self._request(record.url, place, follow)
        record.final_url = self._normal(record.fetched.final_url)
        record.timestamp = timestamp()
        if record.fetched.redirected_out:
            record.outcome = OUTCOME_REDIRECT_OUT
            self.log.decision(OUTCOME_REDIRECT_OUT, record.url, record.final_url or "")
        elif record.final is None:
            record.outcome = OUTCOME_FAILED
            detail = record.fetched.error or str(record.fetched.status)
            self.log.decision(OUTCOME_FAILED, record.url, detail)

    def _in_scope(self, url: str) -> bool:
        normalised = self._normal(url)
        return (
            normalised is not None
            and self.scope is not None
            and self.scope.admits(normalised)
        )

    def _excluded(self, url: str) -> bool:
        """Whether an `--exclude` matches *url* in its compared form."""

        normalised = self._normal(url)
        return (
            normalised is not None
            and self.scope is not None
            and self.scope.excluded(normalised)
        )

    def _not_excluded(self, url: str) -> bool:
        """Whether a redirect may lead to *url*: an excluded URL is never requested, except along the start page's redirects."""

        return not self._excluded(url)

    def _settle_kind(self, record: Record) -> None:
        """A page or file is a page when it is HTML and a file otherwise."""

        fetched = record.fetched
        if record.kind == KIND_RESOURCE or fetched is None or record.final is None:
            return
        html = is_html(fetched.content_type, fetched.final_url)
        record.kind = KIND_PAGE if html else KIND_FILE

    def _discover(self, record: Record) -> None:
        """Take a position on every resource and link a fetched document references."""

        fetched = record.fetched
        if fetched is None or fetched.body is None or record.final is None:
            return
        links: list[str] = []
        feeds: list[str] = []
        if is_html(fetched.content_type, fetched.final_url):
            text = decode_html(fetched.body, fetched.charset)
            tree = LexborHTMLParser(text)
            found = html_references(tree, fetched.final_url)
            if self._in_scope(record.final):
                if self.options.links:
                    links = html_links(tree, fetched.final_url)
                if self.options.feeds:
                    feeds = html_feeds(tree, fetched.final_url)
            if record.kind == KIND_PAGE and is_suspected_shell(text):
                self.shells += 1
        else:
            text, _ = decode_css(fetched.body, fetched.charset)
            found = css_references(text, fetched.final_url)

        for reference in found:
            self._take_resource(reference, record)
        for reference in links:
            self._take_page(reference, SOURCE_LINK, record.url)
        for reference in feeds:
            self._read_feed(reference, SOURCE_LINK, record.url)

    def _take_resource(self, reference: str, document: Record) -> None:
        url = self._normal(reference)
        if url is None:
            return
        existing = self.records.get(url)
        excluded = self._excluded(url)
        admitted = not excluded and self._admits(url)

        # A link the crawl declined is still a resource a page needs.
        declined = (OUTCOME_OUT_OF_SCOPE, OUTCOME_ROBOTS, OUTCOME_OVER_CAP)
        if existing is not None and not (
            admitted
            and existing.kind == KIND_PAGE
            and existing.source in PAGE_SOURCES
            and existing.fetched is None
            and existing.outcome in declined
        ):
            return

        resource = Record(url, KIND_RESOURCE, SOURCE_RESOURCE, document.url)
        self.records[url] = resource
        if admitted:
            self.queue.append(resource)
        else:
            resource.outcome = OUTCOME_EXCLUDED if excluded else OUTCOME_OUT_OF_SCOPE
            self.log.decision(resource.outcome, url)

    def _take_page(self, reference: str, source: str, discovered_from: str) -> None:
        """Take a position on a page or file a link, a sitemap or a feed names."""

        url = self._normal(reference)
        if url is None:
            return

        # A resource `--resources` left out is still a page or file the crawl may take.
        existing = self.records.get(url)
        if existing is not None and not (
            existing.source == SOURCE_RESOURCE
            and existing.fetched is None
            and existing.outcome == OUTCOME_OUT_OF_SCOPE
            and self._in_scope(url)
        ):
            return
        link = Record(url, KIND_PAGE, source, discovered_from)
        self.records[url] = link

        # Exclusion first, then scope, then robots.txt, then the cap, which
        # counts at admission.
        cap = self.options.max_pages
        if self._excluded(url):
            link.outcome = OUTCOME_EXCLUDED
        elif not self._in_scope(url):
            link.outcome = OUTCOME_OUT_OF_SCOPE
        elif not self._robots_allow(url):
            link.outcome = OUTCOME_ROBOTS
        elif cap and self.admitted >= cap:
            link.outcome = OUTCOME_OVER_CAP
        else:
            self.admitted += 1
            self.queue.append(link)
            return
        self.log.decision(link.outcome, url)

    def _read_document(
        self, reference: str, kind: str, source: str, discovered_from: str | None
    ) -> Record | None:
        """Read a sitemap or feed once: the record, where there is a body to read.

        It is fetched with the run's identity and headers, obeys `robots.txt`,
        and is recorded but never placed in the tree. A well-known location
        that is not there is `missing`, which fails nothing.
        """

        url = self._normal(reference)
        if url is None or url in self.records:
            return None
        record = Record(url, kind, source, discovered_from)
        self.records[url] = record
        if self._excluded(url):
            record.outcome = OUTCOME_EXCLUDED
            self.log.decision(OUTCOME_EXCLUDED, url)
            return None
        if not self._robots_allow(url):
            record.outcome = OUTCOME_ROBOTS
            self.log.decision(OUTCOME_ROBOTS, url)
            return None

        fetched = self._request(url, None, self._not_excluded, keep=True)
        record.fetched = fetched
        record.final_url = self._normal(fetched.final_url)
        record.timestamp = timestamp()
        if fetched.succeeded and fetched.body is not None:
            return record
        if fetched.redirected_out:
            record.outcome = OUTCOME_REDIRECT_OUT
            self.log.decision(OUTCOME_REDIRECT_OUT, url, record.final_url or "")
            return None
        record.outcome = (
            OUTCOME_MISSING
            if fetched.status in MISSING_STATUSES
            and url in (*self._well_known_sitemaps(), *self._well_known_feeds())
            else OUTCOME_FAILED
        )
        self.log.decision(record.outcome, url, fetched.error or str(fetched.status))
        return None

    def _well_known_sitemaps(self) -> list[str]:
        """The sitemap locations a run tries at the root host's root."""

        assert self.scope is not None
        return [origin(self.scope.start) + path for path in SITEMAP_PATHS]

    def _well_known_feeds(self) -> list[str]:
        """The feed locations a run tries: at the root host's root, and under the root."""

        assert self.scope is not None
        root = origin(self.scope.start)
        return [root + "/" + FEED_PATH, root + self.scope.prefix + FEED_PATH]

    def _read_sitemaps(self) -> None:
        """Read every sitemap the root host's `robots.txt` or a well-known location holds.

        Indexes are followed recursively, each sitemap read once, and every URL
        a URL set names is a candidate the crawl takes as it takes a link.
        """

        assert self.scope is not None
        root = origin(self.scope.start)
        robots = self._robots(root + "/")
        robots_record = self.robots[root][0]
        pending: deque[tuple[str, str, str | None]] = deque(
            (urljoin(robots_record.url, named), SOURCE_ROBOTS, robots_record.url)
            for named in robots.sitemaps
        )
        pending.extend((url, SOURCE_PROBE, None) for url in self._well_known_sitemaps())
        while pending:
            url, source, discovered_from = pending.popleft()
            record = self._read_document(url, KIND_SITEMAP, source, discovered_from)
            if record is None or record.fetched is None or record.fetched.body is None:
                continue
            base = record.fetched.final_url
            sitemaps, pages = sitemap_entries(record.fetched.body, base)
            pending.extend((child, SOURCE_SITEMAP, record.url) for child in sitemaps)
            for page in pages:
                self._take_page(page, SOURCE_SITEMAP, record.url)

    def _read_well_known_feeds(self) -> None:
        """Read `/feed/` at the root host's root and under the root prefix."""

        for url in self._well_known_feeds():
            self._read_feed(url, SOURCE_PROBE, None)

    def _read_feed(
        self, reference: str, source: str, discovered_from: str | None
    ) -> None:
        """Read a feed once, and take every item's link as a candidate."""

        record = self._read_document(reference, KIND_FEED, source, discovered_from)
        if record is None or record.fetched is None or record.fetched.body is None:
            return
        for page in feed_entries(record.fetched.body, record.fetched.final_url):
            self._take_page(page, SOURCE_FEED, record.url)

    def _admits(self, url: str) -> bool:
        policy = self.options.resources
        if policy == "all":
            return True
        return policy == "in-scope" and self._in_scope(url)

    # --- Placement and rewriting ----------------------------------------------

    def _fetched(self) -> list[Record]:
        """Every page, file and resource fetched: what the tree holds."""

        return [
            record
            for record in self.records.values()
            if record.final is not None and record.kind not in READ_KINDS
        ]

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
            },
            folds_case(output),
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

        # The manifest, `robots.txt` files last, and the log.
        records = [
            *self.records.values(),
            *(record for record, _ in self.robots.values()),
        ]
        rows = "".join(
            json.dumps(record.row(self.fetcher.name), ensure_ascii=False) + "\n"
            for record in records
        )
        write_bytes(state / MANIFEST_NAME, rows.encode("utf-8"))
        write_bytes(
            state / LOG_NAME,
            "".join(f"{line}\n" for line in self.log.lines).encode("utf-8"),
        )

    def _located(self, url: str) -> Record | None:
        """The fetched record an absolute URL leads to, by its own URL or where it ended."""

        normalised = self._normal(url)
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
        """What the Skill relays: counts, size, what the crawl declined, and every failure."""

        records = list(self.records.values())
        fetched = [record for record in records if record.final is not None]
        saved = self._fetched()
        size = sum((record.fetched.size or 0) for record in saved if record.fetched)

        def fetched_of(kind: str) -> int:
            return sum(1 for record in fetched if record.kind == kind)

        def candidates_from(source: str) -> int:
            return sum(
                1
                for record in records
                if record.source == source and record.kind in (KIND_PAGE, KIND_FILE)
            )

        def declined(outcome: str) -> int:
            return sum(1 for record in records if record.outcome == outcome)

        failures = [record for record in records if record.outcome == OUTCOME_FAILED]
        over_cap = declined(OUTCOME_OVER_CAP)

        lines: list[str] = []
        if self.options.dry_run:
            lines.append(f"Dry run of {self.start}: nothing was written. Would fetch:")
            lines.extend(f"  {robots.url}" for robots, _ in self.robots.values())
            lines.extend(
                f"  {record.url}" for record in records if record.fetched is not None
            )
        else:
            lines.append(f"Mirrored {self.start} to {self.output}.")
        lines.append(f"Pages fetched: {fetched_of(KIND_PAGE)}")
        lines.append(f"Files fetched: {fetched_of(KIND_FILE)}")
        lines.append(f"Resources fetched: {fetched_of(KIND_RESOURCE)}")
        lines.append(f"Total size: {human_size(size)}")
        lines.append(f"Sitemaps read: {fetched_of(KIND_SITEMAP)}")
        lines.append(f"Feeds read: {fetched_of(KIND_FEED)}")
        lines.append(f"Candidates from links: {candidates_from(SOURCE_LINK)}")
        lines.append(f"Candidates from sitemaps: {candidates_from(SOURCE_SITEMAP)}")
        lines.append(f"Candidates from feeds: {candidates_from(SOURCE_FEED)}")
        lines.append(f"Out of scope: {declined(OUTCOME_OUT_OF_SCOPE)}")
        lines.append(f"Excluded: {declined(OUTCOME_EXCLUDED)}")
        lines.append(f"Redirected out of scope: {declined(OUTCOME_REDIRECT_OUT)}")
        lines.append(f"Stopped by robots.txt: {declined(OUTCOME_ROBOTS)}")
        lines.append(f"Over the cap: {over_cap}")
        lines.append(f"Suspected JavaScript shells: {self.shells}")
        if over_cap:
            lines.append(
                f"The cap of {self.options.max_pages} pages and files was reached;"
                " --max-pages raises it."
            )
        for robots, rules in self.robots.values():
            if rules.unreadable:
                lines.append(
                    f"{robots.url} could not be read, so nothing was kept out by it."
                )
        if self.shells:
            lines.append(
                "A suspected shell is a page that carries scripts but almost no"
                " text; its content is likely drawn by JavaScript, which this run"
                " does not execute."
            )
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


def excludes_start(pattern: regex.Pattern[str], start: str) -> int:
    """Refuse an `--exclude` that matches the start page, which is always in scope."""

    return refusal(
        f"'--exclude={pattern.pattern}' matches the start page {start},"
        " which is always in scope"
    )


def patterns(flag: str, values: list[str]) -> tuple[regex.Pattern[str], ...] | str:
    """Compile every *flag* value, or the refusal the first that does not compile earns."""

    compiled: list[regex.Pattern[str]] = []
    for value in values:
        try:
            compiled.append(regex.compile(value))
        except regex.error as error:
            return f"'{flag}={value}' is not a regular expression: {error}"
    return tuple(compiled)


def seconds(value: str) -> float | None:
    """A `--delay` value as seconds, or None where it is not a finite number of 0 or more."""

    try:
        amount = float(value)
    except ValueError:
        return None
    return amount if math.isfinite(amount) and amount >= 0 else None


def main(argv: list[str] | None = None) -> int:
    """Read the invocation, refuse what the Skill rejects, and run the mirror."""

    # The grammar is the invocation engine's; this reads what it let through.
    parser = argparse.ArgumentParser(prog="mirror.py")
    parser.add_argument("--output")
    parser.add_argument("--resources", default="all")
    parser.add_argument("--header", action="append", default=[])
    parser.add_argument("--user-agent", default=IDENTITY)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delay", default=str(DEFAULT_DELAY))
    parser.add_argument("--max-pages", default=str(DEFAULT_MAX_PAGES))
    parser.add_argument("--ignore-robots", action="store_true")
    parser.add_argument("--no-links", action="store_true")
    parser.add_argument("--no-sitemap", action="store_true")
    parser.add_argument("--no-feeds", action="store_true")
    parser.add_argument("--include", action="append", default=[])
    parser.add_argument("--exclude", action="append", default=[])
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
    delay = seconds(arguments.delay)
    if delay is None:
        return refusal(
            f"'--delay' takes a number of seconds, 0 or more, not '{arguments.delay}'"
        )
    if not re.fullmatch(r"[0-9]+", arguments.max_pages.strip()):
        return refusal(
            f"'--max-pages' takes a whole number, 0 or more, not '{arguments.max_pages}'"
        )
    includes = patterns("--include", arguments.include)
    if isinstance(includes, str):
        return refusal(includes)
    excludes = patterns("--exclude", arguments.exclude)
    if isinstance(excludes, str):
        return refusal(excludes)
    start = normalise(arguments.url) or arguments.url
    for pattern in excludes:
        if pattern.search(start):
            return excludes_start(pattern, start)

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
        delay=delay,
        max_pages=int(arguments.max_pages),
        ignore_robots=arguments.ignore_robots,
        links=not arguments.no_links,
        sitemaps=not arguments.no_sitemap,
        feeds=not arguments.no_feeds,
        includes=includes,
        excludes=excludes,
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
