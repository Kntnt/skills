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
to be its own (ADR-0196). Fetching sits behind the `Fetcher` protocol, so the
browser is a fetcher beside `HttpFetcher` rather than threaded through it.

A run has three passes. The fetch pass follows the start page's redirects and
crawls from there, one request at a time and breadth first: every page and file
in scope that a link, a sitemap or a feed names, as far as `robots.txt`
and the page cap allow, and every resource those pages and their stylesheets
reference that `--resources` admits; sitemaps and feeds are read, never saved.
The placement pass maps every fetched URL to a path, keeps HTML and CSS as
served under `.mirror/raw/`, a browser page as its rendered DOM without its
scripts, and puts every other file straight into the tree.
The rewrite pass derives the tree's HTML and CSS from the raw copies, so a later
run can rewrite again without fetching.

A rerun into the same output directory is incremental: the earlier manifest's
validators make every request for a file still on disk conditional, except for
a row a browser fetched, which sends none and is fetched again; a `304`
reads a page back from its raw copy, the rewrite writes only bytes that differ,
and a saved file this run did not discover stays and is recorded `absent`.

A host that blocks the run climbs a ladder of rungs, each a fetcher with its own
identity: rung 1 is plain HTTP as the Skill, rung 2 plain HTTP dressed as
Chrome, rung 3 a headless browser and rung 4 a visible one, both driven through
`agent-browser` in one session of the run's own. The rung belongs to the host
and lasts the run; a block moves the host one rung up and the blocked URL is
asked again there, and a block on the top rung the run may reach is the URL's
outcome. A browser fetch saves the rendered DOM without its scripts, and takes
the page's resources from the HAR the browser recorded while it loaded.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import math
import os
import posixpath
import re
import shlex
import shutil
import signal
import subprocess
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
from types import FrameType
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

# The identity every rung-1 request carries unless `--user-agent` replaces it, and
# the product token `robots.txt` groups are matched against.
IDENTITY = "kntnt-mirror (+https://github.com/Kntnt/skills)"
FETCHER_NAME = "http"

# The rungs a host climbs, each a fetcher and the headers it sends as its own.
# Every host starts every run on the lowest rung the run's ladder holds.
RUNG_OWN = 1  # Plain HTTP, as the Skill.
RUNG_CHROME = 2  # Plain HTTP, as Chrome.
RUNG_HEADLESS = 3  # A headless browser.
RUNG_HEADED = 4  # A visible browser, which only `--headed` lets a host reach.
FIRST_RUNG = RUNG_OWN
OWN_HEADERS = (("User-Agent", IDENTITY),)

# The identity rung 2 sends, imitating Chrome 140 on macOS. Bump every line
# together, so the version the user-agent names is the one `sec-ch-ua` names.
CHROME_HEADERS = (
    (
        "User-Agent",
        (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        ),
    ),
    (
        "Accept",
        (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
            "image/webp,*/*;q=0.8"
        ),
    ),
    ("Accept-Language", "sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7"),
    (
        "sec-ch-ua",
        '"Chromium";v="140", "Google Chrome";v="140", "Not?A_Brand";v="24"',
    ),
    ("sec-ch-ua-mobile", "?0"),
    ("sec-ch-ua-platform", '"macOS"'),
)

# `--browser`: whether a host may climb past plain HTTP to a browser, or starts there.
BROWSER_AUTO = "auto"
BROWSER_ALWAYS = "always"
BROWSER_NEVER = "never"
BROWSER_POLICIES = (BROWSER_AUTO, BROWSER_ALWAYS, BROWSER_NEVER)
DEFAULT_BROWSER = BROWSER_AUTO

# The browser rungs: the binary that drives them, the session the run owns, and
# how long a command, a headed page's challenge and each look at it may take.
BROWSER_FETCHER_NAME = "browser"
BROWSER_BINARY = "agent-browser"
SESSION_PREFIX = "kntnt-mirror-"
BROWSER_COMMAND_TIMEOUT = 180.0
HEADED_WAIT = 600.0  # Ten minutes for the person at the window to pass a challenge.
HEADED_POLL = 2.0
SCROLL_DISTANCE = 1_000_000  # Far enough to reach the bottom of any page at once.
SET_BROWSER_HEADERS = ("set", "headers")

# What reading a page in the browser returns: where it ended, the status its
# document was answered with, and the rendered DOM with its doctype.
DOM_SCRIPT = """(() => {
  const navigation = performance.getEntriesByType("navigation")[0];
  const doctype = document.doctype;
  return {
    url: location.href,
    status: navigation ? navigation.responseStatus || 0 : 0,
    doctype: doctype ? new XMLSerializer().serializeToString(doctype) : "",
    html: document.documentElement.outerHTML,
  };
})()"""

# The HAR entries a browser fetch saves, by the resource type the browser gave
# each. Every other type, `xhr`, `fetch`, `websocket`, `eventsource`, `ping`
# and `other` among them, is left: no script remains in the page to read it.
SAVED_RESOURCE_TYPES = frozenset(
    {
        "document",
        "stylesheet",
        "image",
        "font",
        "media",
        "script",
        "manifest",
        "texttrack",
    }
)
JSON_TYPE = re.compile(r"^application/(?:[\w.+-]+\+)?json$")

# A block: an answer that refuses the run's identity rather than the request.
# These statuses are a block once the retries are spent.
BLOCK_STATUSES = frozenset({403, 429, 503})
MATCH_HEADER = "header"  # Matched on every answer.
MATCH_TITLE = "title"  # Matched on every HTML answer.
MATCH_BODY = "body"  # Matched on HTML answers with a block status only.


@dataclass(frozen=True)
class Marker:
    """A sign that a bot defence answered: where it is matched, and what it is.

    A header marker with no *value* matches the header whatever its value, and
    one with a *status* only on that status. Matching is case-insensitive.
    """

    owner: str
    where: str
    text: str
    value: str | None = None
    status: int | None = None

    def describe(self) -> str:
        """The marker as the report names it."""

        if self.where == MATCH_HEADER:
            shown = f"{self.text}: {self.value}" if self.value else self.text
            return f"{self.owner}'s header `{shown}`"
        if self.where == MATCH_TITLE:
            return f'{self.owner}\'s title "{self.text}"'
        return f"{self.owner}'s `{self.text}` in the body"


BLOCK_MARKERS = (
    # Cloudflare: the header its challenges answer with.
    Marker("Cloudflare", MATCH_HEADER, "cf-mitigated", "challenge"),
    # Cloudflare: the title of its JavaScript challenge.
    Marker("Cloudflare", MATCH_TITLE, "Just a moment..."),
    # Cloudflare: the title of its block page.
    Marker("Cloudflare", MATCH_TITLE, "Attention Required! | Cloudflare"),
    # Cloudflare: the scripts of its browser check.
    Marker("Cloudflare", MATCH_BODY, "cf-browser-verification"),
    Marker("Cloudflare", MATCH_BODY, "_cf_chl_opt"),
    # Akamai: its error pages' host.
    Marker("Akamai", MATCH_BODY, "errors.edgesuite.net"),
    # Akamai: its edge server, refusing.
    Marker("Akamai", MATCH_HEADER, "Server", "AkamaiGHost", status=403),
    # PerimeterX (HUMAN): its challenge script and captcha.
    Marker("PerimeterX", MATCH_BODY, "_pxAppId"),
    Marker("PerimeterX", MATCH_BODY, "px-captcha"),
    # DataDome: its captcha host.
    Marker("DataDome", MATCH_BODY, "captcha-delivery.com"),
    # DataDome: its header.
    Marker("DataDome", MATCH_HEADER, "x-datadome"),
    # Imperva (Incapsula): its challenge resource and incident page.
    Marker("Imperva", MATCH_BODY, "_Incapsula_Resource"),
    Marker("Imperva", MATCH_BODY, "Incapsula incident ID"),
    # Imperva (Incapsula): its header.
    Marker("Imperva", MATCH_HEADER, "X-Iinfo"),
)

# Connection handling: timeouts in seconds, and what is retried after which wait.
CONNECT_TIMEOUT = 30.0
READ_TIMEOUT = 30.0
RETRIED_STATUSES = frozenset({429, 500, 502, 503, 504})
RETRY_WAITS = (1.0, 2.0, 4.0)
REDIRECT_STATUSES = frozenset({301, 302, 303, 307, 308})
NOT_MODIFIED = 304
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
OUTCOME_UNCHANGED = "unchanged"  # A conditional request the server answered `304`.
OUTCOME_ABSENT = "absent"  # Saved by an earlier run, and not discovered by this one.
OUTCOME_BLOCKED = "blocked"  # Blocked on the highest rung the run can reach.

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

# The word a dry run's list puts after a URL it would request conditionally.
CONDITIONAL_MARK = "conditional"

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
    unchanged: bool = False  # A `304`: the bytes are those an earlier run saved.
    stored: PurePosixPath | None = None  # Where an unchanged file's bytes are.
    blocked: str | None = None  # What made the answer a block, as the report names it.
    captured: list[Fetched] = field(
        default_factory=list
    )  # What a browser loaded with it.

    @property
    def succeeded(self) -> bool:
        if self.error is not None or self.status is None or self.blocked is not None:
            return False
        return self.unchanged or 200 <= self.status < 300


@dataclass(frozen=True)
class Validators:
    """What an earlier run's manifest row says identifies the bytes it saved."""

    etag: str | None
    last_modified: str | None

    def headers(self) -> list[tuple[str, str]]:
        """The conditional headers these validators can send, and only those."""

        sent: list[tuple[str, str]] = []
        if self.etag:
            sent.append(("If-None-Match", self.etag))
        if self.last_modified:
            sent.append(("If-Modified-Since", self.last_modified))
        return sent


class Fetcher(Protocol):
    """Fetches one URL. The engine names the fetcher in every manifest row."""

    name: str

    def fetch(
        self,
        url: str,
        staging: Path | None,
        follow: Callable[[str], bool] | None = None,
        keep: bool = False,
        validators: Validators | None = None,
    ) -> Fetched:
        """Fetch *url*, following redirects.

        The body of an HTML or CSS answer, or of any answer when *keep*, is
        returned in `body`. Any other body is written to *staging* and named in
        `staged`, or only counted when *staging* is None. Where *follow* says
        no to a redirect's target, the fetch stops there: `final_url` is that
        target, `status` the redirect's, and `redirected_out` is set. With
        *validators*, the request is conditional, and a `304` comes back as
        that status with whatever validators it carries and no body. An answer
        `block_reason` calls a block comes back with `blocked` set.
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
        credentials: tuple[str, str, str] | None,
        log: RunLog,
    ) -> None:
        self.credentials = credentials
        self.log = log
        self.started: dict[int, float] = {}
        # The client follows no redirect itself: on each hop httpx drops
        # `Cookie` and cross-origin `Authorization`, and every header the
        # caller gave belongs on every request, so `_send` follows them.
        self.headers = headers
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
        validators: Validators | None = None,
    ) -> Fetched:
        """Fetch *url*, retrying connection errors, timeouts and busy answers."""

        attempts = len(RETRY_WAITS) + 1
        for attempt in range(attempts):
            last = attempt == attempts - 1
            began = time.monotonic()
            try:
                with self._send(url, follow, validators) as (response, declined):
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
        self,
        url: str,
        follow: Callable[[str], bool] | None,
        validators: Validators | None = None,
    ) -> Iterator[tuple[httpx.Response, str | None]]:
        """GET *url*, following redirects with every header on every hop.

        Yields the final answer, and the redirect target *follow* declined, if any.
        """

        headers = [*self.headers, *(validators.headers() if validators else [])]
        for _ in range(MAX_REDIRECTS + 1):
            request = self.client.build_request("GET", url, headers=headers)
            response = self.client.send(request, auth=self._auth(url), stream=True)
            location = response.headers.get("Location")
            redirected = response.status_code in REDIRECT_STATUSES and location
            target = urljoin(str(response.url), location) if redirected else None
            declined = target if target and follow and not follow(target) else None
            # A redirect is an answer too: one carrying a marker is the block.
            screened = target is not None and self._screen(response) is not None
            if target is None or declined is not None or screened:
                try:
                    yield response, None if screened else declined
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

    def _screen(self, response: httpx.Response) -> str | None:
        """What makes an answer that is not kept a block, its HTML body read."""

        content_type, charset = answer_type(response)
        html = is_html(content_type, str(response.url))
        return block_reason(
            response.status_code,
            response.headers.multi_items(),
            response.read() if html else None,
            charset,
        )

    def _receive(
        self, response: httpx.Response, staging: Path | None, keep: bool
    ) -> Fetched:
        """Read one final answer: keep HTML and CSS, stage or count the rest."""

        # What the headers say.
        content_type, charset = answer_type(response)
        fetched = Fetched(
            final_url=str(response.url),
            status=response.status_code,
            content_type=content_type,
            charset=charset,
            etag=response.headers.get("ETag"),
            last_modified=response.headers.get("Last-Modified"),
        )
        headers = response.headers.multi_items()
        html = is_html(content_type, fetched.final_url)
        if not fetched.succeeded:
            # Every failed answer is screened, its HTML body read whatever the
            # status, since a title marker counts on every HTML answer.
            fetched.blocked = self._screen(response)
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
        fetched.blocked = block_reason(
            response.status_code,
            headers,
            fetched.body if html else None,
            fetched.charset,
        )
        return fetched


class BrowserUnavailable(RuntimeError):
    """`agent-browser` is missing or cannot launch a browser: the run cannot go on."""


class BrowserSession:
    """The one `agent-browser` session a run owns, started on first use and closed at the end.

    Its name carries the engine's process id, so it cannot be a session the
    user or another run has open. Every command carries the run's launch
    options, so the browser the session holds is always the one they describe.
    """

    def __init__(
        self,
        user_agent: str | None,
        headers: list[tuple[str, str]],
        profile: str | None,
    ) -> None:
        self.name = f"{SESSION_PREFIX}{os.getpid()}"
        self.user_agent = user_agent
        self.headers = headers
        self.profile = profile
        self.checked = False
        self.started = False
        self.headed: bool | None = None  # The window the headers were last set for.
        self.directory: Path | None = None
        self.hars = 0

    def ensure(self) -> None:
        """Check once, before the first browser fetch, that a browser can be launched."""

        if self.checked:
            return
        # Every command runs in the session's own directory, which lasts the
        # session, and which holds no `agent-browser.json` to change the browser.
        if self.directory is None:
            self.directory = Path(tempfile.mkdtemp(prefix="kntnt-mirror-browser-"))
        try:
            result = subprocess.run(
                [BROWSER_BINARY, "doctor", "--json"],
                cwd=self.directory,
                capture_output=True,
                text=True,
                check=False,
                timeout=BROWSER_COMMAND_TIMEOUT,
            )
        except FileNotFoundError as error:
            raise BrowserUnavailable(
                f"{BROWSER_BINARY} is not installed, and a host the run reached"
                f" needs a browser: install it with `brew install {BROWSER_BINARY}`,"
                f" then run `{BROWSER_BINARY} install`. Nothing was written."
            ) from error
        except subprocess.TimeoutExpired as error:
            raise BrowserUnavailable(
                f"{BROWSER_BINARY} could not say whether it can launch a browser:"
                f" run `{BROWSER_BINARY} install`, then run the mirror again."
                " Nothing was written."
            ) from error
        if result.returncode != 0:
            raise BrowserUnavailable(
                f"{BROWSER_BINARY} cannot launch a browser, and a host the run"
                f" reached needs one: run `{BROWSER_BINARY} install`, then run the"
                " mirror again. Nothing was written."
            )
        self.checked = True

    def har_path(self) -> Path:
        """A fresh path for one recording, in the session's own directory."""

        assert self.directory is not None
        self.hars += 1
        return self.directory / f"{self.hars}.har"

    def command(
        self, headed: bool, *arguments: str, stdin: str | None = None
    ) -> tuple[bool, object]:
        """Run one command in the session: whether it succeeded, and the data it answered."""

        self.ensure()
        if self.headers and self.headed is not headed:
            self.headed = headed
            names: dict[str, str] = {}
            for name, value in self.headers:
                names[name] = f"{names[name]}, {value}" if name in names else value
            self._run(headed, *SET_BROWSER_HEADERS, json.dumps(names))
        return self._run(headed, *arguments, stdin=stdin)

    def _run(
        self, headed: bool, *arguments: str, stdin: str | None = None
    ) -> tuple[bool, object]:
        launch = ["--session", self.name]
        if self.profile:
            launch += ["--profile", self.profile]
        if self.user_agent:
            launch += ["--user-agent", self.user_agent]
        if headed:
            launch.append("--headed")
        self.started = True
        try:
            result = subprocess.run(
                [BROWSER_BINARY, *launch, "--json", *arguments],
                cwd=self.directory,
                input=stdin,
                capture_output=True,
                text=True,
                check=False,
                timeout=BROWSER_COMMAND_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return False, f"{BROWSER_BINARY} {arguments[0]} did not answer in time"
        try:
            answer = json.loads(result.stdout)
        except json.JSONDecodeError:
            answer = None
        if not isinstance(answer, dict):
            detail = (result.stderr or result.stdout).strip() or "no answer"
            return result.returncode == 0, detail
        if result.returncode != 0 or answer.get("success") is False:
            return False, answer.get("error") or result.stderr.strip() or "failed"
        return True, answer.get("data")

    def close(self) -> None:
        """Close the session, where the run started one, and remove its recordings."""

        if self.started:
            self.started = False
            try:
                subprocess.run(
                    [BROWSER_BINARY, "--session", self.name, "close"],
                    cwd=self.directory,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=BROWSER_COMMAND_TIMEOUT,
                )
            except (OSError, subprocess.SubprocessError):
                pass
        if self.directory is not None:
            shutil.rmtree(self.directory, ignore_errors=True)
            self.directory = None


@dataclass(frozen=True)
class Rendered:
    """What reading a page in the browser gave: where it is, its status, and its DOM."""

    url: str
    status: int
    html: str

    @classmethod
    def of(cls, data: object) -> Rendered | None:
        result = data.get("result") if isinstance(data, dict) else None
        if not isinstance(result, dict) or not isinstance(result.get("html"), str):
            return None
        status = result.get("status")
        return cls(
            str(result.get("url") or ""),
            status if isinstance(status, int) else 0,
            str(result.get("doctype") or "") + result["html"],
        )

    def blocked(self) -> str | None:
        """What makes the page as it stands a challenge, judged on its status and DOM."""

        return block_reason(self.status, [], self.html.encode("utf-8"), "utf-8")


class BrowserFetcher:
    """A browser in the run's session: headless on rung 3, visible on rung 4."""

    name = BROWSER_FETCHER_NAME

    def __init__(self, session: BrowserSession, headed: bool, log: RunLog) -> None:
        self.session = session
        self.headed = headed
        self.log = log

    def fetch(
        self,
        url: str,
        staging: Path | None,
        follow: Callable[[str], bool] | None = None,
        keep: bool = False,
        validators: Validators | None = None,
    ) -> Fetched:
        """Load *url* in the browser under a HAR recording, and read what it rendered.

        The browser makes no conditional request, so *validators* go unused.
        """

        began = time.monotonic()
        self.session.ensure()
        har = self.session.har_path()
        started, detail = self.session.command(
            self.headed, "network", "har", "start", "--content", "all"
        )
        if not started:
            return Fetched(url, error=f"the browser could not record: {detail}")
        rendered: Rendered | None = None
        try:
            opened, detail = self.session.command(self.headed, "open", url)
            if opened:
                rendered = self._load()
        finally:
            self.session.command(self.headed, "network", "har", "stop", str(har))
        if not opened:
            return Fetched(url, error=f"the browser could not open it: {detail}")
        if rendered is None:
            return Fetched(url, error="the browser could not read the page")
        entries = har_entries(har)
        har.unlink(missing_ok=True)
        fetched = self._answer(url, rendered, entries, staging, follow, keep)
        self.log.request(
            "GET", url, str(fetched.status or "error"), time.monotonic() - began
        )
        return fetched

    def _load(self) -> Rendered | None:
        """Let the page settle, past a challenge where a person can pass one, and read it."""

        self.session.command(self.headed, "wait", "--load", "networkidle")
        if self.headed:
            deadline = time.monotonic() + HEADED_WAIT
            while True:
                seen = Rendered.of(self._read())
                if seen is not None and seen.blocked() is None:
                    break
                if time.monotonic() >= deadline:
                    return seen
                time.sleep(HEADED_POLL)
            self.session.command(self.headed, "wait", "--load", "networkidle")
        self.session.command(self.headed, "scroll", "down", str(SCROLL_DISTANCE))
        self.session.command(self.headed, "wait", "--load", "networkidle")
        return Rendered.of(self._read())

    def _read(self) -> object:
        _, data = self.session.command(self.headed, "eval", "--stdin", stdin=DOM_SCRIPT)
        return data

    def _answer(
        self,
        url: str,
        rendered: Rendered,
        entries: list[dict[str, object]],
        staging: Path | None,
        follow: Callable[[str], bool] | None,
        keep: bool,
    ) -> Fetched:
        """What the browser's load of *url* comes to, as HTTP's answer would."""

        # The document is the last one recorded where the page ended.
        final = normalise(rendered.url) if rendered.url else None
        documents = [entry for entry in entries if har_type(entry) == "document"]
        main = next(
            (
                entry
                for entry in reversed(documents)
                if normalise(har_url(entry)) == final
            ),
            documents[-1] if documents else None,
        )
        if final is None or (main is None and not rendered.status):
            return Fetched(url, error="the browser got no answer")
        final_url = rendered.url
        if final != normalise(url) and follow is not None and not follow(final_url):
            return Fetched(final_url, status=har_status(main), redirected_out=True)

        headers = har_headers(main) if main is not None else []
        status = har_status(main) or rendered.status
        content_type, charset = header_type(headers)
        if content_type is None and main is not None:
            content_type = header_type([("Content-Type", har_mime(main))])[0]
        fetched = Fetched(final_url, status=status, content_type=content_type)

        # A page is its rendered DOM, judged with its scripts and saved without.
        if is_html(content_type, final_url):
            dom = rendered.html.encode("utf-8")
            fetched.blocked = block_reason(status, headers, dom, "utf-8")
            body: bytes | None = without_scripts(rendered.html).encode("utf-8")
            fetched.charset = "utf-8"
            if fetched.succeeded:
                fetched.captured = self._captured(entries, main, staging)
        else:
            fetched.blocked = block_reason(status, headers, None, charset)
            body, recoded = har_body(main) if main is not None else (None, False)
            fetched.charset = "utf-8" if recoded else charset
            if body is None and fetched.succeeded:
                return Fetched(final_url, error="the browser kept no body for it")
        if body is not None:
            settle_body(fetched, body, staging, keep)
        return fetched

    def _captured(
        self,
        entries: list[dict[str, object]],
        main: dict[str, object] | None,
        staging: Path | None,
    ) -> list[Fetched]:
        """Every resource the page loaded that a mirror keeps, one per URL, last answer kept."""

        captured: dict[str, Fetched] = {}
        for position, entry in enumerate(entries):
            if entry is main or not saves(entry):
                continue
            status = har_status(entry)
            body, recoded = har_body(entry)
            if status is None or not 200 <= status < 300 or body is None:
                continue
            content_type, charset = header_type(har_headers(entry))
            if content_type is None:
                content_type = header_type([("Content-Type", har_mime(entry))])[0]
            item = Fetched(
                har_url(entry),
                status=status,
                content_type=content_type,
                charset="utf-8" if recoded else charset,
            )
            place = staging.with_name(f"{staging.name}-{position}") if staging else None
            settle_body(item, body, place, keep=False)
            captured[har_url(entry)] = item
        return list(captured.values())


def settle_body(
    fetched: Fetched, body: bytes, staging: Path | None, keep: bool
) -> None:
    """Keep *body* where the rewrite or the caller reads it, and stage or count it otherwise."""

    fetched.size = len(body)
    fetched.sha256 = hashlib.sha256(body).hexdigest()
    if keep or is_rewritable(fetched.content_type, fetched.final_url):
        fetched.body = body
    elif staging is not None:
        staging.parent.mkdir(parents=True, exist_ok=True)
        staging.write_bytes(body)
        fetched.staged = staging


def without_scripts(html: str) -> str:
    """A rendered DOM with every `script` element removed and every `noscript` kept."""

    tree = LexborHTMLParser(html)
    for node in tree.css("script"):
        node.decompose()
    return tree.html or ""


def har_entries(path: Path) -> list[dict[str, object]]:
    """The entries of a HAR file, or none where it is missing or unreadable."""

    try:
        har = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    log = har.get("log") if isinstance(har, dict) else None
    entries = log.get("entries") if isinstance(log, dict) else None
    return (
        [entry for entry in entries if isinstance(entry, dict)]
        if isinstance(entries, list)
        else []
    )


def _part(entry: dict[str, object] | None, name: str) -> dict[str, object]:
    part = entry.get(name) if entry is not None else None
    return part if isinstance(part, dict) else {}


def har_url(entry: dict[str, object]) -> str:
    return str(_part(entry, "request").get("url") or "")


def har_type(entry: dict[str, object]) -> str | None:
    kind = entry.get("_resourceType")
    return kind.lower() if isinstance(kind, str) else None


def har_status(entry: dict[str, object] | None) -> int | None:
    status = _part(entry, "response").get("status")
    return status if isinstance(status, int) and status > 0 else None


def har_headers(entry: dict[str, object]) -> list[tuple[str, str]]:
    headers = _part(entry, "response").get("headers")
    if not isinstance(headers, list):
        return []
    return [
        (str(header.get("name")), str(header.get("value")))
        for header in headers
        if isinstance(header, dict) and header.get("name") is not None
    ]


def har_mime(entry: dict[str, object]) -> str:
    content = _part(_part(entry, "response"), "content")
    return str(content.get("mimeType") or "")


def har_body(entry: dict[str, object]) -> tuple[bytes | None, bool]:
    """An entry's body, and whether it came as text the HAR holds in UTF-8 rather than as its bytes."""

    content = _part(_part(entry, "response"), "content")
    text = content.get("text")
    if not isinstance(text, str):
        return None, False
    if content.get("encoding") == "base64":
        try:
            return base64.b64decode(text, validate=True), False
        except (binascii.Error, ValueError):
            return None, False
    return text.encode("utf-8"), True


def saves(entry: dict[str, object]) -> bool:
    """Whether a browser fetch keeps a HAR entry: by its resource type, or where it has none, unless it is JSON."""

    kind = har_type(entry)
    if kind is not None:
        return kind in SAVED_RESOURCE_TYPES
    media_type = header_type([("Content-Type", har_mime(entry))])[0] or ""
    return JSON_TYPE.match(media_type) is None


def header_type(headers: Iterable[tuple[str, str]]) -> tuple[str | None, str | None]:
    """A media type, lowercased, and the charset a `Content-Type` among *headers* names."""

    value = next(
        (value for name, value in headers if name.lower() == "content-type"), ""
    )
    media_type, _, parameters = value.partition(";")
    charset = re.search(r"charset=\"?([^\";\s]+)", parameters, re.IGNORECASE)
    return media_type.strip().lower() or None, charset.group(1) if charset else None


def answer_type(response: httpx.Response) -> tuple[str | None, str | None]:
    """An answer's media type, lowercased, and the charset its header names."""

    return header_type([("Content-Type", response.headers.get("Content-Type", ""))])


def block_reason(
    status: int, headers: list[tuple[str, str]], html: bytes | None, charset: str | None
) -> str | None:
    """What makes an answer a block, as the report names it, or None where it is none.

    *status* is the final answer's, its retries spent, and *html* the body of
    an HTML answer, or None for any other. A marker is named where one matches,
    after the status where the status is a block too; header markers are
    matched on every answer, title markers on every HTML answer, and body
    markers only on an HTML answer with a block status.
    """

    blocked_status = status in BLOCK_STATUSES
    text = decode_html(html, charset) if html is not None else None
    title = page_title(text) if text is not None else None
    for marker in BLOCK_MARKERS:
        if marker.status is not None and marker.status != status:
            continue
        if marker.where == MATCH_HEADER:
            found = any(
                name.lower() == marker.text.lower()
                and (marker.value is None or marker.value.lower() in value.lower())
                for name, value in headers
            )
        elif marker.where == MATCH_TITLE:
            found = title is not None and title.lower() == marker.text.lower()
        else:
            found = (
                blocked_status
                and text is not None
                and marker.text.lower() in text.lower()
            )
        if found:
            described = marker.describe()
            return f"{status} with {described}" if blocked_status else described
    return str(status) if blocked_status else None


def page_title(text: str) -> str | None:
    """A page's title, whitespace collapsed, or None where it has none."""

    node = LexborHTMLParser(text).css_first("title")
    return " ".join(node.text(deep=True).split()) if node is not None else None


def compose_headers(
    identity: Iterable[tuple[str, str]],
    user_agent: str | None,
    headers: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    """The headers one rung sends: its identity, as the user replaced it.

    `--user-agent` replaces the rung's `User-Agent`, and a `--header` whose
    name the rung also sets replaces the rung's header of that name.
    """

    replaced = {name.lower() for name, _ in headers}
    own = [
        (name, user_agent if user_agent and name.lower() == "user-agent" else value)
        for name, value in identity
        if name.lower() not in replaced
    ]
    return [*own, *headers]


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
    conditional: bool = False  # Requested with an earlier run's validators.
    fetcher: str | None = None  # The fetcher of the last attempt, None before one.
    rung: int | None = None  # The rung of the last attempt, None before one.

    @property
    def final(self) -> str | None:
        """The normalised URL this record's bytes live at."""

        if self.fetched is None or not self.fetched.succeeded:
            return None
        return self.final_url

    def row(self) -> dict[str, object]:
        """The manifest row: every field on every row, null where nothing is known."""

        fetched = self.fetched
        return {
            "url": self.url,
            "final_url": self.final_url if fetched else None,
            "kind": self.kind,
            "source": self.source,
            "discovered_from": self.discovered_from,
            "fetcher": self.fetcher,
            "rung": self.rung,
            "status": fetched.status if fetched else None,
            "content_type": fetched.content_type if fetched else None,
            "charset": fetched.charset if fetched else None,
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
    browser: str = DEFAULT_BROWSER
    headed: bool = False
    invocation: tuple[str, ...] = ()  # The arguments as given, for a command to paste.


@dataclass(frozen=True)
class Climb:
    """One step a host took up the ladder: the rung, and the block that moved it."""

    rung: int
    reason: str
    url: str


class Mirror:
    """One run: crawl, place, rewrite, and account for it."""

    def __init__(
        self, options: Options, fetchers: dict[int, Fetcher], log: RunLog
    ) -> None:
        self.options = options
        self.fetchers = fetchers
        self.log = log
        self.rungs: dict[str, int] = {}  # The rung each host asked is on.
        self.climbs: dict[str, list[Climb]] = {}
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
        self.previous: dict[str, dict[str, object]] = {}
        self.previous_output: Path | None = None
        self.absent: list[dict[str, object]] = []
        # What a browser loaded with a page, by URL, and the rung it was loaded on.
        self.captured: dict[str, tuple[Fetched, int]] = {}

    def run(self, staging: Path | None) -> int:
        """Mirror everything under the start page; return the exit status."""

        # An earlier run's manifest makes every request it can conditional.
        start_url = self.start
        self._remember(self.options.output or Path(urlsplit(start_url).hostname or ""))

        # The start page is a page robots.txt governs, like every other.
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
            if start.fetched.blocked is not None:
                why = (
                    f"it was blocked on rung {start.rung} after"
                    f" {with_article(start.fetched.blocked)}, and rung {start.rung}"
                    " was not enough"
                )
            print(
                f"Could not fetch the start page {start_url}: {why}. Nothing was written."
            )
            for line in self._next_step([start]):
                print(line)
            return EXIT_FAILED
        self.root_host = urlsplit(start.final).hostname or ""
        self.scope = Scope.of(start.final, self.options.includes, self.options.excludes)
        for pattern in self.options.excludes:
            if pattern.search(start.final):
                return excludes_start(pattern, start.final)
        self.output = self.options.output or Path(self.root_host)
        self._remember(self.output)
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

        # What an earlier run saved and this one never came to.
        self._settle_absent()
        if not self.options.dry_run:
            self._write()
        print(self._report())
        failed = any(
            record.outcome in (OUTCOME_FAILED, OUTCOME_BLOCKED)
            for record in self.records.values()
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
        record: Record,
        staging: Path | None,
        follow: Callable[[str], bool] | None = None,
        keep: bool = False,
        validators: Validators | None = None,
    ) -> Fetched:
        """Fetch *record*'s URL on its host's rung, climbing while the host blocks it.

        The first block on a host moves the host one rung up, so every later
        request to it goes there, and the blocked URL is asked again there at
        once. A block on the highest rung is returned as it came.
        """

        url = record.url
        host = origin(url)
        while True:
            rung = self.rungs.setdefault(host, min(self.fetchers))
            fetcher = self.fetchers[rung]
            self._pace(url)
            try:
                fetched = fetcher.fetch(url, staging, follow, keep, validators)
            finally:
                self.last_request = time.monotonic()
            record.fetcher, record.rung = fetcher.name, rung
            if fetched.blocked is None:
                return fetched
            higher = [step for step in self.fetchers if step > rung]
            if not higher:
                self.log.decision(
                    OUTCOME_BLOCKED, url, f"rung {rung} {fetched.blocked}"
                )
                return fetched
            self.rungs[host] = min(higher)
            self.climbs.setdefault(host, []).append(
                Climb(min(higher), fetched.blocked, url)
            )
            self.log.decision(
                "climbed", host, f"rung {min(higher)} {fetched.blocked} {url}"
            )

    def _robots(self, url: str) -> Robots:
        """The rules for *url*'s host, its `robots.txt` read the first time it is asked."""

        host = origin(url)
        if host in self.robots:
            return self.robots[host][1]
        robots_url = host + ROBOTS_PATH
        record = Record(robots_url, KIND_ROBOTS, SOURCE_ROBOTS, None)
        fetched = self._request(record, None, keep=True)
        record.fetched = fetched
        record.final_url = normalise(fetched.final_url)
        record.timestamp = timestamp()

        # 2xx is read; any 4xx allows everything; 5xx or no answer does too, unread.
        if fetched.succeeded and fetched.body is not None:
            robots = Robots.parse(fetched.body.decode("utf-8", "replace"), self.token)
        elif fetched.error is None and fetched.status and fetched.status < 500:
            robots = Robots()
        elif fetched.blocked is not None:
            robots = Robots(unreadable=True)
            record.outcome = OUTCOME_BLOCKED
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

    # --- An earlier run -----------------------------------------------------------

    def _remember(self, output: Path) -> None:
        """Read the manifest an earlier run left in *output*, where there is one.

        Read once per output directory: the start page's own request goes to
        the directory its URL names, and the rest to the one the run writes.
        """

        if output == self.previous_output:
            return
        self.previous_output = output
        self.previous = {}
        manifest = output / STATE_DIRECTORY / MANIFEST_NAME
        if not manifest.is_file():
            return
        for line in manifest.read_text(encoding="utf-8").splitlines():
            row = json.loads(line) if line.strip() else None
            if isinstance(row, dict) and isinstance(row.get("url"), str):
                self.previous[row["url"]] = row

    def _saved(self, row: dict[str, object]) -> PurePosixPath | None:
        """The path of the file an earlier run's row saved, while it is still there."""

        local_path = row.get("local_path")
        if self.previous_output is None or not isinstance(local_path, str):
            return None
        if not (self.previous_output / local_path).is_file():
            return None
        return PurePosixPath(local_path)

    def _reusable(self, url: str) -> dict[str, object] | None:
        """The earlier row a request for *url* can be made conditional on, or None.

        It needs a saved file that is still there, its raw copy too where the
        rewrite reads it, and at least one validator to send.
        """

        row = self.previous.get(url)
        if row is None or self.previous_output is None:
            return None
        # A browser sends no validators, so what it fetched is fetched again.
        if row.get("fetcher") == BROWSER_FETCHER_NAME:
            return None
        saved = self._saved(row)
        if saved is None or not (row.get("etag") or row.get("last_modified")):
            return None
        content_type = optional_text(row.get("content_type"))
        final = optional_text(row.get("final_url")) or url
        raw = self.previous_output / STATE_DIRECTORY / RAW_DIRECTORY / str(saved)
        if is_rewritable(content_type, final) and not raw.is_file():
            return None
        return row

    def _unchanged(self, answer: Fetched, row: dict[str, object]) -> Fetched:
        """What a `304` stands for: the earlier row, updated by what the `304` carries.

        A rewritable file's bytes are read back from its raw copy, so the page
        is read for links and resources, and rewritten, as a fetched one is.
        """

        assert self.previous_output is not None
        saved = self._saved(row)
        assert saved is not None
        earlier_type = optional_text(row.get("content_type"))
        rewritable = is_rewritable(earlier_type, answer.final_url)
        raw = self.previous_output / STATE_DIRECTORY / RAW_DIRECTORY / str(saved)
        size = row.get("size")
        return Fetched(
            final_url=answer.final_url,
            status=answer.status,
            content_type=answer.content_type or earlier_type,
            charset=answer.charset or optional_text(row.get("charset")),
            etag=answer.etag or optional_text(row.get("etag")),
            last_modified=answer.last_modified
            or optional_text(row.get("last_modified")),
            size=size if isinstance(size, int) else None,
            sha256=optional_text(row.get("sha256")),
            body=raw.read_bytes() if rewritable else None,
            unchanged=True,
            stored=saved,
        )

    def _settle_absent(self) -> None:
        """Record every file an earlier run saved whose URL this run did not discover.

        The file stays where it is: nothing is ever deleted from the tree.
        """

        self.absent = []
        for url, row in self.previous.items():
            if url in self.records or self._saved(row) is None:
                continue
            self.absent.append(
                {
                    **row,
                    "fetcher": None,
                    "rung": None,
                    "outcome": OUTCOME_ABSENT,
                    "timestamp": timestamp(),
                }
            )
            self.log.decision(OUTCOME_ABSENT, url)

    # --- Fetching and discovery -------------------------------------------------

    def _fetch(self, record: Record, staging: Path | None) -> None:
        self.fetches += 1
        place = staging / str(self.fetches) if staging else None
        follow = self._in_scope if record.source in PAGE_SOURCES else self._not_excluded
        previous = self._reusable(record.url)
        validators = (
            Validators(
                optional_text(previous.get("etag")),
                optional_text(previous.get("last_modified")),
            )
            if previous is not None
            else None
        )

        # A resource a browser already loaded with a page is taken as it loaded it.
        captured = (
            self.captured.pop(record.url, None)
            if record.kind == KIND_RESOURCE
            else None
        )
        if captured is not None:
            fetched, record.rung = captured
            record.fetcher = BROWSER_FETCHER_NAME
        else:
            record.conditional = validators is not None
            fetched = self._request(record, place, follow, validators=validators)
            record.conditional &= record.fetcher != BROWSER_FETCHER_NAME
            for item in fetched.captured:
                key = self._normal(item.final_url)
                if key is not None and record.rung is not None:
                    self.captured.setdefault(key, (item, record.rung))
        if (
            previous is not None
            and fetched.status == NOT_MODIFIED
            and not fetched.error
            and fetched.blocked is None
        ):
            fetched = self._unchanged(fetched, previous)
            record.outcome = OUTCOME_UNCHANGED
        record.fetched = fetched
        record.final_url = self._normal(record.fetched.final_url)
        record.timestamp = timestamp()
        if record.fetched.redirected_out:
            record.outcome = OUTCOME_REDIRECT_OUT
            self.log.decision(OUTCOME_REDIRECT_OUT, record.url, record.final_url or "")
        elif record.fetched.blocked is not None:
            record.outcome = OUTCOME_BLOCKED
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
        """Whether a redirect may lead to *url*.

        Over plain HTTP an excluded URL is never requested, except along the
        start page's redirects; a browser has already followed the redirect,
        and this only records it.
        """

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
            found.extend(item.final_url for item in fetched.captured)
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

        fetched = self._request(record, None, self._not_excluded, keep=True)
        record.fetched = fetched
        record.final_url = self._normal(fetched.final_url)
        record.timestamp = timestamp()
        if fetched.succeeded and fetched.body is not None:
            return record
        if fetched.redirected_out:
            record.outcome = OUTCOME_REDIRECT_OUT
            self.log.decision(OUTCOME_REDIRECT_OUT, url, record.final_url or "")
            return None
        if fetched.blocked is not None:
            record.outcome = OUTCOME_BLOCKED
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

        # HTML and CSS go to raw as served, a browser page as its rendered DOM
        # without its scripts; everything else straight to the tree,
        # where an unchanged file already is unless its path moved.
        for final, record in by_final.items():
            fetched = record.fetched
            assert fetched is not None
            target = output / str(paths[final])
            if fetched.body is not None:
                write_bytes(raw / str(paths[final]), fetched.body)
            elif fetched.staged is not None:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(fetched.staged, target)
            elif fetched.stored is not None and fetched.stored != paths[final]:
                write_bytes(target, (output / str(fetched.stored)).read_bytes())

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

        # The manifest, `robots.txt` files and what is absent last, and the log.
        records = [
            *self.records.values(),
            *(record for record, _ in self.robots.values()),
        ]
        rows = "".join(
            json.dumps(row, ensure_ascii=False) + "\n"
            for row in (
                *(record.row() for record in records),
                *self.absent,
            )
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
        fetched = [
            record
            for record in records
            if record.final is not None and record.outcome != OUTCOME_UNCHANGED
        ]
        saved = [
            record for record in self._fetched() if record.outcome != OUTCOME_UNCHANGED
        ]
        size = sum((record.fetched.size or 0) for record in saved if record.fetched)

        def fetched_of(kind: str) -> int:
            return sum(1 for record in fetched if record.kind == kind)

        def unchanged_of(kind: str) -> int:
            return sum(
                1
                for record in records
                if record.outcome == OUTCOME_UNCHANGED and record.kind == kind
            )

        def candidates_from(source: str) -> int:
            return sum(
                1
                for record in records
                if record.source == source and record.kind in (KIND_PAGE, KIND_FILE)
            )

        def declined(outcome: str) -> int:
            return sum(1 for record in records if record.outcome == outcome)

        failures = [
            record
            for record in records
            if record.outcome in (OUTCOME_FAILED, OUTCOME_BLOCKED)
        ]
        over_cap = declined(OUTCOME_OVER_CAP)
        robots_records = [record for record, _ in self.robots.values()]
        blocked = [
            record
            for record in (*records, *robots_records)
            if record.outcome == OUTCOME_BLOCKED
        ]

        lines: list[str] = []
        if self.options.dry_run:
            lines.append(f"Dry run of {self.start}: nothing was written. Would fetch:")
            lines.extend(f"  {robots.url}" for robots, _ in self.robots.values())
            lines.extend(
                f"  {record.url}{f' {CONDITIONAL_MARK}' if record.conditional else ''}"
                for record in records
                if record.fetched is not None
            )
        else:
            lines.append(f"Mirrored {self.start} to {self.output}.")
        lines.append(f"Pages fetched: {fetched_of(KIND_PAGE)}")
        lines.append(f"Files fetched: {fetched_of(KIND_FILE)}")
        lines.append(f"Resources fetched: {fetched_of(KIND_RESOURCE)}")
        lines.append(f"Pages unchanged: {unchanged_of(KIND_PAGE)}")
        lines.append(f"Files unchanged: {unchanged_of(KIND_FILE)}")
        lines.append(f"Resources unchanged: {unchanged_of(KIND_RESOURCE)}")
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
        lines.append(f"Absent: {len(self.absent)}")
        lines.append(f"Suspected JavaScript shells: {self.shells}")
        lines.append(f"Blocked: {len(blocked)}")
        lines.append(
            "Hosts that stayed on rung 1: "
            f"{sum(1 for rung in self.rungs.values() if rung == FIRST_RUNG)}"
        )
        blocked_hosts = {origin(record.url) for record in blocked}
        for host, rung in self.rungs.items():
            if rung == FIRST_RUNG and host not in blocked_hosts:
                continue
            climb = self.climbs[host][-1] if host in self.climbs else None
            line = f"{host} is on rung {rung}"
            if climb is not None:
                line = (
                    f"{host} climbed to rung {rung} after"
                    f" {with_article(climb.reason)} on {climb.url}"
                )
            if host in blocked_hosts:
                count = sum(1 for record in blocked if origin(record.url) == host)
                line += (
                    f", and rung {rung} was not enough: {count} of its URLs"
                    " stayed blocked"
                )
            lines.append(line + ".")
        lines.extend(self._next_step(blocked))
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
                "A suspected shell is a page fetched over plain HTTP that carries"
                " scripts but almost no text; its content is likely drawn by"
                " JavaScript, which plain HTTP does not execute."
            )
        if failures:
            lines.append(f"Failures: {len(failures)}")
            for record in failures:
                assert record.fetched is not None
                status = record.fetched.status or f"no answer ({record.fetched.error})"
                lines.append(f"  {record.fetched.blocked or status} {record.url}")
        return "\n".join(lines)

    def _next_step(self, blocked: Iterable[Record]) -> list[str]:
        """Where the headless browser was not enough and a visible one may be: what to run.

        The command is the invocation as given with `--headed` added before
        the URL, on a line of its own, ready to paste.
        """

        if RUNG_HEADLESS not in self.fetchers or RUNG_HEADED in self.fetchers:
            return []
        urls = [record.url for record in blocked if record.rung == RUNG_HEADLESS]
        if not urls:
            return []
        given = list(self.options.invocation)
        if self.options.url in given:
            given.pop(len(given) - 1 - given[::-1].index(self.options.url))
        command = " ".join(
            shlex.quote(argument) for argument in (*given, "--headed", self.options.url)
        )
        explanation = (
            f"Still blocked in the headless browser: {', '.join(urls)}. --headed is"
            " the next step: it opens a visible browser, where you can pass the"
            " challenge or log in, and waits for you. Run:"
        )
        return [explanation, f"/mirror {command}"]


def decode_css(body: bytes, charset: str | None) -> tuple[str, str]:
    """Decode a stylesheet as CSS Syntax says: BOM, header, `@charset`, UTF-8.

    Returns the text and the codec it was decoded with, which a rewritten
    stylesheet is encoded back into so that its `@charset` stays true.
    """

    text, encoding = tinycss2.bytes.decode_stylesheet_bytes(
        body, protocol_encoding=charset
    )
    return text, encoding.codec_info.name


def with_article(reason: str) -> str:
    """A block's reason as it follows "after": a status takes "a", a marker none."""

    return f"a {reason}" if reason[:1].isdigit() else reason


def write_bytes(path: Path, content: bytes) -> None:
    """Write *content* to *path*, unless the file there already holds exactly it.

    An unchanged file keeps its modification time through a rerun's rewrite.
    """

    if (
        path.is_file()
        and path.stat().st_size == len(content)
        and path.read_bytes() == content
    ):
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def optional_text(value: object) -> str | None:
    """A manifest value as text, or None where it is not."""

    return value if isinstance(value, str) else None


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


def ladder(
    user_agent: str | None,
    headers: list[tuple[str, str]],
    credentials: tuple[str, str, str] | None,
    log: RunLog,
    browser: str,
    headed: bool,
    session: BrowserSession,
) -> dict[int, Fetcher]:
    """The rungs a host may climb, each with its fetcher, lowest first.

    `never` keeps a host on plain HTTP, rungs 1 and 2; `auto` adds the headless
    browser, and the visible one where `--headed` allows it; `always` holds
    only the browser, headless or, with `--headed`, visible.
    """

    http: dict[int, Fetcher] = {
        RUNG_OWN: HttpFetcher(
            compose_headers(OWN_HEADERS, user_agent, headers), credentials, log
        ),
        RUNG_CHROME: HttpFetcher(
            compose_headers(CHROME_HEADERS, user_agent, headers), credentials, log
        ),
    }
    browsers: dict[int, Fetcher] = {
        RUNG_HEADLESS: BrowserFetcher(session, headed=False, log=log),
        RUNG_HEADED: BrowserFetcher(session, headed=True, log=log),
    }
    if browser == BROWSER_NEVER:
        return http
    if browser == BROWSER_ALWAYS:
        rung = RUNG_HEADED if headed else RUNG_HEADLESS
        return {rung: browsers[rung]}
    if not headed:
        browsers.pop(RUNG_HEADED)
    return {**http, **browsers}


def profile(value: str | None) -> str | None:
    """A `--profile` as the browser takes it: a name as given, a path made absolute.

    The browser runs in a directory of its own, so a relative path is resolved
    against the invocation's working directory first.
    """

    if value is None or not (os.sep in value or value.startswith((".", "~"))):
        return value
    return str(Path(value).expanduser().resolve())


def interrupted(signum: int, frame: FrameType | None) -> None:
    """End the run on `SIGINT` or `SIGTERM` as an exit does, so the session is closed."""

    raise SystemExit(128 + signum)


def main(argv: list[str] | None = None) -> int:
    """Read the invocation, refuse what the Skill rejects, and run the mirror."""

    # The grammar is the invocation engine's; this reads what it let through.
    parser = argparse.ArgumentParser(prog="mirror.py")
    parser.add_argument("--output")
    parser.add_argument("--resources", default="all")
    parser.add_argument("--header", action="append", default=[])
    parser.add_argument("--user-agent")
    parser.add_argument("--browser", default=DEFAULT_BROWSER)
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--profile")
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
    given = list(sys.argv[1:] if argv is None else argv)
    arguments = parser.parse_args(given)

    # A value whose form the page admits and whose meaning the Skill rejects.
    parts = urlsplit(arguments.url)
    if parts.scheme.lower() not in DEFAULT_PORTS or not parts.hostname:
        return refusal(f"'{arguments.url}' is not an absolute http or https URL")
    if arguments.resources not in RESOURCE_POLICIES:
        return refusal(
            f"'--resources' takes all, in-scope or none, not '{arguments.resources}'"
        )
    if arguments.browser not in BROWSER_POLICIES:
        return refusal(
            f"'--browser' takes auto, always or never, not '{arguments.browser}'"
        )
    if arguments.browser == BROWSER_NEVER:
        for flag, given_flag in (
            ("--headed", arguments.headed),
            ("--profile", arguments.profile is not None),
        ):
            if given_flag:
                return refusal(
                    f"'{flag}' needs a browser, and '--browser=never' keeps every"
                    " host on plain HTTP"
                )
    if arguments.profile is not None and not arguments.profile.strip():
        return refusal("'--profile' takes a Chrome profile name or a directory path")
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
        user_agent=arguments.user_agent or IDENTITY,
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
        browser=arguments.browser,
        headed=arguments.headed,
        invocation=tuple(given),
    )

    # Run; a real run stages the files it downloads outside the output directory,
    # and the browser session is closed however the run ends.
    log = RunLog()
    session = BrowserSession(arguments.user_agent, headers, profile(arguments.profile))
    fetchers = ladder(
        arguments.user_agent,
        headers,
        credentials,
        log,
        arguments.browser,
        arguments.headed,
        session,
    )
    run = Mirror(options, fetchers, log)
    for signum in (signal.SIGINT, signal.SIGTERM):
        signal.signal(signum, interrupted)
    try:
        if options.dry_run:
            return run.run(None)
        with tempfile.TemporaryDirectory(prefix="kntnt-mirror-") as staging:
            return run.run(Path(staging))
    except BrowserUnavailable as error:
        print(error)
        return EXIT_REFUSED
    finally:
        session.close()


if __name__ == "__main__":
    sys.exit(main())
