"""The mirror engine, driven against fixture sites a local HTTP server serves.

The engine is run the way its Skill runs it, through `uv run`, which gives it
the dependencies its PEP 723 block pins; the test interpreter has none of them.
Every site is served from `127.0.0.1` on a port the operating system picks, and
`localhost` on the same port stands in for a second host, so no test reaches
the network. A crawl needs three names on that one server, and takes them under
`.localhost`, which resolves to the loopback address: `mirror.localhost` as the
root host, `www.mirror.localhost` as its other form, and `other.mirror.localhost`
as another subdomain. The server answers by the name in the `Host` header.

No test reaches a real browser either: every run finds a stand-in `agent-browser`
first on `PATH`, which records what it was asked and answers from fixtures.
"""

from __future__ import annotations

import base64
import gzip
import hashlib
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, field
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest
from support.fake_binary import fake_binary_on_path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "web" / "mirror"
ENGINE = SKILL / "scripts" / "mirror.py"

IDENTITY = "kntnt-mirror (+https://github.com/Kntnt/skills)"

MANIFEST_FIELDS = {
    "url",
    "final_url",
    "kind",
    "source",
    "discovered_from",
    "fetcher",
    "status",
    "content_type",
    "size",
    "local_path",
    "sha256",
    "etag",
    "last_modified",
    "timestamp",
    "outcome",
    "charset",
    "rung",
    "robots_tag",
}

# The attributes a saved page references another file through.
REFERENCE_ATTRIBUTES = {"href", "src", "srcset", "poster", "data", "action"}

# The well-known locations a run tries at the root of the root's host; `/feed/` is tried under the root too.
PROBED = ("/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml", "/feed/")


@dataclass
class Response:
    """One answer a fixture route gives."""

    body: bytes = b""
    content_type: str = "text/html; charset=utf-8"
    status: int = 200
    headers: dict[str, str] = field(default_factory=dict)


@dataclass
class Request:
    """One request the fixture server received."""

    host: str
    path: str
    headers: dict[str, str]
    time: float = field(default_factory=time.monotonic)


class Site:
    """A fixture site: routes by request path, on one host or all, and what arrived."""

    def __init__(self) -> None:
        self.routes: dict[str, list[Response]] = {}
        self.host_routes: dict[tuple[str, str], list[Response]] = {}
        self.requests: list[Request] = []
        self.port = 0
        # Answers a request before any route does, where it returns a response.
        self.gate: Callable[[Request], Response | None] | None = None

    def add(self, path: str, *responses: Response, host: str | None = None) -> None:
        """Serve *responses* at *path* in turn, the last one from then on.

        Without *host* the route answers on every name; with it, on that name only.
        """

        if host is None:
            self.routes[path] = list(responses)
        else:
            self.host_routes[(host, path)] = list(responses)

    def html(self, path: str, markup: str, host: str | None = None) -> None:
        self.add(path, Response(markup.encode()), host=host)

    def css(self, path: str, text: str) -> None:
        self.add(path, Response(text.encode(), "text/css"))

    def binary(self, path: str, body: bytes, content_type: str = "image/png") -> None:
        self.add(path, Response(body, content_type))

    def url(self, path: str, host: str = "127.0.0.1") -> str:
        return f"http://{host}:{self.port}{path}"

    def requested(self, path: str, host: str = "127.0.0.1") -> list[Request]:
        return [
            request
            for request in self.requests
            if request.path == path and request.host == f"{host}:{self.port}"
        ]

    def tree(self, output: Path, host: str = "127.0.0.1") -> Path:
        """The directory the mirror keeps this site's host in."""

        return output / f"{host}%3A{self.port}"


# The validators a route may carry, and the conditional headers that name them.
VALIDATORS = ("ETag", "Last-Modified")


def not_modified(response: Response, headers: Mapping[str, str]) -> bool:
    """Whether a conditional request matches the route's validators: a `304`.

    `If-None-Match` decides where it is sent, as RFC 9110 says, and
    `If-Modified-Since` only where it is not.
    """

    tag = headers.get("If-None-Match")
    if tag is not None:
        return tag == response.headers.get("ETag")
    since = headers.get("If-Modified-Since")
    return since is not None and since == response.headers.get("Last-Modified")


@pytest.fixture
def site() -> Iterator[Site]:
    """Serve a fresh fixture site for one test, and stop it afterwards."""

    served = Site()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            host = self.headers.get("Host", "")
            request = Request(host, self.path, dict(self.headers))
            served.requests.append(request)
            gated = served.gate(request) if served.gate else None
            if gated is not None:
                self.send_response(gated.status)
                self.send_header("Content-Type", gated.content_type)
                self.send_header("Content-Length", str(len(gated.body)))
                for name, value in gated.headers.items():
                    self.send_header(name, value)
                self.end_headers()
                self.wfile.write(gated.body)
                return
            responses = served.host_routes.get(
                (host.rpartition(":")[0], self.path)
            ) or served.routes.get(self.path)
            if not responses:
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            response = responses.pop(0) if len(responses) > 1 else responses[0]
            if not_modified(response, dict(self.headers)):
                self.send_response(304)
                for name in VALIDATORS:
                    if name in response.headers:
                        self.send_header(name, response.headers[name])
                self.end_headers()
                return
            self.send_response(response.status)
            self.send_header("Content-Type", response.content_type)
            self.send_header("Content-Length", str(len(response.body)))
            for name, value in response.headers.items():
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(response.body)

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    served.port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield served
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


# The stand-in for `agent-browser`. It logs every call, with its arguments and
# what it read on stdin, and answers each subcommand from `fixture.json` beside
# its `bin/`: a page's rendered DOM for `eval`, its HAR for `network har stop`.
# What it was last asked to open is kept in `state.json` between calls.
FAKE_BROWSER = f"""#!{sys.executable}
import base64, json, sys, time
from pathlib import Path

HOME = Path(__file__).resolve().parent.parent
FIXTURE = json.loads((HOME / "fixture.json").read_text())
STATE = HOME / "state.json"
VALUED = {{"--session", "--profile", "--user-agent"}}
BARE = {{"--json", "--headed"}}

# The global flags come first, and the subcommand with its own arguments after them.
arguments = sys.argv[1:]
flags = {{}}
index = 0
while index < len(arguments) and arguments[index] in VALUED | BARE:
    token = arguments[index]
    if token in VALUED:
        flags[token] = arguments[index + 1]
        index += 2
    else:
        flags[token] = True
        index += 1
command = arguments[index:]
stdin = sys.stdin.read() if "--stdin" in command else None
with (HOME / "calls.ndjson").open("a") as log:
    log.write(json.dumps({{"argv": arguments, "flags": flags, "command": command, "stdin": stdin}}) + "\\n")

def answer(data=None, success=True, code=0):
    print(json.dumps({{"success": success, "data": data, "error": None if success else "failed"}}))
    sys.exit(code)

state = json.loads(STATE.read_text()) if STATE.exists() else {{}}
if command[:1] == ["doctor"]:
    code = FIXTURE.get("doctor_exit", 0)
    status = "pass" if code == 0 else "fail"
    print(json.dumps({{"success": code == 0, "checks": [{{"id": "chrome.installed", "status": status}}]}}))
    sys.exit(code)
if command[:1] == ["open"]:
    url = command[1]
    page = FIXTURE.get("pages", {{}}).get(url, {{}})
    state = {{"url": url, "headed": bool(flags.get("--headed")), "scroll": 0}}
    STATE.write_text(json.dumps(state))
    if page.get("hang"):
        time.sleep(120)
    answer({{"url": page.get("final", url), "title": ""}})
page = FIXTURE.get("pages", {{}}).get(state.get("url"), {{}})
headed = state.get("headed") and "headed_dom" in page
if command[:1] == ["scroll"]:
    distance = int(command[2])
    bottom = int(page.get("scroll_bottom", 0))
    if command[1] == "down":
        state["scroll"] = min(int(state.get("scroll", 0)) + distance, bottom)
    else:
        state["scroll"] = max(int(state.get("scroll", 0)) - distance, 0)
    STATE.write_text(json.dumps(state))
    answer({{}})
if command[:1] == ["eval"]:
    if stdin and "window.scrollY" in stdin:
        answer({{"result": {{"top": int(state.get("scroll", 0)), "bottom": int(page.get("scroll_bottom", 0))}}}})
    html = page["headed_dom"] if headed else page.get("dom", "<html><head></head><body></body></html>")
    status = page.get("headed_status" if headed else "status", 404 if not page else 200)
    answer({{"result": {{"url": page.get("final", state.get("url")), "status": status, "doctype": "<!DOCTYPE html>", "html": html}}}})
if command[:3] == ["network", "har", "stop"]:
    entries = page.get("headed_har" if headed else "har")
    if entries is None:
        entries = [{{"url": state.get("url"), "type": "Document", "status": 404, "mime": "text/html", "text": ""}}]
    har = {{"log": {{"version": "1.2", "entries": [
        {{
            "_resourceType": entry["type"],
            "request": {{"method": "GET", "url": entry["url"], "headers": []}},
            "response": {{
                "status": entry["status"],
                "headers": [{{"name": "Content-Type", "value": entry["mime"]}}, *[{{"name": n, "value": v}} for n, v in entry.get("headers", {{}}).items()]],
                "content": {{"mimeType": entry["mime"], **({{"text": entry["base64"], "encoding": "base64"}} if "base64" in entry else {{"text": entry["text"]}} if "text" in entry else {{}})}},
            }},
        }}
        for entry in entries
    ]}}}}
    Path(command[3]).write_text(json.dumps(har))
    answer({{"path": command[3]}})
answer({{}})
"""


@dataclass
class Call:
    """One call the stand-in `agent-browser` received."""

    argv: list[str]
    flags: dict[str, str | bool]
    command: list[str]
    stdin: str | None


@dataclass
class FakeBrowser:
    """A stand-in `agent-browser` on `PATH`: what it answers, and what it was asked."""

    home: Path
    env: dict[str, str]
    fixture: dict[str, object] = field(default_factory=lambda: {"pages": {}})

    @classmethod
    def at(cls, home: Path) -> FakeBrowser:
        home.mkdir(parents=True, exist_ok=True)
        browser = cls(home, fake_binary_on_path(home, "agent-browser", FAKE_BROWSER))
        browser.save()
        return browser

    def save(self) -> None:
        (self.home / "fixture.json").write_text(json.dumps(self.fixture))

    def serve(self, url: str, **page: object) -> None:
        """Answer an `open` of *url* with *page*: `dom`, `status`, `har`, and their headed forms."""

        pages = self.fixture["pages"]
        assert isinstance(pages, dict)
        pages[url] = page
        self.save()

    def lacks_a_browser(self) -> None:
        self.fixture["doctor_exit"] = 1
        self.save()

    def calls(self) -> list[Call]:
        log = self.home / "calls.ndjson"
        if not log.exists():
            return []
        return [
            Call(**json.loads(line)) for line in log.read_text().splitlines() if line
        ]

    def commands(self) -> list[list[str]]:
        return [call.command for call in self.calls()]

    def opened(self) -> list[str]:
        return [command[1] for command in self.commands() if command[:1] == ["open"]]


def har_entry(
    url: str,
    kind: str,
    body: bytes | str,
    mime: str,
    status: int = 200,
    headers: dict[str, str] | None = None,
) -> dict[str, object]:
    """One HAR entry the stand-in records: text as text, bytes base64-encoded."""

    entry: dict[str, object] = {
        "url": url,
        "type": kind,
        "status": status,
        "mime": mime,
        "headers": headers or {},
    }
    if isinstance(body, bytes):
        entry["base64"] = base64.b64encode(body).decode("ascii")
    else:
        entry["text"] = body
    return entry


IDLE_BROWSER: FakeBrowser | None = None


@pytest.fixture(autouse=True, scope="session")
def idle_browser(tmp_path_factory: pytest.TempPathFactory) -> None:
    """A stand-in `agent-browser` for every run a test gives none, so none reaches a real one."""

    global IDLE_BROWSER
    IDLE_BROWSER = FakeBrowser.at(tmp_path_factory.mktemp("idle-browser"))


def mirror(
    cwd: Path, *args: str, browser: FakeBrowser | None = None
) -> subprocess.CompletedProcess[str]:
    """Run the engine as its Skill does, from *cwd*, with a stand-in `agent-browser`."""

    stand_in = browser or IDLE_BROWSER
    assert stand_in is not None
    return subprocess.run(
        ["uv", "run", "--quiet", str(ENGINE), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        timeout=300,
        env={**os.environ, **stand_in.env},
    )


class References(HTMLParser):
    """Every reference a saved page makes, and the elements it keeps."""

    def __init__(self) -> None:
        super().__init__()
        self.references: list[tuple[str, str, str]] = []
        self.tags: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        self.tags.append((tag, attributes))
        for name, value in attrs:
            if value is None:
                continue
            if name in {"srcset", "imagesrcset"}:
                for candidate in value.split(","):
                    self.references.append((tag, name, candidate.split()[0]))
            elif name in REFERENCE_ATTRIBUTES:
                self.references.append((tag, name, value.strip()))
            elif name == "style":
                for target in css_references(value):
                    self.references.append((tag, "style", target))


def css_references(text: str) -> list[str]:
    """Every `url()` and `@import` target a stylesheet names."""

    found = re.findall(r"url\(\s*['\"]?([^'\")]+?)['\"]?\s*\)", text)
    found += re.findall(r"@import\s+['\"]([^'\"]+)['\"]", text)
    return found


def read_page(path: Path) -> References:
    parser = References()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def resolves(document: Path, reference: str) -> Path | None:
    """The file a relative reference leads to from *document*, or None."""

    if urlsplit(reference).scheme or reference.startswith("//"):
        return None
    target = unquote(urlsplit(reference).path)
    return (document.parent / target).resolve()


def manifest(output: Path) -> list[dict[str, object]]:
    lines = (output / ".mirror" / "manifest.ndjson").read_text(encoding="utf-8")
    return [json.loads(line) for line in lines.splitlines() if line]


# A script whose bytes the rewrite never touches, so its integrity holds.
SCRIPT = b"console.log('mirror');\n"
SCRIPT_INTEGRITY = "sha256-" + hashlib.sha256(SCRIPT).hexdigest()


def serve_the_full_page(site: Site) -> None:
    """A page that needs every kind of resource the first acceptance names."""

    site.html(
        "/site/",
        f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>Fixture</title>
<link rel="stylesheet" href="css/main.css" integrity="sha384-stale">
<link rel="icon" href="/site/favicon.ico">
<script src="js/app.js" integrity="{SCRIPT_INTEGRITY}"></script>
</head><body>
<img src="img/small.png" srcset="img/small.png 1x, img/large.png 2x" alt="">
<div style="background-image: url('img/bg.png')"></div>
<a href="/about">About</a>
</body></html>
""",
    )
    site.css(
        "/site/css/main.css",
        '@import url("theme.css");\n'
        "@font-face { font-family: F; src: url(/site/fonts/f.woff2) format('woff2'); }\n"
        "body { font-family: F; }\n",
    )
    site.css("/site/css/theme.css", "h1 { color: red; }\n")
    site.binary("/site/fonts/f.woff2", b"wOF2", "font/woff2")
    site.binary("/site/js/app.js", SCRIPT, "text/javascript")
    site.binary("/site/favicon.ico", b"ico", "image/x-icon")
    site.binary("/site/img/small.png", b"small")
    site.binary("/site/img/large.png", b"large")
    site.binary("/site/img/bg.png", b"bg")
    site.html("/about", "<p>About</p>")


# --- The saved tree ------------------------------------------------------------


def test_every_resource_a_page_needs_is_saved_and_every_reference_resolves(
    site: Site, tmp_path: Path
) -> None:
    serve_the_full_page(site)

    result = mirror(tmp_path, "--output=out", "--browser=never", site.url("/site/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    tree = site.tree(tmp_path / "out")
    expected = [
        "site/index.html",
        "site/css/main.css",
        "site/css/theme.css",
        "site/fonts/f.woff2",
        "site/js/app.js",
        "site/favicon.ico",
        "site/img/small.png",
        "site/img/large.png",
        "site/img/bg.png",
    ]
    for relative in expected:
        assert (tree / relative).is_file(), relative

    page = tree / "site" / "index.html"
    local = [
        reference
        for tag, _, reference in read_page(page).references
        if not (tag == "a" and reference.startswith("http"))
    ]
    assert len(local) == 7, local
    for reference in local:
        target = resolves(page, reference)
        assert target is not None and target.is_file(), reference

    for stylesheet in ("main.css", "theme.css"):
        css = tree / "site" / "css" / stylesheet
        for reference in css_references(css.read_text(encoding="utf-8")):
            target = resolves(css, reference)
            assert target is not None and target.is_file(), reference
    assert len(css_references((tree / "site/css/main.css").read_text())) == 2


def test_the_saved_page_drops_base_and_only_the_integrity_its_rewrite_broke(
    site: Site, tmp_path: Path
) -> None:
    serve_the_full_page(site)
    site.html(
        "/site/",
        (
            '<html><head><base href="/site/"><link rel="stylesheet"'
            ' href="css/main.css" integrity="sha384-stale"><script'
            f' src="js/app.js" integrity="{SCRIPT_INTEGRITY}"></script>'
            "</head><body></body></html>"
        ),
    )

    result = mirror(tmp_path, "--output=out", "--browser=never", site.url("/site/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    tags = read_page(site.tree(tmp_path / "out") / "site" / "index.html").tags
    assert not [tag for tag, _ in tags if tag == "base"]
    link = next(attributes for tag, attributes in tags if tag == "link")
    script = next(attributes for tag, attributes in tags if tag == "script")
    assert "integrity" not in link
    assert script["integrity"] == SCRIPT_INTEGRITY


def test_a_local_resource_drops_crossorigin(site: Site, tmp_path: Path) -> None:
    site.html(
        "/media/",
        '<video crossorigin="anonymous" src="movie.mp4"></video>',
    )
    site.binary("/media/movie.mp4", b"video", "video/mp4")

    result = mirror(
        tmp_path,
        "--output=out",
        "--browser=never",
        "--no-sitemap",
        "--no-feeds",
        site.url("/media/"),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    page = site.tree(tmp_path / "out") / "media" / "index.html"
    video = next(
        attributes for tag, attributes in read_page(page).tags if tag == "video"
    )
    assert "crossorigin" not in video


def test_a_base_element_is_honoured_before_it_is_removed(
    site: Site, tmp_path: Path
) -> None:
    site.html(
        "/b/", '<html><head><base href="/b/sub/"></head><img src="pic.png"></html>'
    )
    site.binary("/b/sub/pic.png", b"pic")

    result = mirror(tmp_path, "--output=out", site.url("/b/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert site.requested("/b/sub/pic.png")
    assert not site.requested("/b/pic.png")
    page = site.tree(tmp_path / "out") / "b" / "index.html"
    [(_, _, reference)] = read_page(page).references
    target = resolves(page, reference)
    assert target is not None and target.read_bytes() == b"pic"


def test_a_resource_on_a_second_host_follows_the_resources_flag(
    site: Site, tmp_path: Path
) -> None:
    site.html(
        "/p/",
        (
            f'<img src="{site.url("/cdn/logo.png", host="localhost")}">'
            '<img src="here.png"><img src="/elsewhere/x.png">'
        ),
    )
    site.binary("/cdn/logo.png", b"logo")
    site.binary("/p/here.png", b"here")
    site.binary("/elsewhere/x.png", b"x")
    logo = site.url("/cdn/logo.png", host="localhost")

    everything = tmp_path / "all"
    everything.mkdir()
    result = mirror(everything, "--output=out", site.url("/p/"))
    assert result.returncode == 0, (result.stdout, result.stderr)
    saved = site.tree(everything / "out", host="localhost") / "cdn" / "logo.png"
    assert saved.read_bytes() == b"logo"
    page = site.tree(everything / "out") / "p" / "index.html"
    for _, _, reference in read_page(page).references:
        target = resolves(page, reference)
        assert target is not None and target.is_file(), reference

    site.requests.clear()
    in_scope = tmp_path / "in-scope"
    in_scope.mkdir()
    result = mirror(in_scope, "--output=out", "--resources=in-scope", site.url("/p/"))
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert not site.requested("/cdn/logo.png", host="localhost")
    assert not site.requested("/elsewhere/x.png")
    assert site.requested("/p/here.png")
    assert not (in_scope / "out" / f"localhost%3A{site.port}").exists()
    page = site.tree(in_scope / "out") / "p" / "index.html"
    references = [reference for _, _, reference in read_page(page).references]
    assert logo in references
    assert site.url("/elsewhere/x.png") in references

    site.requests.clear()
    nothing = tmp_path / "none"
    nothing.mkdir()
    result = mirror(nothing, "--output=out", "--resources=none", site.url("/p/"))
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert [request.path for request in site.requests] == [
        "/robots.txt",
        "/p/",
        *PROBED,
        "/p/feed/",
    ]
    page = site.tree(nothing / "out") / "p" / "index.html"
    references = [reference for _, _, reference in read_page(page).references]
    assert references == [logo, site.url("/p/here.png"), site.url("/elsewhere/x.png")]


def test_a_link_to_a_page_outside_the_mirror_stays_absolute(
    site: Site, tmp_path: Path
) -> None:
    serve_the_full_page(site)

    result = mirror(tmp_path, "--output=out", "--browser=never", site.url("/site/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    page = site.tree(tmp_path / "out") / "site" / "index.html"
    anchors = [ref for tag, _, ref in read_page(page).references if tag == "a"]
    assert anchors == [site.url("/about")]
    assert not site.requested("/about")


def test_file_names_follow_the_mapping_the_manpage_states(
    site: Site, tmp_path: Path
) -> None:
    site.html(
        "/docs/guide",
        (
            '<link rel="stylesheet" href="style.css?v=2">'
            '<iframe src="/docs/"></iframe>'
            '<object data="data"></object><img src="data/x.png">'
        ),
    )
    site.css("/docs/style.css?v=2", "p { margin: 0; }")
    site.html("/docs/", "<p>index</p>")
    site.binary("/docs/data", b"blob", "application/octet-stream")
    site.binary("/docs/data/x.png", b"x")

    result = mirror(tmp_path, "--output=out", site.url("/docs/guide"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    docs = site.tree(tmp_path / "out") / "docs"
    assert (docs / "guide.html").is_file()
    assert (docs / "index.html").read_text(encoding="utf-8").count("index") == 1
    assert (docs / "style%3Fv=2.css").is_file()
    assert (docs / "data~file").read_bytes() == b"blob"
    assert (docs / "data" / "x.png").read_bytes() == b"x"
    page = docs / "guide.html"
    for _, _, reference in read_page(page).references:
        target = resolves(page, reference)
        assert target is not None and target.is_file(), reference

    help_page = (SKILL / "help.md").read_text(encoding="utf-8")
    files = help_page.partition("\n## FILES\n")[2].partition("\n## ")[0]
    for statement in ("index.html", ".html", "~file", "%3F", "manifest.ndjson"):
        assert statement in files, statement


def test_long_url_components_are_bounded_and_collision_resistant(
    site: Site, tmp_path: Path
) -> None:
    first = "/long/asset?payload=" + "x" * 1000
    second = "/long/asset?payload=" + "y" * 1000
    site.html("/long/", f'<img src="{first}"><img src="{second}">')
    site.binary(first, b"first")
    site.binary(second, b"second")

    result = mirror(
        tmp_path,
        "--output=out",
        "--browser=never",
        "--no-sitemap",
        "--no-feeds",
        site.url("/long/"),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    rows = [
        row
        for row in manifest(tmp_path / "out")
        if str(row["url"]).startswith(site.url("/long/asset"))
    ]
    paths = [Path(str(row["local_path"])) for row in rows]
    assert len(paths) == 2 and paths[0] != paths[1]
    assert all(
        len(component.encode("utf-8")) <= 240
        for path in paths
        for component in path.parts
    )


def test_html_and_css_keep_their_bytes_as_served_and_nothing_else_does(
    site: Site, tmp_path: Path
) -> None:
    serve_the_full_page(site)

    result = mirror(tmp_path, "--output=out", "--browser=never", site.url("/site/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    output = tmp_path / "out"
    host = site.tree(output).name
    raw = output / ".mirror" / "raw" / host / "site"
    for relative, route in (
        ("index.html", "/site/"),
        ("css/main.css", "/site/css/main.css"),
        ("css/theme.css", "/site/css/theme.css"),
    ):
        assert (raw / relative).read_bytes() == site.routes[route][0].body, relative
    assert (site.tree(output) / "site/css/main.css").read_bytes() != (
        raw / "css/main.css"
    ).read_bytes()
    for relative in ("img/small.png", "fonts/f.woff2", "js/app.js"):
        assert not (raw / relative).exists(), relative


# --- Manifest, log and dry run -------------------------------------------------


def test_the_manifest_has_one_row_per_url_with_every_field(
    site: Site, tmp_path: Path
) -> None:
    serve_the_full_page(site)
    site.html(
        "/site/",
        (
            '<img src="img/small.png"><img src="img/missing.png">'
            f'<img src="{site.url("/x.png", host="localhost")}">'
        ),
    )

    result = mirror(
        tmp_path, "--output=out", "--resources=in-scope", site.url("/site/")
    )

    assert result.returncode == 1, (result.stdout, result.stderr)
    rows = manifest(tmp_path / "out")
    for row in rows:
        assert set(row) == MANIFEST_FIELDS, row
    by_url = {row["url"]: row for row in rows}
    assert len(by_url) == len(rows) == 10
    for path in (*PROBED, "/site/feed/"):
        probe = by_url[site.url(path)]
        assert (probe["kind"], probe["source"], probe["outcome"]) == (
            "feed" if "feed" in path else "sitemap",
            "probe",
            "missing",
        ), path

    start = by_url[site.url("/site/")]
    assert (start["kind"], start["source"], start["outcome"]) == (
        "page",
        "start",
        "fetched",
    )
    assert start["fetcher"] == "http" and start["status"] == 200
    assert start["rung"] == 1
    for row in rows:
        requested = row["status"] is not None
        assert (row["fetcher"], row["rung"]) == (
            ("http", 1) if requested else (None, None)
        ), row
    assert start["local_path"] == f"{site.tree(Path('.')).name}/site/index.html"
    assert start["discovered_from"] is None

    image = by_url[site.url("/site/img/small.png")]
    assert (image["kind"], image["source"]) == ("resource", "resource")
    assert image["discovered_from"] == site.url("/site/")
    assert image["size"] == 5
    assert image["sha256"] == hashlib.sha256(b"small").hexdigest()
    assert image["content_type"] == "image/png"

    missing = by_url[site.url("/site/img/missing.png")]
    assert (missing["outcome"], missing["status"]) == ("failed", 404)
    outside = by_url[site.url("/x.png", host="localhost")]
    assert outside["outcome"] == "out-of-scope"
    robots = by_url[site.url("/robots.txt")]
    assert (robots["kind"], robots["status"], robots["local_path"]) == (
        "robots",
        404,
        None,
    )

    log = (tmp_path / "out" / ".mirror" / "run.log").read_text(encoding="utf-8")
    assert re.search(rf"GET {re.escape(site.url('/site/'))} 200 ", log)
    assert "out-of-scope" in log


def test_a_dry_run_writes_nothing_and_reports_what_a_real_run_would(
    site: Site, tmp_path: Path
) -> None:
    serve_the_full_page(site)

    dry = mirror(tmp_path, "--dry-run", "--browser=never", site.url("/site/"))

    assert dry.returncode == 0, (dry.stdout, dry.stderr)
    assert list(tmp_path.iterdir()) == []
    for path in ("/site/", "/site/css/theme.css", "/site/img/bg.png"):
        assert site.url(path) in dry.stdout, path

    real = mirror(tmp_path, "--browser=never", site.url("/site/"))

    assert real.returncode == 0, (real.stdout, real.stderr)
    assert (tmp_path / "127.0.0.1").is_dir()

    def counts(text: str) -> list[str]:
        return re.findall(r"^(?:Pages|Resources|Total).*$", text, re.MULTILINE)

    assert counts(dry.stdout) and counts(dry.stdout) == counts(real.stdout)


# --- Requests -----------------------------------------------------------------


def test_every_request_carries_the_identity_and_every_header(
    site: Site, tmp_path: Path
) -> None:
    serve_the_full_page(site)

    result = mirror(tmp_path, "--output=a", "--browser=never", site.url("/site/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert len(site.requests) == 15
    assert {request.headers["User-Agent"] for request in site.requests} == {IDENTITY}

    site.requests.clear()
    result = mirror(
        tmp_path,
        "--output=b",
        "--header=X-Token: secret",
        "--header=Cookie: session=1",
        "--user-agent=fixture-bot/2",
        "--browser=never",
        site.url("/site/"),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert len(site.requests) == 15
    for request in site.requests:
        assert request.headers["User-Agent"] == "fixture-bot/2"
        assert request.headers["X-Token"] == "secret"
        assert request.headers["Cookie"] == "session=1"


def test_every_header_survives_every_redirect_and_retry(
    site: Site, tmp_path: Path
) -> None:
    other = site.url("/elsewhere/logo.png", host="localhost")
    site.add(
        "/start",
        Response(
            b"",
            status=302,
            headers={"Location": "/h/", "Set-Cookie": "tracker=server"},
        ),
    )
    site.html("/h/", '<img src="moved.png"><img src="away.png"><img src="busy.png">')
    site.add("/h/moved.png", Response(b"", status=301, headers={"Location": "a.png"}))
    site.binary("/h/a.png", b"a")
    site.add("/h/away.png", Response(b"", status=307, headers={"Location": other}))
    site.binary("/elsewhere/logo.png", b"logo")
    site.add(
        "/h/busy.png",
        Response(b"", status=302, headers={"Location": "/h/b.png"}),
    )
    site.add(
        "/h/b.png",
        Response(b"", status=503, headers={"Retry-After": "0"}),
        Response(b"b", "image/png"),
    )

    result = mirror(
        tmp_path,
        "--output=out",
        "--header=Cookie: session=1",
        "--header=Authorization: Bearer secret",
        "--header=X-Token: secret",
        "--user-agent=fixture-bot/2",
        "--no-sitemap",
        "--no-feeds",
        site.url("/start"),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    paths = {(request.host.split(":")[0], request.path) for request in site.requests}
    assert paths == {
        ("127.0.0.1", "/robots.txt"),
        ("127.0.0.1", "/start"),
        ("127.0.0.1", "/h/"),
        ("127.0.0.1", "/h/moved.png"),
        ("127.0.0.1", "/h/a.png"),
        ("127.0.0.1", "/h/away.png"),
        ("localhost", "/elsewhere/logo.png"),
        ("127.0.0.1", "/h/busy.png"),
        ("127.0.0.1", "/h/b.png"),
    }
    for request in site.requests:
        assert request.headers.get("User-Agent") == "fixture-bot/2", request
        assert request.headers.get("Cookie") == "session=1", request
        assert request.headers.get("Authorization") == "Bearer secret", request
        assert request.headers.get("X-Token") == "secret", request


def test_a_busy_answer_is_retried_and_a_missing_one_is_not(
    site: Site, tmp_path: Path
) -> None:
    site.html("/r/", '<img src="busy.png"><img src="gone.png">')
    site.add(
        "/r/busy.png",
        Response(b"", status=503, headers={"Retry-After": "0"}),
        Response(b"busy", "image/png"),
    )

    result = mirror(tmp_path, "--output=out", site.url("/r/"))

    assert result.returncode == 1, (result.stdout, result.stderr)
    assert len(site.requested("/r/busy.png")) == 2
    assert len(site.requested("/r/gone.png")) == 1
    assert (site.tree(tmp_path / "out") / "r" / "busy.png").read_bytes() == b"busy"


def test_equal_urls_are_fetched_once(site: Site, tmp_path: Path) -> None:
    site.html(
        "/n/",
        (
            '<img src="img/a.png?utm_source=x&amp;fbclid=1">'
            '<img src="./img/../img/a.png#top"><img src="%69mg/a.png">'
            '<iframe src="index.html"></iframe>'
        ),
    )
    site.binary("/n/img/a.png", b"a")

    result = mirror(
        tmp_path, "--output=out", "--no-sitemap", "--no-feeds", site.url("/n/")
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert [request.path for request in site.requests] == [
        "/robots.txt",
        "/n/",
        "/n/img/a.png",
    ]
    page = site.tree(tmp_path / "out") / "n" / "index.html"
    for _, _, reference in read_page(page).references:
        target = resolves(page, reference)
        assert target is not None and target.is_file(), reference


def test_the_start_page_is_where_redirects_end_and_its_directory_is_the_root(
    site: Site, tmp_path: Path
) -> None:
    site.add(
        "/old",
        Response(b"", status=301, headers={"Location": "/blog/post"}),
    )
    site.html("/blog/post", '<img src="img.png"><img src="/assets/x.png">')
    site.binary("/blog/img.png", b"img")
    site.binary("/assets/x.png", b"x")

    result = mirror(tmp_path, "--output=out", "--resources=in-scope", site.url("/old"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    blog = site.tree(tmp_path / "out") / "blog"
    assert (blog / "post.html").is_file()
    assert (blog / "img.png").is_file()
    assert not site.requested("/assets/x.png")
    [start] = [row for row in manifest(tmp_path / "out") if row["source"] == "start"]
    assert (start["url"], start["final_url"]) == (
        site.url("/old"),
        site.url("/blog/post"),
    )


# --- Exit status and report ---------------------------------------------------


def test_a_clean_run_exits_zero_and_reports_what_it_fetched(
    site: Site, tmp_path: Path
) -> None:
    serve_the_full_page(site)

    result = mirror(tmp_path, "--output=out", "--browser=never", site.url("/site/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert re.search(r"^Pages fetched: 1$", result.stdout, re.MULTILINE)
    assert re.search(r"^Resources fetched: 8$", result.stdout, re.MULTILINE)
    assert re.search(r"^Total size: ", result.stdout, re.MULTILINE)


def test_a_resource_that_answers_404_exits_one_and_is_named_in_the_report(
    site: Site, tmp_path: Path
) -> None:
    site.html("/f/", '<img src="gone.png">')

    result = mirror(tmp_path, "--output=out", site.url("/f/"))

    assert result.returncode == 1, (result.stdout, result.stderr)
    assert re.search(
        rf"^\s*404 {re.escape(site.url('/f/gone.png'))}$", result.stdout, re.MULTILINE
    )


def test_a_start_page_that_cannot_be_fetched_exits_one_and_writes_nothing(
    site: Site, tmp_path: Path
) -> None:
    result = mirror(tmp_path, "--output=out", site.url("/nowhere/"))

    assert result.returncode == 1, (result.stdout, result.stderr)
    assert "404" in result.stdout
    assert not (tmp_path / "out").exists()


@pytest.mark.parametrize(
    "arguments",
    [
        ("ftp://example.com/",),
        ("example.com/page",),
        ("--resources=some", "http://example.com/"),
        ("--header=no-colon", "http://example.com/"),
        ("--delay=soon", "http://example.com/"),
        ("--delay=-1", "http://example.com/"),
        ("--max-pages=two", "http://example.com/"),
        ("--max-pages=-3", "http://example.com/"),
        ("--browser=maybe", "http://example.com/"),
    ],
)
def test_a_value_the_skill_rejects_is_refused_in_the_collections_shape(
    tmp_path: Path, arguments: tuple[str, ...]
) -> None:
    result = mirror(tmp_path, *arguments)

    assert result.returncode == 2, (result.stdout, result.stderr)
    synopsis = (SKILL / "help.md").read_text(encoding="utf-8")
    synopsis = synopsis.partition("\n## SYNOPSIS\n")[2].partition("\n## ")[0].strip()
    assert synopsis in result.stdout
    assert result.stdout.rstrip("\n").endswith("see '/mirror --help'")
    assert list(tmp_path.iterdir()) == []


def test_the_skill_reads_the_saved_urls_relative_to_the_page(tmp_path: Path) -> None:
    """A guard on the helper the other tests lean on, so a green run means something."""

    page = tmp_path / "a" / "index.html"
    page.parent.mkdir()
    page.write_text("", encoding="utf-8")
    (tmp_path / "b%3Fx.css").write_text("", encoding="utf-8")

    assert resolves(page, "http://example.com/") is None
    assert resolves(page, "../b%253Fx.css") == (tmp_path / "b%3Fx.css").resolve()


# --- The crawl ----------------------------------------------------------------

ROOT_HOST = "mirror.localhost"
WWW_HOST = "www.mirror.localhost"
OTHER_HOST = "other.mirror.localhost"


def links_from(page: Path) -> list[str]:
    """Every `a`, `area` and `link` reference a saved page makes."""

    return [
        reference
        for tag, name, reference in read_page(page).references
        if tag in {"a", "area", "link"} and name == "href"
    ]


def page_times(site: Site, paths: list[str]) -> list[float]:
    return [site.requested(path, host=ROOT_HOST)[0].time for path in paths]


def serve_the_docs_site(site: Site) -> None:
    """A root `/docs/` whose links reach every case the first criterion names."""

    site.html(
        "/docs/",
        f"""<html><head><link rel="next" href="sub/"></head><body>
<a href="guide">Guide</a>
<a href="manual.pdf">Manual</a>
<a href="/about/">About</a>
<a href="{site.url("/docs/elsewhere", host=OTHER_HOST)}">Other subdomain</a>
<a href="{site.url("/docs/www-page", host=WWW_HOST)}">Through www</a>
<a href="guide#intro">Guide, intro</a>
<a href="guide?utm_source=news">Guide, tracked</a>
<map><area href="moved" alt="Moved"></map>
</body></html>""",
        host=ROOT_HOST,
    )
    site.html(
        "/docs/guide",
        '<a href="/docs/">Up</a><a href="sub/deep">Deep</a><img src="img/fig.png">',
        host=ROOT_HOST,
    )
    site.binary("/docs/img/fig.png", b"fig")
    site.html("/docs/sub/", '<a href="deep">Deep</a>', host=ROOT_HOST)
    site.html("/docs/sub/deep", '<a href="../guide">Guide</a>', host=ROOT_HOST)
    site.html("/docs/www-page", '<a href="guide">Guide</a>', host=ROOT_HOST)
    site.html("/docs/www-page", "<p>served through www</p>", host=WWW_HOST)
    site.add("/docs/manual.pdf", Response(b"%PDF-1.4", "application/pdf"))
    site.add(
        "/docs/moved",
        Response(
            b"", status=301, headers={"Location": site.url("/about/", host=ROOT_HOST)}
        ),
    )
    site.html("/about/", "<p>About</p>")
    site.html("/docs/elsewhere", "<p>Elsewhere</p>", host=OTHER_HOST)


def test_a_crawl_saves_every_page_under_the_root_once_and_nothing_outside_it(
    site: Site, tmp_path: Path
) -> None:
    serve_the_docs_site(site)

    result = mirror(tmp_path, "--output=out", site.url("/docs/", host=ROOT_HOST))

    assert result.returncode == 0, (result.stdout, result.stderr)
    output = tmp_path / "out"
    tree = site.tree(output, host=ROOT_HOST)
    saved = {
        "/docs/": "docs/index.html",
        "/docs/guide": "docs/guide.html",
        "/docs/manual.pdf": "docs/manual.pdf",
        "/docs/sub/": "docs/sub/index.html",
        "/docs/sub/deep": "docs/sub/deep.html",
        "/docs/www-page": "docs/www-page.html",
    }
    for path, relative in saved.items():
        assert (tree / relative).is_file(), relative
        assert len(site.requested(path, host=ROOT_HOST)) == 1, path
    assert (tree / "docs/www-page.html").read_text().count("served through www") == 0

    # Nothing from above the root, from another subdomain, or the www form.
    assert not site.requested("/about/", host=ROOT_HOST)
    assert not [r for r in site.requests if r.host.startswith(OTHER_HOST)]
    assert not [r for r in site.requests if r.host.startswith(WWW_HOST)]
    assert sorted(child.name for child in output.iterdir()) == sorted(
        [".mirror", tree.name]
    )

    rows = manifest(output)
    by_url = {row["url"]: row for row in rows}
    assert len(by_url) == len(rows)
    assert by_url[site.url("/about/", host=ROOT_HOST)]["outcome"] == "out-of-scope"
    assert (
        by_url[site.url("/docs/elsewhere", host=OTHER_HOST)]["outcome"]
        == "out-of-scope"
    )
    moved = by_url[site.url("/docs/moved", host=ROOT_HOST)]
    assert (moved["outcome"], moved["status"], moved["local_path"]) == (
        "redirect-out",
        301,
        None,
    )
    www_rows = [row for row in rows if "www-page" in str(row["url"])]
    assert [row["url"] for row in www_rows] == [
        site.url("/docs/www-page", host=ROOT_HOST)
    ]
    assert not [row for row in rows if WWW_HOST in str(row["url"])]
    assert not [
        row for row in rows if "#" in str(row["url"]) or "utm_" in str(row["url"])
    ]
    pdf = by_url[site.url("/docs/manual.pdf", host=ROOT_HOST)]
    assert (pdf["kind"], pdf["source"], pdf["outcome"]) == ("file", "link", "fetched")
    assert pdf["discovered_from"] == site.url("/docs/", host=ROOT_HOST)
    guide = by_url[site.url("/docs/guide", host=ROOT_HOST)]
    assert (guide["kind"], guide["source"]) == ("page", "link")
    figure = by_url[site.url("/docs/img/fig.png", host=ROOT_HOST)]
    assert (figure["kind"], figure["source"]) == ("resource", "resource")
    assert figure["discovered_from"] == site.url("/docs/guide", host=ROOT_HOST)

    assert re.search(r"^Pages fetched: 5$", result.stdout, re.MULTILINE)
    assert re.search(r"^Files fetched: 1$", result.stdout, re.MULTILINE)
    assert re.search(r"^Resources fetched: 1$", result.stdout, re.MULTILINE)
    assert re.search(r"^Out of scope: 2$", result.stdout, re.MULTILINE)


def test_links_between_saved_pages_are_relative_and_links_out_stay_absolute(
    site: Site, tmp_path: Path
) -> None:
    serve_the_docs_site(site)

    result = mirror(tmp_path, "--output=out", site.url("/docs/", host=ROOT_HOST))

    assert result.returncode == 0, (result.stdout, result.stderr)
    tree = site.tree(tmp_path / "out", host=ROOT_HOST)
    outside = {
        site.url("/about/", host=ROOT_HOST),
        site.url("/docs/elsewhere", host=OTHER_HOST),
        site.url("/docs/moved", host=ROOT_HOST),
    }
    internal = 0
    for page in tree.rglob("*.html"):
        for reference in links_from(page):
            if reference in outside:
                continue
            assert not urlsplit(reference).scheme, (page, reference)
            target = resolves(page, reference)
            assert target is not None and target.is_file(), (page, reference)
            internal += 1
    assert internal >= 10
    start = links_from(tree / "docs" / "index.html")
    assert site.url("/about/", host=ROOT_HOST) in start
    assert site.url("/docs/elsewhere", host=OTHER_HOST) in start


def test_no_links_saves_the_start_page_and_its_resources_only(
    site: Site, tmp_path: Path
) -> None:
    site.html("/n/", '<img src="pic.png"><a href="next">Next</a>')
    site.binary("/n/pic.png", b"pic")
    site.html("/n/next", "<p>next</p>")

    result = mirror(tmp_path, "--output=out", "--no-links", site.url("/n/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert not site.requested("/n/next")
    tree = site.tree(tmp_path / "out")
    assert sorted(
        str(path.relative_to(tree)) for path in tree.rglob("*") if path.is_file()
    ) == ["n/index.html", "n/pic.png"]
    [(_, _, image), (_, _, anchor)] = read_page(tree / "n" / "index.html").references
    assert anchor == site.url("/n/next")
    target = resolves(tree / "n" / "index.html", image)
    assert target is not None and target.is_file()


def test_the_page_cap_stops_discovery_and_the_report_says_so(
    site: Site, tmp_path: Path
) -> None:
    site.html("/m/", '<a href="a">A</a><a href="b">B</a><a href="c">C</a>')
    site.html("/m/a", '<img src="a.png">')
    site.binary("/m/a.png", b"a")
    site.html("/m/b", "<p>b</p>")
    site.html("/m/c", "<p>c</p>")

    result = mirror(tmp_path, "--output=out", "--max-pages=2", site.url("/m/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert site.requested("/m/a") and site.requested("/m/a.png")
    assert not site.requested("/m/b") and not site.requested("/m/c")
    assert re.search(r"^Pages fetched: 2$", result.stdout, re.MULTILINE)
    assert re.search(r"^Over the cap: 2$", result.stdout, re.MULTILINE)
    assert re.search(r"cap of 2\b.*reached", result.stdout)
    outcomes = {row["url"]: row["outcome"] for row in manifest(tmp_path / "out")}
    assert outcomes[site.url("/m/b")] == outcomes[site.url("/m/c")] == "over-cap"


def test_robots_txt_keeps_a_disallowed_page_out_unless_it_is_ignored(
    site: Site, tmp_path: Path
) -> None:
    site.add(
        "/robots.txt",
        Response(
            b"User-agent: *\nDisallow: /docs/private/\n\nSitemap: /sitemap.xml\n",
            "text/plain",
        ),
    )
    site.html(
        "/docs/",
        '<a href="private/secret">Secret</a><a href="open">Open</a>'
        '<img src="private/pic.png">',
    )
    site.html("/docs/private/secret", "<p>secret</p>")
    site.html("/docs/open", "<p>open</p>")
    site.binary("/docs/private/pic.png", b"pic")

    obeyed = tmp_path / "obeyed"
    obeyed.mkdir()
    result = mirror(obeyed, "--output=out", site.url("/docs/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert not site.requested("/docs/private/secret")
    assert site.requested("/docs/open")
    assert site.requested("/docs/private/pic.png"), "resources are exempt"
    assert len(site.requested("/robots.txt")) == 1
    assert re.search(r"^Stopped by robots\.txt: 1$", result.stdout, re.MULTILINE)
    rows = {row["url"]: row for row in manifest(obeyed / "out")}
    assert rows[site.url("/docs/private/secret")]["outcome"] == "robots"
    assert rows[site.url("/robots.txt")]["kind"] == "robots"
    assert not list((obeyed / "out").rglob("robots.txt"))

    site.requests.clear()
    ignored = tmp_path / "ignored"
    ignored.mkdir()
    result = mirror(ignored, "--output=out", "--ignore-robots", site.url("/docs/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert site.requested("/robots.txt"), "the file is still read"
    assert site.requested("/docs/private/secret")
    assert re.search(r"^Stopped by robots\.txt: 0$", result.stdout, re.MULTILINE)


def test_robots_txt_applies_the_group_for_the_runs_own_token_before_the_star(
    site: Site, tmp_path: Path
) -> None:
    site.add(
        "/robots.txt",
        Response(
            b"User-agent: *\nDisallow: /docs/public/\n\n"
            b"User-agent: KNTNT-Mirror\nDisallow: /docs/private/\n",
            "text/plain",
        ),
    )
    site.html("/docs/", '<a href="private/">P</a><a href="public/">Q</a>')
    site.html("/docs/private/", "<p>private</p>")
    site.html("/docs/public/", "<p>public</p>")

    own = tmp_path / "own"
    own.mkdir()
    result = mirror(own, "--output=out", site.url("/docs/"))
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert site.requested("/docs/public/")
    assert not site.requested("/docs/private/")

    site.requests.clear()
    other = tmp_path / "other"
    other.mkdir()
    result = mirror(
        other, "--output=out", "--user-agent=fixture-bot/2 (x)", site.url("/docs/")
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert site.requested("/docs/private/")
    assert not site.requested("/docs/public/")


def test_a_nofollow_robots_tag_keeps_a_pages_links_unfollowed_unless_robots_are_ignored(
    site: Site, tmp_path: Path
) -> None:
    site.html(
        "/docs/",
        '<a href="meta">Meta</a><a href="token">Token</a><a href="other">Other</a>'
        '<a href="header">Header</a><a href="theirs">Theirs</a>',
    )
    site.html(
        "/docs/meta",
        '<meta name="robots" content="noindex, NoFollow">'
        '<a href="from-meta">On</a><img src="meta.png">',
    )
    site.html(
        "/docs/token",
        '<meta name="kntnt-mirror" content="none"><a href="from-token">On</a>',
    )
    site.html(
        "/docs/other",
        '<meta name="googlebot" content="nofollow"><a href="from-other">On</a>',
    )
    site.add(
        "/docs/header",
        Response(
            b'<a href="from-header">On</a>',
            headers={"X-Robots-Tag": "noarchive, nofollow"},
        ),
    )
    site.add(
        "/docs/theirs",
        Response(
            b'<a href="from-theirs">On</a>',
            headers={"X-Robots-Tag": "googlebot: nofollow"},
        ),
    )
    for path in ("from-meta", "from-token", "from-other", "from-header", "from-theirs"):
        site.html(f"/docs/{path}", "<p>on</p>")
    site.binary("/docs/meta.png", b"png")

    obeyed = tmp_path / "obeyed"
    obeyed.mkdir()
    result = mirror(obeyed, "--output=out", site.url("/docs/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    for page in ("meta", "token", "header"):
        assert site.requested(f"/docs/{page}"), (
            f"a nofollow page is still saved: {page}"
        )
        assert not site.requested(f"/docs/from-{page}"), page
    assert site.requested("/docs/meta.png"), "resources are exempt"
    assert site.requested("/docs/from-other"), (
        "a tag for another crawler binds nobody here"
    )
    assert site.requested("/docs/from-theirs"), "so does a header for another crawler"
    assert count(result.stdout, "Pages whose links nofollow stopped") == 3
    rows = {row["url"]: row for row in manifest(obeyed / "out")}
    assert rows[site.url("/docs/header")]["robots_tag"] == ["noarchive, nofollow"]
    assert rows[site.url("/docs/meta")]["robots_tag"] is None

    site.requests.clear()
    ignored = tmp_path / "ignored"
    ignored.mkdir()
    result = mirror(ignored, "--output=out", "--ignore-robots", site.url("/docs/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    for page in ("meta", "token", "header"):
        assert site.requested(f"/docs/from-{page}"), page
    assert count(result.stdout, "Pages whose links nofollow stopped") == 0


def test_a_nofollow_header_still_binds_a_page_a_rerun_finds_unchanged(
    site: Site, tmp_path: Path
) -> None:
    site.html("/docs/", '<a href="header">Header</a>')
    site.add(
        "/docs/header",
        Response(
            b'<a href="beyond">On</a>',
            headers={"X-Robots-Tag": "nofollow", "ETag": '"h1"'},
        ),
    )
    site.html("/docs/beyond", "<p>on</p>")

    first = mirror(tmp_path, "--output=out", site.url("/docs/"))
    assert first.returncode == 0, (first.stdout, first.stderr)
    site.requests.clear()
    second = mirror(tmp_path, "--output=out", site.url("/docs/"))

    assert second.returncode == 0, (second.stdout, second.stderr)
    [request] = site.requested("/docs/header")
    assert request.headers["If-None-Match"] == '"h1"'
    rows = {row["url"]: row for row in manifest(tmp_path / "out")}
    assert rows[site.url("/docs/header")]["outcome"] == "unchanged"
    assert rows[site.url("/docs/header")]["robots_tag"] == ["nofollow"]
    assert not site.requested("/docs/beyond"), "the 304 carries no X-Robots-Tag"


def test_an_unreadable_robots_txt_allows_everything_and_is_reported(
    site: Site, tmp_path: Path
) -> None:
    site.add("/robots.txt", Response(b"", status=503, headers={"Retry-After": "0"}))
    site.html("/u/", '<a href="next">Next</a>')
    site.html("/u/next", "<p>next</p>")

    result = mirror(tmp_path, "--output=out", "--browser=never", site.url("/u/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert site.requested("/u/next")
    assert re.search(r"robots\.txt.*could not be read", result.stdout)


def test_a_delay_spaces_the_requests(site: Site, tmp_path: Path) -> None:
    site.html("/d/", '<a href="a">A</a><a href="b">B</a>', host=ROOT_HOST)
    site.html("/d/a", "<p>a</p>", host=ROOT_HOST)
    site.html("/d/b", "<p>b</p>", host=ROOT_HOST)

    result = mirror(
        tmp_path, "--output=out", "--delay=1", site.url("/d/", host=ROOT_HOST)
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    first, _, last = page_times(site, ["/d/", "/d/a", "/d/b"])
    assert last - first >= 2.0


def test_a_crawl_delay_longer_than_the_delay_is_honoured(
    site: Site, tmp_path: Path
) -> None:
    site.add(
        "/robots.txt",
        Response(b"User-agent: *\nCrawl-delay: 1\n", "text/plain"),
        host=ROOT_HOST,
    )
    site.html("/d/", '<a href="a">A</a>', host=ROOT_HOST)
    site.html("/d/a", "<p>a</p>", host=ROOT_HOST)

    result = mirror(tmp_path, "--output=out", site.url("/d/", host=ROOT_HOST))

    assert result.returncode == 0, (result.stdout, result.stderr)
    first, last = page_times(site, ["/d/", "/d/a"])
    assert last - first >= 1.0


def folds_case(directory: Path) -> bool:
    """Whether the file system under *directory* treats names differing in case as one."""

    handle, name = tempfile.mkstemp(prefix="probe-", dir=directory)
    os.close(handle)
    probe = Path(name)
    try:
        return (probe.parent / probe.name.swapcase()).exists()
    finally:
        probe.unlink()


def test_urls_differing_only_in_case_are_both_saved(site: Site, tmp_path: Path) -> None:
    site.html("/c/", '<a href="Page">Upper</a><a href="page">Lower</a>')
    site.html("/c/Page", "<p>upper</p>")
    site.html("/c/page", "<p>lower</p>")

    result = mirror(tmp_path, "--output=out", site.url("/c/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    tree = site.tree(tmp_path / "out")
    paths = {row["url"]: row["local_path"] for row in manifest(tmp_path / "out")}
    upper = paths[site.url("/c/Page")]
    lower = paths[site.url("/c/page")]
    assert upper == f"{tree.name}/c/Page.html"
    if folds_case(tmp_path):
        assert lower == f"{tree.name}/c/page~2.html"
    else:
        assert lower == f"{tree.name}/c/page.html"
    assert "upper" in (tmp_path / "out" / str(upper)).read_text()
    assert "lower" in (tmp_path / "out" / str(lower)).read_text()
    start = tree / "c" / "index.html"
    for reference in links_from(start):
        target = resolves(start, reference)
        assert target is not None and target.is_file(), reference


def test_a_page_of_scripts_without_text_is_counted_as_a_suspected_shell(
    site: Site, tmp_path: Path
) -> None:
    site.html("/s/", '<a href="app">App</a><a href="article">Article</a>')
    site.html(
        "/s/app",
        '<html><head><script src="bundle.js"></script></head>'
        '<body><div id="root"></div><noscript>'
        + "Enable JavaScript. " * 20
        + "</noscript></body></html>",
    )
    site.binary("/s/bundle.js", b"render()", "text/javascript")
    site.html(
        "/s/article",
        "<script>track()</script><p>" + "A paragraph of real text. " * 10 + "</p>",
    )

    result = mirror(tmp_path, "--output=out", "--browser=never", site.url("/s/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert re.search(r"^Suspected JavaScript shells: 1$", result.stdout, re.MULTILINE)


def test_the_manpage_states_what_the_crawl_does() -> None:
    page = (SKILL / "help.md").read_text(encoding="utf-8")
    options = page.partition("\n## OPTIONS\n")[2].partition("\n## ")[0]
    for flag in ("--max-pages=", "--delay=", "--no-links", "--ignore-robots"):
        assert f"**{flag}" in options, flag
    description = page.partition("\n## DESCRIPTION\n")[2].partition("\n## ")[0]
    for statement in (
        "is the root",
        "is in scope when",
        "`www.`",
        "`robots.txt`",
        "RFC 9309",
        "Resources are exempt",
        "5000 pages and files",
        "differ only in case",
        "suspected JavaScript shell",
        "`nofollow`",
        "`X-Robots-Tag`",
    ):
        assert statement in description, statement


def test_a_link_in_scope_is_fetched_where_resources_left_the_same_url_out(
    site: Site, tmp_path: Path
) -> None:
    site.html("/l/", '<img src="big.png"><a href="big.png">Full size</a>')
    site.binary("/l/big.png", b"big")

    result = mirror(tmp_path, "--output=out", "--resources=none", site.url("/l/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    rows = {row["url"]: row for row in manifest(tmp_path / "out")}
    image = rows[site.url("/l/big.png")]
    assert (image["kind"], image["source"], image["outcome"]) == (
        "file",
        "link",
        "fetched",
    )
    assert (site.tree(tmp_path / "out") / "l" / "big.png").read_bytes() == b"big"


# --- Sitemaps and feeds ---------------------------------------------------------

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def urlset(*urls: str) -> bytes:
    entries = "".join(f"<url><loc>{url}</loc></url>" for url in urls)
    return (
        f'<?xml version="1.0"?><urlset xmlns="{SITEMAP_NS}">{entries}</urlset>'.encode()
    )


def sitemap_index(*urls: str) -> bytes:
    entries = "".join(f"<sitemap><loc>{url}</loc></sitemap>" for url in urls)
    return (
        f'<?xml version="1.0"?><sitemapindex xmlns="{SITEMAP_NS}">{entries}'
        "</sitemapindex>"
    ).encode()


def rss(*links: str) -> bytes:
    items = "".join(
        f"<item><title>t</title><link>{link}</link></item>" for link in links
    )
    return f'<?xml version="1.0"?><rss version="2.0"><channel>{items}</channel></rss>'.encode()


def atom(*links: str) -> bytes:
    entries = "".join(
        f'<entry><title>t</title><link rel="alternate" href="{link}"/></entry>'
        for link in links
    )
    return (
        '<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">'
        f"{entries}</feed>"
    ).encode()


def serve_the_sourced_site(site: Site) -> None:
    """A root `/docs/` whose unlinked pages only sitemaps and feeds name."""

    site.add(
        "/robots.txt",
        Response(
            b"User-agent: *\nAllow: /\n\nSitemap: /maps/index.xml\n", "text/plain"
        ),
    )
    site.add(
        "/maps/index.xml",
        Response(
            sitemap_index(site.url("/maps/pages.xml.gz"), site.url("/maps/index.xml")),
            "application/xml",
        ),
    )
    site.add(
        "/maps/pages.xml.gz",
        Response(
            gzip.compress(
                urlset(
                    site.url("/docs/unlinked-a"),
                    site.url("/docs/unlinked-b"),
                    site.url("/outside/page"),
                    site.url("/docs/elsewhere", host="localhost"),
                )
            ),
            "application/x-gzip",
        ),
    )
    site.add(
        "/wp-sitemap.xml",
        Response(urlset(site.url("/docs/wp-only")), "application/xml"),
    )
    site.html(
        "/docs/",
        '<html><head><link rel="alternate" type="application/atom+xml"'
        ' href="atom.xml"></head><body><img src="pic.png"></body></html>',
    )
    site.binary("/docs/pic.png", b"pic")
    site.add("/docs/atom.xml", Response(atom("from-atom"), "application/atom+xml"))
    site.add("/feed/", Response(rss(site.url("/docs/from-rss")), "application/rss+xml"))
    for page in ("unlinked-a", "unlinked-b", "wp-only", "from-atom", "from-rss"):
        site.html(f"/docs/{page}", f"<p>{page}</p>")
    site.html("/outside/page", "<p>outside</p>")
    site.html("/docs/elsewhere", "<p>elsewhere</p>")


def test_sitemaps_named_by_robots_and_tried_at_the_root_feed_the_crawl(
    site: Site, tmp_path: Path
) -> None:
    serve_the_sourced_site(site)

    result = mirror(tmp_path, "--output=out", site.url("/docs/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    output = tmp_path / "out"
    tree = site.tree(output)
    for page in ("unlinked-a", "unlinked-b", "wp-only"):
        assert (tree / "docs" / f"{page}.html").is_file(), page
    assert not site.requested("/outside/page")
    assert not site.requested("/docs/elsewhere", host="localhost")
    assert len(site.requested("/maps/index.xml")) == 1, "a cyclic index ends"

    rows = manifest(output)
    by_url = {row["url"]: row for row in rows}
    assert len(by_url) == len(rows)
    for page in ("unlinked-a", "unlinked-b"):
        row = by_url[site.url(f"/docs/{page}")]
        assert (row["kind"], row["source"], row["outcome"]) == (
            "page",
            "sitemap",
            "fetched",
        )
        assert row["discovered_from"] == site.url("/maps/pages.xml.gz")
    assert by_url[site.url("/docs/wp-only")]["discovered_from"] == site.url(
        "/wp-sitemap.xml"
    )
    for outside in (
        site.url("/outside/page"),
        site.url("/docs/elsewhere", host="localhost"),
    ):
        assert (by_url[outside]["source"], by_url[outside]["outcome"]) == (
            "sitemap",
            "out-of-scope",
        )

    for path in ("/maps/index.xml", "/maps/pages.xml.gz", "/wp-sitemap.xml"):
        row = by_url[site.url(path)]
        assert (row["kind"], row["outcome"], row["local_path"]) == (
            "sitemap",
            "fetched",
            None,
        ), path
    for path in ("/sitemap.xml", "/sitemap_index.xml"):
        row = by_url[site.url(path)]
        assert (row["kind"], row["outcome"], row["status"]) == (
            "sitemap",
            "missing",
            404,
        )
    assert not list(output.rglob("*.xml")) and not list(output.rglob("*.gz"))
    assert not (tree / "feed").exists() and not (tree / "docs" / "atom.xml").exists()


def test_feeds_named_by_a_page_and_tried_at_the_root_feed_the_crawl(
    site: Site, tmp_path: Path
) -> None:
    serve_the_sourced_site(site)

    result = mirror(tmp_path, "--output=out", site.url("/docs/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    output = tmp_path / "out"
    tree = site.tree(output)
    rows = {row["url"]: row for row in manifest(output)}
    for page, feed in (("from-atom", "/docs/atom.xml"), ("from-rss", "/feed/")):
        assert (tree / "docs" / f"{page}.html").is_file(), page
        row = rows[site.url(f"/docs/{page}")]
        assert (row["source"], row["discovered_from"]) == ("feed", site.url(feed))
    for feed in ("/docs/atom.xml", "/feed/"):
        row = rows[site.url(feed)]
        assert (row["kind"], row["outcome"], row["local_path"]) == (
            "feed",
            "fetched",
            None,
        )
        assert len(site.requested(feed)) == 1
    probe = rows[site.url("/docs/feed/")]
    assert (probe["kind"], probe["outcome"]) == ("feed", "missing")
    assert not [
        row
        for row in rows.values()
        if row["kind"] == "page" and "atom.xml" in str(row["url"])
    ]

    assert re.search(r"^Candidates from sitemaps: 5$", result.stdout, re.MULTILINE)
    assert re.search(r"^Candidates from feeds: 2$", result.stdout, re.MULTILINE)
    assert re.search(r"^Candidates from links: 0$", result.stdout, re.MULTILINE)
    assert re.search(r"^Sitemaps read: 3$", result.stdout, re.MULTILINE)
    assert re.search(r"^Feeds read: 2$", result.stdout, re.MULTILINE)


def test_each_source_can_be_turned_off(site: Site, tmp_path: Path) -> None:
    serve_the_sourced_site(site)
    site.html(
        "/docs/",
        '<html><head><link rel="alternate" type="application/rss+xml"'
        ' href="atom.xml"></head><body><a href="linked">L</a></body></html>',
    )
    site.html("/docs/linked", "<p>linked</p>")

    def run(name: str, *flags: str) -> set[str]:
        site.requests.clear()
        directory = tmp_path / name
        directory.mkdir()
        result = mirror(directory, "--output=out", *flags, site.url("/docs/"))
        assert result.returncode == 0, (result.stdout, result.stderr)
        return {request.path for request in site.requests}

    no_sitemap = run("no-sitemap", "--no-sitemap")
    assert not {"/docs/unlinked-a", "/docs/wp-only", "/maps/index.xml"} & no_sitemap
    assert not {"/sitemap.xml", "/wp-sitemap.xml"} & no_sitemap
    assert {"/docs/from-atom", "/docs/from-rss", "/docs/linked"} <= no_sitemap

    no_feeds = run("no-feeds", "--no-feeds")
    assert (
        not {"/docs/from-atom", "/docs/from-rss", "/feed/", "/docs/atom.xml"} & no_feeds
    )
    assert {"/docs/unlinked-a", "/docs/linked"} <= no_feeds

    no_links = run("no-links", "--no-links")
    assert "/docs/linked" not in no_links
    assert {"/docs/unlinked-a", "/docs/from-atom", "/docs/from-rss"} <= no_links

    nothing = run("nothing", "--no-links", "--no-sitemap", "--no-feeds")
    assert nothing == {"/robots.txt", "/docs/"}


def test_sitemap_candidates_count_toward_the_cap_and_obey_robots(
    site: Site, tmp_path: Path
) -> None:
    site.add(
        "/robots.txt",
        Response(b"User-agent: *\nDisallow: /docs/private\n", "text/plain"),
    )
    site.add(
        "/sitemap.xml",
        Response(
            urlset(
                *(site.url(f"/docs/p{n}") for n in range(40)), site.url("/docs/private")
            ),
            "application/xml",
        ),
    )
    site.html("/docs/", "<p>start</p>")
    for n in range(40):
        site.html(f"/docs/p{n}", f"<p>{n}</p>")
    site.html("/docs/private", "<p>private</p>")

    capped = tmp_path / "capped"
    capped.mkdir()
    result = mirror(capped, "--output=out", "--max-pages=3", site.url("/docs/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    fetched = [n for n in range(40) if site.requested(f"/docs/p{n}")]
    assert fetched == [0, 1]
    assert re.search(r"^Over the cap: 38$", result.stdout, re.MULTILINE)

    site.requests.clear()
    polite = tmp_path / "polite"
    polite.mkdir()
    result = mirror(polite, "--output=out", site.url("/docs/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert not site.requested("/docs/private")
    rows = {row["url"]: row for row in manifest(polite / "out")}
    assert (
        rows[site.url("/docs/private")]["source"],
        rows[site.url("/docs/private")]["outcome"],
    ) == (
        "sitemap",
        "robots",
    )
    assert re.search(r"^Stopped by robots\.txt: 1$", result.stdout, re.MULTILINE)


def test_sitemaps_and_feeds_are_fetched_with_the_runs_identity_and_headers(
    site: Site, tmp_path: Path
) -> None:
    serve_the_sourced_site(site)

    result = mirror(
        tmp_path,
        "--output=out",
        "--header=X-Token: secret",
        "--user-agent=fixture-bot/2",
        site.url("/docs/"),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    for path in ("/maps/index.xml", "/maps/pages.xml.gz", "/feed/", "/docs/atom.xml"):
        [request] = site.requested(path)
        assert request.headers["User-Agent"] == "fixture-bot/2", path
        assert request.headers["X-Token"] == "secret", path


def test_the_manpage_states_the_sources_and_where_they_are_looked_for() -> None:
    page = (SKILL / "help.md").read_text(encoding="utf-8")
    synopsis = page.partition("\n## SYNOPSIS\n")[2].partition("\n## ")[0]
    options = page.partition("\n## OPTIONS\n")[2].partition("\n## ")[0]
    description = page.partition("\n## DESCRIPTION\n")[2].partition("\n## ")[0]
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for flag in ("--no-sitemap", "--no-feeds"):
        assert f"**{flag}**" in synopsis, flag
        assert f"**{flag}**" in options, flag
        assert f"[{flag}]" in body, flag
        assert f"`{flag}`" in body.partition("## Arguments")[2], flag
    for location in (
        *PROBED,
        "`Sitemap:`",
        "application/rss+xml",
        "application/atom+xml",
    ):
        assert location.strip("`") in description, location


# --- Include and exclude --------------------------------------------------------


def serve_the_widened_site(site: Site) -> None:
    """A root `/docs/` beside `/press/` on its own host, and a second host's pages.

    `robots.txt` disallows `/docs/private/`, so an exclude that keeps that page
    out is seen to win over the robots outcome.
    """

    second = site.url("/", host=OTHER_HOST)
    site.add(
        "/robots.txt",
        Response(b"User-agent: *\nDisallow: /docs/private/\n", "text/plain"),
    )
    site.html(
        "/docs/",
        f"""<html><head><link rel="stylesheet" href="style.css"></head><body>
<img src="/assets/logo.png">
<a href="guide">Guide</a>
<a href="private/secret">Secret</a>
<a href="/press/">Press</a>
<a href="{second}">Second host</a>
</body></html>""",
        host=ROOT_HOST,
    )
    site.html("/docs/guide", "<p>guide</p>", host=ROOT_HOST)
    site.html("/docs/private/secret", "<p>secret</p>", host=ROOT_HOST)
    site.css("/docs/style.css", "body { color: black }")
    site.binary("/assets/logo.png", b"logo")
    site.html(
        "/press/",
        '<a href="release">Release</a><a href="/about/">About</a>',
        host=ROOT_HOST,
    )
    site.html("/press/release", '<a href="./">Press</a>', host=ROOT_HOST)
    site.html("/about/", "<p>about</p>", host=ROOT_HOST)
    site.html("/", '<a href="page">Page</a>', host=OTHER_HOST)
    site.html("/page", '<a href="/">Home</a>', host=OTHER_HOST)


def test_an_include_widens_the_scope_to_pages_outside_the_root(
    site: Site, tmp_path: Path
) -> None:
    serve_the_widened_site(site)

    result = mirror(
        tmp_path,
        "--output=out",
        "--include=^https?://[^/]+/press/",
        site.url("/docs/", host=ROOT_HOST),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    tree = site.tree(tmp_path / "out", host=ROOT_HOST)
    for path, relative in (
        ("/press/", "press/index.html"),
        ("/press/release", "press/release.html"),
    ):
        assert len(site.requested(path, host=ROOT_HOST)) == 1, path
        assert (tree / relative).is_file(), relative
    assert not site.requested("/about/", host=ROOT_HOST)
    assert not [r for r in site.requests if r.host.startswith(OTHER_HOST)]

    # The link to the included page is rewritten like one under the root.
    start = tree / "docs" / "index.html"
    [press] = [ref for ref in links_from(start) if "press" in ref]
    target = resolves(start, press)
    assert target == (tree / "press" / "index.html").resolve()

    rows = {row["url"]: row for row in manifest(tmp_path / "out")}
    assert rows[site.url("/press/", host=ROOT_HOST)]["outcome"] == "fetched"
    assert rows[site.url("/about/", host=ROOT_HOST)]["outcome"] == "out-of-scope"
    assert rows[site.url("/", host=OTHER_HOST)]["outcome"] == "out-of-scope"


def test_an_include_matching_a_second_hosts_root_saves_that_host(
    site: Site, tmp_path: Path
) -> None:
    serve_the_widened_site(site)
    second = site.url("/", host=OTHER_HOST)

    result = mirror(
        tmp_path,
        "--output=out",
        f"--include=^{re.escape(second)}",
        site.url("/docs/", host=ROOT_HOST),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    output = tmp_path / "out"
    other = site.tree(output, host=OTHER_HOST)
    home = other / "index.html"
    page = other / "page.html"
    assert home.is_file() and page.is_file()
    [back] = links_from(page)
    assert resolves(page, back) == home.resolve()
    [forward] = links_from(home)
    assert resolves(home, forward) == page.resolve()
    start = site.tree(output, host=ROOT_HOST) / "docs" / "index.html"
    [to_second] = [ref for ref in links_from(start) if OTHER_HOST in ref]
    assert resolves(start, to_second) == home.resolve()
    assert not site.requested("/press/", host=ROOT_HOST)


def test_an_exclude_keeps_a_page_and_a_resource_out_and_wins_over_robots(
    site: Site, tmp_path: Path
) -> None:
    serve_the_widened_site(site)

    result = mirror(
        tmp_path,
        "--output=out",
        "--exclude=/docs/private/",
        r"--exclude=style\.css$",
        "--exclude=/assets/",
        "--exclude=/about/",
        "--include=/press/",
        site.url("/docs/", host=ROOT_HOST),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    for path in ("/docs/private/secret", "/docs/style.css", "/assets/logo.png"):
        assert not site.requested(path, host=ROOT_HOST), path
    assert not site.requested("/about/", host=ROOT_HOST)
    assert site.requested("/docs/guide", host=ROOT_HOST)
    rows = {row["url"]: row for row in manifest(tmp_path / "out")}
    for path in ("/docs/private/secret", "/docs/style.css", "/assets/logo.png"):
        row = rows[site.url(path, host=ROOT_HOST)]
        assert (row["outcome"], row["status"], row["local_path"]) == (
            "excluded",
            None,
            None,
        ), path
    # Outside the root and included too, the exclude still wins.
    assert rows[site.url("/about/", host=ROOT_HOST)]["outcome"] == "excluded"

    # The stylesheet's reference is left absolute.
    start = site.tree(tmp_path / "out", host=ROOT_HOST) / "docs" / "index.html"
    references = {ref for _, _, ref in read_page(start).references}
    assert site.url("/docs/style.css", host=ROOT_HOST) in references
    assert site.url("/assets/logo.png", host=ROOT_HOST) in references

    assert re.search(r"^Excluded: 4$", result.stdout, re.MULTILINE)
    assert re.search(r"^Stopped by robots\.txt: 0$", result.stdout, re.MULTILINE)
    log = (tmp_path / "out" / ".mirror" / "run.log").read_text(encoding="utf-8")
    assert f"excluded {site.url('/docs/private/secret', host=ROOT_HOST)}" in log


def test_in_scope_resources_follow_the_widened_scope(
    site: Site, tmp_path: Path
) -> None:
    serve_the_widened_site(site)

    result = mirror(
        tmp_path,
        "--output=out",
        "--resources=in-scope",
        "--include=/assets/",
        site.url("/docs/", host=ROOT_HOST),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert len(site.requested("/assets/logo.png", host=ROOT_HOST)) == 1
    tree = site.tree(tmp_path / "out", host=ROOT_HOST)
    assert (tree / "assets" / "logo.png").read_bytes() == b"logo"


def test_a_possessive_quantifier_and_keep_out_compile_and_match(
    site: Site, tmp_path: Path
) -> None:
    serve_the_widened_site(site)

    result = mirror(
        tmp_path,
        "--output=out",
        r"--include=^https?://[^/]++/pre\Kss/",
        r"--exclude=/press/\Krel(?:ease)++$",
        site.url("/docs/", host=ROOT_HOST),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert site.requested("/press/", host=ROOT_HOST)
    assert not site.requested("/press/release", host=ROOT_HOST)
    rows = {row["url"]: row for row in manifest(tmp_path / "out")}
    assert rows[site.url("/press/release", host=ROOT_HOST)]["outcome"] == "excluded"


def test_an_exclude_keeps_a_sitemap_from_being_read(site: Site, tmp_path: Path) -> None:
    serve_the_sourced_site(site)

    result = mirror(tmp_path, "--output=out", "--exclude=/maps/", site.url("/docs/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert not site.requested("/maps/index.xml")
    assert not site.requested("/docs/unlinked-a")
    rows = {row["url"]: row for row in manifest(tmp_path / "out")}
    row = rows[site.url("/maps/index.xml")]
    assert (row["kind"], row["outcome"]) == ("sitemap", "excluded")


@pytest.mark.parametrize(
    ("flag", "error"),
    [
        ("--include=(", "missing )"),
        ("--exclude=[a-", "unterminated character set"),
    ],
)
def test_a_pattern_that_does_not_compile_is_refused_before_anything_is_fetched(
    site: Site, tmp_path: Path, flag: str, error: str
) -> None:
    site.html("/docs/", "<p>docs</p>")

    result = mirror(tmp_path, flag, site.url("/docs/"))

    assert result.returncode == 2, (result.stdout, result.stderr)
    first = result.stdout.splitlines()[0]
    assert f"'{flag}'" in first
    assert error in first
    assert result.stdout.rstrip("\n").endswith("see '/mirror --help'")
    assert site.requests == []
    assert list(tmp_path.iterdir()) == []


def test_an_exclude_matching_the_start_page_is_refused(
    site: Site, tmp_path: Path
) -> None:
    site.html("/docs/", "<p>docs</p>")

    result = mirror(tmp_path, "--exclude=/docs/$", site.url("/docs/"))

    assert result.returncode == 2, (result.stdout, result.stderr)
    assert "'--exclude=/docs/$'" in result.stdout.splitlines()[0]
    assert result.stdout.rstrip("\n").endswith("see '/mirror --help'")
    assert site.requests == []
    assert list(tmp_path.iterdir()) == []


def test_the_manpage_states_include_and_exclude() -> None:
    page = (SKILL / "help.md").read_text(encoding="utf-8")
    synopsis = page.partition("\n## SYNOPSIS\n")[2].partition("\n## ")[0]
    options = page.partition("\n## OPTIONS\n")[2].partition("\n## ")[0]
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for flag in ("--include=", "--exclude="):
        assert f"[**{flag}**_REGEX_ ...]" in synopsis, flag
        assert f"**{flag}**_REGEX_" in options, flag
        assert f"[{flag}<regex> ...]" in body, flag
        assert f"`{flag.rstrip('=')}`" in body.partition("## Arguments")[2], flag
    for statement in ("`regex`", "unanchored", r"`^https://ir\.x\.se/`"):
        assert statement in page, statement
    engine = ENGINE.read_text(encoding="utf-8")
    metadata = engine.partition("# /// script")[2].partition("# ///")[0]
    assert re.search(r'"regex==[0-9.]+"', metadata)


# --- A second run ---------------------------------------------------------------

# The date every versioned route says it was last modified.
LAST_MODIFIED = "Wed, 09 Sep 2026 10:00:00 GMT"

# A time well before any run, set on every saved file so a rewrite shows.
EARLIER = 1_000_000_000


def versioned(
    site: Site,
    path: str,
    body: bytes,
    content_type: str = "text/html; charset=utf-8",
    version: int = 1,
) -> None:
    """Serve *body* at *path* with an `ETag` of its *version* and a `Last-Modified`."""

    headers = {"ETag": f'"{path}-{version}"', "Last-Modified": LAST_MODIFIED}
    site.add(path, Response(body, content_type, headers=headers))


def serve_the_versioned_site(site: Site) -> None:
    """A root `/v/` with pages, a file and resources, every one with both validators."""

    versioned(
        site,
        "/v/",
        b'<link rel="stylesheet" href="css/site.css"><img src="img/pic.png">'
        b'<a href="page">Page</a><a href="gone">Gone</a><a href="doc.pdf">Doc</a>',
    )
    versioned(site, "/v/page", b"<p>Page</p>")
    versioned(site, "/v/gone", b"<p>Gone</p>")
    versioned(site, "/v/doc.pdf", b"%PDF-1.4", "application/pdf")
    versioned(
        site, "/v/css/site.css", b"body { background: url(../img/bg.png); }", "text/css"
    )
    versioned(site, "/v/img/pic.png", b"pic", "image/png")
    versioned(site, "/v/img/bg.png", b"bg", "image/png")


def saved_rows(output: Path) -> dict[str, dict[str, object]]:
    """Every manifest row with a saved file, by its URL."""

    return {str(row["url"]): row for row in manifest(output) if row["local_path"]}


def age_the_mirror(output: Path) -> dict[Path, int]:
    """Set every saved file and raw copy to an earlier time, and return the times."""

    times: dict[Path, int] = {}
    for path in output.rglob("*"):
        if path.is_file() and path.name not in ("manifest.ndjson", "run.log"):
            os.utime(path, ns=(EARLIER * 10**9, EARLIER * 10**9))
            times[path] = path.stat().st_mtime_ns
    return times


def count(report: str, label: str) -> int:
    found = re.search(rf"^{re.escape(label)}: (\d+)$", report, re.MULTILINE)
    assert found is not None, (label, report)
    return int(found.group(1))


def test_a_second_run_against_an_unchanged_site_asks_conditionally_and_replaces_nothing(
    site: Site, tmp_path: Path
) -> None:
    serve_the_versioned_site(site)
    output = tmp_path / "out"
    first = mirror(tmp_path, "--output=out", site.url("/v/"))
    assert first.returncode == 0, (first.stdout, first.stderr)
    saved = saved_rows(output)
    assert len(saved) == 7
    times = age_the_mirror(output)

    for run in ("second", "third"):
        site.requests.clear()
        result = mirror(tmp_path, "--output=out", site.url("/v/"))

        assert result.returncode == 0, (run, result.stdout, result.stderr)
        for url, row in saved.items():
            [request] = site.requested(urlsplit(url).path)
            assert request.headers["If-None-Match"] == row["etag"], (run, url)
            assert request.headers["If-Modified-Since"] == row["last_modified"], url
        rows = {str(row["url"]): row for row in manifest(output)}
        for url, row in saved.items():
            now = rows[url]
            assert (now["outcome"], now["status"]) == ("unchanged", 304), (run, url)
            for kept in ("etag", "last_modified", "sha256", "size", "content_type"):
                assert now[kept] == row[kept], (run, url, kept)
            assert now["local_path"] == row["local_path"], (run, url)
        assert {path: path.stat().st_mtime_ns for path in times} == times, run
        assert count(result.stdout, "Pages unchanged") == 3
        assert count(result.stdout, "Files unchanged") == 1
        assert count(result.stdout, "Resources unchanged") == 3
        assert count(result.stdout, "Pages fetched") == 0
        assert count(result.stdout, "Absent") == 0


def test_a_changed_page_is_replaced_with_its_raw_copy_and_nothing_else_is(
    site: Site, tmp_path: Path
) -> None:
    serve_the_versioned_site(site)
    output = tmp_path / "out"
    first = mirror(tmp_path, "--output=out", site.url("/v/"))
    assert first.returncode == 0, (first.stdout, first.stderr)
    times = age_the_mirror(output)
    versioned(site, "/v/page", b"<p>Page, revised</p>", version=2)

    result = mirror(tmp_path, "--output=out", site.url("/v/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    tree = site.tree(output)
    page = tree / "v" / "page.html"
    raw = output / ".mirror" / "raw" / tree.name / "v" / "page.html"
    assert "revised" in page.read_text(encoding="utf-8")
    assert raw.read_bytes() == b"<p>Page, revised</p>"
    for path, before in times.items():
        if path not in (page, raw):
            assert path.stat().st_mtime_ns == before, path
    rows = {str(row["url"]): row for row in manifest(output)}
    changed = rows[site.url("/v/page")]
    assert (changed["outcome"], changed["etag"]) == ("fetched", '"/v/page-2"')
    for url, row in rows.items():
        if row["local_path"] and url != site.url("/v/page"):
            assert row["outcome"] == "unchanged", url
    assert count(result.stdout, "Pages fetched") == 1
    assert count(result.stdout, "Pages unchanged") == 2


def test_a_page_new_to_the_mirror_turns_a_reference_in_an_unchanged_page_local(
    site: Site, tmp_path: Path
) -> None:
    serve_the_versioned_site(site)
    versioned(site, "/v/", b'<a href="later">Later</a>')
    site.add("/v/later", Response(b"", status=404), Response(b"<p>Later</p>"))
    output = tmp_path / "out"
    first = mirror(tmp_path, "--output=out", site.url("/v/"))
    start = site.tree(output) / "v" / "index.html"
    assert links_from(start) == [site.url("/v/later")], first.stdout

    result = mirror(tmp_path, "--output=out", site.url("/v/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    rows = {str(row["url"]): row for row in manifest(output)}
    assert rows[site.url("/v/")]["outcome"] == "unchanged"
    assert rows[site.url("/v/later")]["outcome"] == "fetched"
    [reference] = links_from(start)
    target = resolves(start, reference)
    assert target is not None and target.read_text().count("Later") == 1


def test_a_page_gone_from_the_site_keeps_its_file_and_is_recorded_absent(
    site: Site, tmp_path: Path
) -> None:
    serve_the_versioned_site(site)
    output = tmp_path / "out"
    first = mirror(tmp_path, "--output=out", site.url("/v/"))
    assert first.returncode == 0, (first.stdout, first.stderr)
    gone = saved_rows(output)[site.url("/v/gone")]
    versioned(
        site,
        "/v/",
        b'<link rel="stylesheet" href="css/site.css"><img src="img/pic.png">'
        b'<a href="page">Page</a><a href="doc.pdf">Doc</a>',
        version=2,
    )
    site.add("/v/gone", Response(b"", status=404))

    for run in ("second", "third"):
        result = mirror(tmp_path, "--output=out", site.url("/v/"))

        assert result.returncode == 0, (run, result.stdout, result.stderr)
        assert "<p>Gone</p>" in (output / str(gone["local_path"])).read_text(), run
        rows = {str(row["url"]): row for row in manifest(output)}
        absent = rows[site.url("/v/gone")]
        assert (absent["outcome"], absent["local_path"]) == (
            "absent",
            gone["local_path"],
        )
        assert count(result.stdout, "Absent") == 1, run
    assert not site.requested("/v/gone")[1:]


def test_a_row_without_a_validator_sends_only_what_it_has(
    site: Site, tmp_path: Path
) -> None:
    site.html("/n/", '<img src="dated.png"><img src="plain.png">')
    site.add(
        "/n/dated.png",
        Response(b"dated", "image/png", headers={"Last-Modified": LAST_MODIFIED}),
    )
    site.binary("/n/plain.png", b"plain")
    first = mirror(tmp_path, "--output=out", site.url("/n/"))
    assert first.returncode == 0, (first.stdout, first.stderr)
    site.requests.clear()

    result = mirror(tmp_path, "--output=out", site.url("/n/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    [dated] = site.requested("/n/dated.png")
    assert dated.headers.get("If-Modified-Since") == LAST_MODIFIED
    assert "If-None-Match" not in dated.headers
    for path in ("/n/plain.png", "/n/"):
        [plain] = site.requested(path)
        assert "If-None-Match" not in plain.headers, path
        assert "If-Modified-Since" not in plain.headers, path
    rows = {str(row["url"]): row for row in manifest(tmp_path / "out")}
    assert rows[site.url("/n/dated.png")]["outcome"] == "unchanged"
    assert rows[site.url("/n/plain.png")]["outcome"] == "fetched"


def test_a_dry_run_against_a_mirror_marks_the_conditional_urls_and_writes_nothing(
    site: Site, tmp_path: Path
) -> None:
    serve_the_versioned_site(site)
    output = tmp_path / "out"
    first = mirror(tmp_path, "--output=out", site.url("/v/"))
    assert first.returncode == 0, (first.stdout, first.stderr)
    saved = saved_rows(output)
    times = age_the_mirror(output)
    state = {
        name: (output / ".mirror" / name).read_bytes()
        for name in ("manifest.ndjson", "run.log")
    }
    before = sorted(output.rglob("*"))

    result = mirror(tmp_path, "--output=out", "--dry-run", site.url("/v/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    listed = result.stdout.partition("Would fetch:")[2].partition("\nPages")[0]
    marked = {
        line.split()[0]
        for line in listed.splitlines()
        if line.strip().endswith(" conditional")
    }
    assert marked == set(saved)
    assert f"{site.url('/robots.txt')}\n" in listed
    assert sorted(output.rglob("*")) == before
    assert {path: path.stat().st_mtime_ns for path in times} == times
    for name, content in state.items():
        assert (output / ".mirror" / name).read_bytes() == content, name


def test_a_charset_the_server_declared_holds_for_an_unchanged_page(
    site: Site, tmp_path: Path
) -> None:
    body = "<p>Smörgåsbord</p>".encode("iso-8859-1")
    site.add(
        "/l/",
        Response(body, "text/html; charset=iso-8859-1", headers={"ETag": '"l"'}),
    )
    first = mirror(tmp_path, "--output=out", site.url("/l/"))
    assert first.returncode == 0, (first.stdout, first.stderr)
    page = site.tree(tmp_path / "out") / "l" / "index.html"
    saved = page.read_bytes()

    result = mirror(tmp_path, "--output=out", site.url("/l/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert page.read_bytes() == saved
    assert "Smörgåsbord" in saved.decode("utf-8")


def test_the_manpage_states_that_a_rerun_is_incremental() -> None:
    page = (SKILL / "help.md").read_text(encoding="utf-8")
    description = page.partition("\n## DESCRIPTION\n")[2].partition("\n## ")[0]
    for statement in (
        "incremental",
        "`If-None-Match`",
        "`If-Modified-Since`",
        "`ETag`",
        "`Last-Modified`",
        "nothing is ever deleted",
        "`unchanged`",
        "`absent`",
    ):
        assert statement in description, statement
    files = page.partition("\n## FILES\n")[2].partition("\n## ")[0]
    for outcome in ("`unchanged`", "`absent`", "`charset`"):
        assert outcome in files, outcome
    options = page.partition("\n## OPTIONS\n")[2].partition("\n## ")[0]
    assert "`conditional`" in options


# --- Blocks and rungs ------------------------------------------------------------

# The rung-2 identity the engine sends, as the ticket states it literally.
CHROME_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
        "image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-ch-ua": '"Chromium";v="140", "Google Chrome";v="140", "Not?A_Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}

FORBIDDEN = Response(b"<title>Forbidden</title>", status=403)


def is_chrome(request: Request) -> bool:
    return "Chrome" in request.headers.get("User-Agent", "")


def serve_the_guarded_site(site: Site) -> None:
    """A section that answers `403` to every request whose user-agent is not Chrome."""

    site.gate = lambda request: None if is_chrome(request) else FORBIDDEN
    site.html("/g/", '<a href="next">Next</a><img src="logo.png">')
    site.html("/g/next", "<p>next</p>")
    site.binary("/g/logo.png", b"logo")


def test_a_host_that_refuses_the_skills_identity_climbs_to_rung_two(
    site: Site, tmp_path: Path
) -> None:
    serve_the_guarded_site(site)

    result = mirror(tmp_path, "--output=out", site.url("/g/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    first = site.requests[0]
    assert (first.path, is_chrome(first)) == ("/robots.txt", False)
    assert all(is_chrome(request) for request in site.requests[1:])
    asked = [(request.path, is_chrome(request)) for request in site.requests]
    assert len(asked) == len(set(asked)), "nothing is fetched twice on one rung"
    assert site.requested("/robots.txt")[-1] is not first
    for path in ("/g/", "/g/next", "/g/logo.png"):
        assert [is_chrome(request) for request in site.requested(path)] == [True]
    tree = site.tree(tmp_path / "out") / "g"
    assert (tree / "index.html").is_file() and (tree / "next.html").is_file()

    rows = {row["url"]: row for row in manifest(tmp_path / "out")}
    for path in ("/robots.txt", "/g/", "/g/next", "/g/logo.png"):
        assert (rows[site.url(path)]["fetcher"], rows[site.url(path)]["rung"]) == (
            "http",
            2,
        ), path
    assert re.search(
        rf"{re.escape(site.url(''))}.* climbed to rung 2 after a 403 on"
        rf" {re.escape(site.url('/robots.txt'))}",
        result.stdout,
    )
    assert re.search(r"^Hosts that stayed on rung 1: 0$", result.stdout, re.MULTILINE)
    assert re.search(r"^Blocked: 0$", result.stdout, re.MULTILINE)


def test_rung_two_looks_like_chrome_and_the_users_identity_wins_on_both_rungs(
    site: Site, tmp_path: Path
) -> None:
    serve_the_guarded_site(site)

    result = mirror(tmp_path, "--output=a", site.url("/g/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    for request in site.requests[1:]:
        for name, value in CHROME_HEADERS.items():
            assert request.headers.get(name) == value, (name, request)

    site.requests.clear()
    site.gate = lambda request: None if "sec-ch-ua" in request.headers else FORBIDDEN
    result = mirror(
        tmp_path,
        "--output=b",
        "--user-agent=fixture-bot/2",
        "--header=Accept-Language: en",
        site.url("/g/"),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    rungs = {"sec-ch-ua" in request.headers for request in site.requests}
    assert rungs == {False, True}, "both rungs were asked"
    for request in site.requests:
        assert request.headers["User-Agent"] == "fixture-bot/2", request
        assert request.headers["Accept-Language"] == "en", request


def test_a_challenge_page_is_a_block_and_a_busy_answer_that_recovers_is_not(
    site: Site, tmp_path: Path
) -> None:
    challenge = Response(b"<html><head><title>Just a moment...</title></head></html>")
    site.gate = lambda request: (
        challenge if request.path == "/c/" and not is_chrome(request) else None
    )
    site.html("/c/", '<a href="mentions">Mentions</a><img src="busy.png">')
    site.html(
        "/c/mentions",
        "<title>How cf-browser-verification and _cf_chl_opt work</title><p>x</p>",
    )
    site.add(
        "/c/busy.png",
        Response(b"", status=429, headers={"Retry-After": "1"}),
        Response(b"busy", "image/png"),
    )

    result = mirror(tmp_path, "--output=out", site.url("/c/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert [is_chrome(request) for request in site.requested("/c/")] == [False, True]
    busy = site.requested("/c/busy.png")
    assert len(busy) == 2 and busy[1].time - busy[0].time >= 0.9
    rows = {row["url"]: row for row in manifest(tmp_path / "out")}
    assert rows[site.url("/c/busy.png")]["outcome"] == "fetched"
    assert rows[site.url("/c/mentions")]["outcome"] == "fetched"
    assert re.search(
        r'climbed to rung 2 after Cloudflare\'s title "Just a moment\.\.\." on '
        + re.escape(site.url("/c/")),
        result.stdout,
    )
    assert re.search(r"^Blocked: 0$", result.stdout, re.MULTILINE)


@pytest.mark.parametrize(
    "response",
    [
        Response(b"<p>ok</p>", headers={"cf-mitigated": "challenge"}),
        Response(b"<p>ok</p>", headers={"X-DataDome": "protected"}),
        Response(b"<p>ok</p>", headers={"X-Iinfo": "1-2-3"}),
        Response(b"<title>ATTENTION REQUIRED! | CLOUDFLARE</title>"),
        # A title marker is read on every HTML answer, not only a block status.
        Response(b"<title>Just a moment...</title>", status=404),
        Response(b"<title>Just a moment...</title>", status=401),
        # Every answer counts: a redirect followed, and one declined.
        Response(
            b"", status=302, headers={"Location": "/m/", "cf-mitigated": "challenge"}
        ),
        Response(
            b"<title>Just a moment...</title>",
            status=302,
            headers={"Location": "/m/landing"},
        ),
        Response(b"", status=302, headers={"Location": "/elsewhere/", "X-Iinfo": "1"}),
    ],
)
def test_a_marker_on_any_answer_moves_the_host(
    site: Site, tmp_path: Path, response: Response
) -> None:
    site.gate = lambda request: (
        response if request.path == "/m/" and not is_chrome(request) else None
    )
    site.html("/m/", "<p>real</p>")

    result = mirror(
        tmp_path, "--output=out", "--no-sitemap", "--no-feeds", site.url("/m/")
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert [is_chrome(request) for request in site.requested("/m/")] == [False, True]
    assert "climbed to rung 2" in result.stdout


def test_a_host_that_refuses_every_identity_ends_blocked(
    site: Site, tmp_path: Path
) -> None:
    site.gate = lambda request: FORBIDDEN if request.path == "/w/private" else None
    site.html("/w/", '<a href="private">Private</a><a href="open">Open</a>')
    site.html("/w/open", "<p>open</p>")

    result = mirror(tmp_path, "--output=out", "--browser=never", site.url("/w/"))

    assert result.returncode == 1, (result.stdout, result.stderr)
    assert [is_chrome(request) for request in site.requested("/w/private")] == [
        False,
        True,
    ]
    rows = {row["url"]: row for row in manifest(tmp_path / "out")}
    private = rows[site.url("/w/private")]
    assert (private["outcome"], private["status"], private["rung"]) == (
        "blocked",
        403,
        2,
    )
    assert rows[site.url("/w/open")]["outcome"] == "fetched"
    assert re.search(r"^Blocked: 1$", result.stdout, re.MULTILINE)
    assert re.search(r"rung 2 was not enough", result.stdout)
    assert re.search(
        rf"^\s*403 {re.escape(site.url('/w/private'))}$", result.stdout, re.MULTILINE
    )

    site.requests.clear()
    site.gate = lambda request: FORBIDDEN
    whole = tmp_path / "whole"
    whole.mkdir()
    browser = FakeBrowser.at(tmp_path / "browser")
    browser.serve(site.url("/w/"), dom="<body><p>w</p></body>")
    result = mirror(
        whole, "--output=out", "--browser=never", site.url("/w/"), browser=browser
    )

    assert result.returncode == 1, (result.stdout, result.stderr)
    assert "rung 2 was not enough" in result.stdout
    assert "--headed" not in result.stdout
    assert not (whole / "out").exists()
    assert browser.calls() == [], "--browser=never never calls the browser"


def test_a_robots_disallow_is_obeyed_and_moves_no_host(
    site: Site, tmp_path: Path
) -> None:
    site.add(
        "/robots.txt",
        Response(b"User-agent: *\nDisallow: /r/private\n", "text/plain"),
    )
    site.html("/r/", '<a href="private">Private</a>')
    site.html("/r/private", "<p>private</p>")

    result = mirror(tmp_path, "--output=out", site.url("/r/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert not any(is_chrome(request) for request in site.requests)
    assert not site.requested("/r/private")
    private = {row["url"]: row for row in manifest(tmp_path / "out")}[
        site.url("/r/private")
    ]
    assert (private["outcome"], private["fetcher"], private["rung"]) == (
        "robots",
        None,
        None,
    )
    assert re.search(r"^Hosts that stayed on rung 1: 1$", result.stdout, re.MULTILINE)
    assert "climbed" not in result.stdout


def test_browser_never_and_always_are_accepted(site: Site, tmp_path: Path) -> None:
    site.html("/n/", "<p>n</p>")

    result = mirror(tmp_path, "--output=out", "--browser=never", site.url("/n/"))

    assert result.returncode == 0, (result.stdout, result.stderr)


def test_a_browser_value_the_skill_rejects_is_refused_before_anything_is_fetched(
    site: Site, tmp_path: Path
) -> None:
    site.html("/n/", "<p>n</p>")

    result = mirror(tmp_path, "--browser=maybe", site.url("/n/"))

    assert result.returncode == 2, (result.stdout, result.stderr)
    assert "'--browser'" in result.stdout.splitlines()[0]
    assert result.stdout.rstrip("\n").endswith("see '/mirror --help'")
    assert site.requests == []
    assert list(tmp_path.iterdir()) == []


def test_the_manpage_states_the_rungs_and_what_a_block_is() -> None:
    page = (SKILL / "help.md").read_text(encoding="utf-8")
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    synopsis = page.partition("\n## SYNOPSIS\n")[2].partition("\n## ")[0]
    options = page.partition("\n## OPTIONS\n")[2].partition("\n## ")[0]
    assert "[**--browser=**_auto_|_always_|_never_]" in synopsis
    assert "**--browser=**_auto_|_always_|_never_" in options
    assert "[--browser=auto|always|never]" in body
    assert "`--browser`" in body.partition("## Arguments")[2]
    description = page.partition("\n## DESCRIPTION\n")[2].partition("\n## ")[0]
    for statement in (
        "rung 1",
        "rung 2",
        "`sec-ch-ua`",
        "`403`, `429` or `503`",
        "`Just a moment...`",
        "Cloudflare",
        "Akamai",
        "PerimeterX",
        "DataDome",
        "Imperva",
        "is not a block",
    ):
        assert statement in description, statement
    files = page.partition("\n## FILES\n")[2].partition("\n## ")[0]
    for statement in ("`rung`", "`blocked`"):
        assert statement in files, statement


# --- The browser rungs ------------------------------------------------------------

SESSION = re.compile(r"^kntnt-mirror-[0-9]+$")

# The page the browser renders: what its scripts drew is in it, and so are they.
RENDERED = """<html><head><title>Rendered</title>
<link rel="stylesheet" href="style.css">
<link rel="prefetch" href="runtime.json">
<link rel="modulepreload" href="app.js">
<script src="app.js"></script>
</head><body>
<img src="logo.png">
<img src="extra.png">
<noscript><p>Scripts are off.</p></noscript>
<script>document.body.insertAdjacentHTML('beforeend', '<a href="rendered">R</a>')</script>
<a href="rendered">Rendered</a>
</body></html>"""

# What the server sent before any script ran: no link to the rendered page.
SERVED = """<!DOCTYPE html><html><head><title>Rendered</title>
<link rel="stylesheet" href="style.css"><script src="app.js"></script></head>
<body><img src="logo.png"><noscript><p>Scripts are off.</p></noscript>
<script>document.body.insertAdjacentHTML('beforeend', '<a href="rendered">R</a>')</script>
</body></html>"""

STYLE = "body { color: navy; }\n"
LOGO = b"\x89PNG logo"
EXTRA = b"\x89PNG extra"
APP = "console.log('app');\n"


def serve_the_rendered_page(
    site: Site, browser: FakeBrowser, path: str = "/b/"
) -> None:
    """A page only a browser gets: its DOM, and a HAR of what loading it fetched."""

    url = site.url(path)
    browser.serve(
        url,
        dom=RENDERED,
        scroll_bottom=1440,
        har=[
            har_entry(url, "Document", SERVED, "text/html"),
            har_entry(url + "style.css", "Stylesheet", STYLE, "text/css"),
            har_entry(url + "app.js", "Script", APP, "text/javascript"),
            har_entry(url + "logo.png", "Image", LOGO, "image/png"),
            har_entry(
                url + "telemetry?payload=" + "x" * 1000,
                "Image",
                b"pixel",
                "image/gif",
            ),
            har_entry(url + "api/data.json", "XHR", '{"a": 1}', "application/json"),
        ],
    )
    browser.serve(
        url + "rendered",
        dom="<html><head><title>R</title></head><body><p>rendered</p></body></html>",
        har=[har_entry(url + "rendered", "Document", "<p>rendered</p>", "text/html")],
    )
    browser.serve(
        url + "extra.png",
        dom='<html><body><img src="extra.png"></body></html>',
        har=[har_entry(url + "extra.png", "Document", EXTRA, "image/png")],
    )


def test_auto_renders_html_with_executable_javascript(
    site: Site, tmp_path: Path
) -> None:
    url = site.url("/dynamic/")
    site.html(
        "/dynamic/",
        "<html><script>document.body.textContent = 'rendered'</script></html>",
    )
    browser = FakeBrowser.at(tmp_path / "browser")
    browser.serve(
        url,
        dom="<html><body><p>rendered</p></body></html>",
        har=[har_entry(url, "Document", "<p>rendered</p>", "text/html")],
    )

    result = mirror(
        tmp_path,
        "--output=out",
        "--no-links",
        "--no-sitemap",
        "--no-feeds",
        url,
        browser=browser,
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert browser.opened() == [url]
    page = site.tree(tmp_path / "out") / "dynamic" / "index.html"
    assert "rendered" in page.read_text(encoding="utf-8")
    assert "executable JavaScript" in result.stdout


@pytest.mark.parametrize(
    "markup",
    [
        "<html><body><p>static</p></body></html>",
        '<html><script type="application/ld+json">{}</script></html>',
    ],
)
def test_auto_keeps_non_executable_html_on_http(
    site: Site, tmp_path: Path, markup: str
) -> None:
    site.html("/static/", markup)
    browser = FakeBrowser.at(tmp_path / "browser")

    result = mirror(
        tmp_path,
        "--output=out",
        "--no-links",
        "--no-sitemap",
        "--no-feeds",
        site.url("/static/"),
        browser=browser,
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert browser.calls() == []
    [row] = [row for row in manifest(tmp_path / "out") if row["kind"] == "page"]
    assert (row["fetcher"], row["rung"]) == ("http", 1)


def test_a_host_every_http_identity_is_refused_by_is_mirrored_from_a_headless_browser(
    site: Site, tmp_path: Path
) -> None:
    site.gate = lambda request: FORBIDDEN
    browser = FakeBrowser.at(tmp_path / "browser")
    serve_the_rendered_page(site, browser)

    result = mirror(
        tmp_path,
        "--output=out",
        "--user-agent=fixture-bot/3",
        "--header=X-One: 1",
        "--header=X-Two: 2",
        site.url("/b/"),
        browser=browser,
    )

    assert result.returncode == 0, (result.stdout, result.stderr)

    # Only `robots.txt` went over HTTP, on rungs 1 and 2; the rest went to the browser.
    assert [request.path for request in site.requests] == ["/robots.txt"] * 2
    assert site.url("/robots.txt") in browser.opened()
    assert site.url("/sitemap.xml") in browser.opened()

    # The page is the rendered DOM, its scripts gone and its `noscript` kept.
    tree = site.tree(tmp_path / "out") / "b"
    page = (tree / "index.html").read_text(encoding="utf-8")
    assert "<script" not in page
    assert "<noscript>" in page and "Scripts are off." in page
    assert 'rel="prefetch"' not in page and 'rel="modulepreload"' not in page
    assert (tree / "style.css").read_text(encoding="utf-8") == STYLE
    assert (tree / "logo.png").read_bytes() == LOGO
    assert not (tree / "app.js").exists()
    references = {
        (tag, name): value
        for tag, name, value in read_page(tree / "index.html").references
    }
    assert references[("link", "href")] == "style.css"
    sources = [
        value
        for tag, name, value in read_page(tree / "index.html").references
        if tag == "img"
    ]
    assert sources == ["logo.png", "extra.png"]

    # A statically found resource the HAR lacks is opened in the browser too.
    assert (tree / "extra.png").read_bytes() == EXTRA
    assert site.url("/b/extra.png") in browser.opened()
    assert site.url("/b/style.css") not in browser.opened()

    # A link only the rendered DOM holds is followed; the XHR answer is not saved.
    assert (tree / "rendered.html").is_file()
    assert not (tree / "api").exists()
    rows = {str(row["url"]): row for row in manifest(tmp_path / "out")}
    assert site.url("/b/api/data.json") not in rows
    assert not [url for url in rows if "telemetry?payload=" in url]
    for path in ("/b/", "/b/style.css", "/b/logo.png", "/b/extra.png", "/b/rendered"):
        row = rows[site.url(path)]
        assert (row["fetcher"], row["rung"], row["outcome"]) == (
            "browser",
            3,
            "fetched",
        ), path
    assert re.search(
        rf"{re.escape(site.url(''))}.* climbed to rung 3 after a 403 on", result.stdout
    )

    # What the browser was asked, in the engine's own session, with the run's identity.
    calls = browser.calls()
    sessions = {
        call.flags.get("--session") for call in calls if call.command[:1] != ["doctor"]
    }
    assert len(sessions) == 1 and SESSION.match(str(next(iter(sessions))))
    commands = browser.commands()
    assert ["doctor", "--json"] in commands
    for call in calls:
        if call.command[:1] == ["open"]:
            assert call.flags.get("--user-agent") == "fixture-bot/3", call
    headers = [command for command in commands if command[:2] == ["set", "headers"]]
    assert headers and json.loads(headers[0][2]) == {"X-One": "1", "X-Two": "2"}
    assert commands.index(headers[0]) < commands.index(["open", site.url("/b/")])
    viewport = ["set", "viewport", "1280", "720"]
    recording = ["network", "har", "start", "--content", "all"]
    assert commands.index(viewport) < commands.index(recording)
    page_calls = commands[commands.index(["open", site.url("/b/")]) - 1 :]
    assert page_calls[0] == recording
    reads = [call for call in calls if call.command[:2] == ["eval", "--stdin"]]
    assert any(
        "document.documentElement.outerHTML" in str(call.stdin) for call in reads
    )
    after_open = page_calls[1:]
    assert ["wait", "--load", "networkidle"] in after_open
    stop = next(
        command for command in after_open if command[:3] == ["network", "har", "stop"]
    )
    capture = after_open[: after_open.index(stop) + 1]
    scrolls = [command for command in capture if command[:1] == ["scroll"]]
    assert scrolls == [
        ["scroll", "down", "600"],
        ["scroll", "down", "600"],
        ["scroll", "down", "600"],
        ["scroll", "up", "1000000"],
    ]
    read = next(command for command in capture if command[:2] == ["eval", "--stdin"])
    assert capture.index(read) < capture.index(stop)
    assert commands[-1] == ["close"]
    closing = calls[-1].flags
    assert isinstance(closing, dict) and closing.get("--session") in sessions


def test_browser_always_sends_the_first_request_to_the_browser(
    site: Site, tmp_path: Path
) -> None:
    site.html("/b/", "<p>served over HTTP</p>")
    browser = FakeBrowser.at(tmp_path / "browser")
    serve_the_rendered_page(site, browser)

    result = mirror(
        tmp_path, "--output=out", "--browser=always", site.url("/b/"), browser=browser
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert site.requests == [], "no HTTP attempt"
    assert browser.opened()[0] == site.url("/robots.txt")
    rows = {row["url"]: row for row in manifest(tmp_path / "out")}
    assert (rows[site.url("/b/")]["fetcher"], rows[site.url("/b/")]["rung"]) == (
        "browser",
        3,
    )
    assert (
        "<script" not in (site.tree(tmp_path / "out") / "b" / "index.html").read_text()
    )


CHALLENGE = "<html><head><title>Just a moment...</title></head><body><p>Checking</p></body></html>"


def serve_the_challenged_page(site: Site, browser: FakeBrowser) -> None:
    """A page the headless browser meets a challenge on, and a headed one gets past."""

    url = site.url("/x/")
    site.gate = lambda request: FORBIDDEN
    browser.serve(
        url,
        dom=CHALLENGE,
        status=403,
        har=[har_entry(url, "Document", CHALLENGE, "text/html", status=403)],
        headed_dom="<html><head><title>X</title></head><body><p>real</p></body></html>",
        headed_status=200,
        headed_har=[har_entry(url, "Document", "<p>real</p>", "text/html")],
    )


def test_a_challenge_in_the_headless_browser_ends_blocked_and_names_headed(
    site: Site, tmp_path: Path
) -> None:
    browser = FakeBrowser.at(tmp_path / "browser")
    serve_the_challenged_page(site, browser)

    result = mirror(
        tmp_path, "--output=out", "--no-sitemap", site.url("/x/"), browser=browser
    )

    assert result.returncode == 1, (result.stdout, result.stderr)
    assert not any(call.flags.get("--headed") for call in browser.calls())
    assert "rung 3 was not enough" in result.stdout
    command = (
        f"/mirror --output=out --no-sitemap --headed {shlex.quote(site.url('/x/'))}"
    )
    assert command in result.stdout.splitlines(), result.stdout
    assert any(
        "--headed" in line and site.url("/x/") in line and line != command
        for line in result.stdout.splitlines()
    ), "a line names the URLs still blocked and --headed as the next step"
    assert not (tmp_path / "out").exists(), "a blocked start page writes nothing"

    # A blocked page that is not the start page is recorded `blocked` on rung 3.
    site.gate = lambda request: FORBIDDEN
    browser.serve(
        site.url("/y/"),
        dom='<body><a href="/x/">X</a></body>',
        har=[
            har_entry(site.url("/y/"), "Document", "<a href='/x/'>X</a>", "text/html")
        ],
    )
    result = mirror(
        tmp_path, "--output=out", "--include=/x/", site.url("/y/"), browser=browser
    )

    assert result.returncode == 1, (result.stdout, result.stderr)
    row = {row["url"]: row for row in manifest(tmp_path / "out")}[site.url("/x/")]
    assert (row["outcome"], row["fetcher"], row["rung"]) == ("blocked", "browser", 3)
    assert (
        f"/mirror --output=out --include=/x/ --headed {site.url('/y/')}"
        in result.stdout.splitlines()
    )


def test_headed_takes_a_host_the_headless_browser_is_challenged_on_to_rung_four(
    site: Site, tmp_path: Path
) -> None:
    browser = FakeBrowser.at(tmp_path / "browser")
    serve_the_challenged_page(site, browser)
    profile = tmp_path / "profile"

    result = mirror(
        tmp_path,
        "--output=out",
        "--headed",
        f"--profile={profile}",
        site.url("/x/"),
        browser=browser,
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    opens = [
        call for call in browser.calls() if call.command == ["open", site.url("/x/")]
    ]
    assert [bool(call.flags.get("--headed")) for call in opens] == [False, True]
    for call in opens:
        assert call.flags.get("--profile") == str(profile), call
    row = {row["url"]: row for row in manifest(tmp_path / "out")}[site.url("/x/")]
    assert (row["outcome"], row["fetcher"], row["rung"]) == ("fetched", "browser", 4)
    assert "real" in (site.tree(tmp_path / "out") / "x" / "index.html").read_text()
    assert "climbed to rung 4" in result.stdout


def patched_mirror(
    cwd: Path, overrides: dict[str, float], *args: str, browser: FakeBrowser
) -> subprocess.CompletedProcess[str]:
    """Run the engine with some of its module constants replaced, as `uv run` would run it."""

    source = ENGINE.read_text(encoding="utf-8")
    block = source[
        : source.index("# ///\n", source.index("# /// script")) + len("# ///\n")
    ]
    driver = cwd.parent / f"{cwd.name}-driver.py"
    driver.write_text(
        block
        + "import importlib.util, sys\n"
        + f"spec = importlib.util.spec_from_file_location('mirror', {str(ENGINE)!r})\n"
        + "module = importlib.util.module_from_spec(spec)\n"
        + "sys.modules['mirror'] = module\n"
        + "spec.loader.exec_module(module)\n"
        + "".join(f"module.{name} = {value!r}\n" for name, value in overrides.items())
        + "sys.exit(module.main(sys.argv[1:]))\n",
        encoding="utf-8",
    )
    return subprocess.run(
        ["uv", "run", "--quiet", str(driver), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        timeout=300,
        env={**os.environ, **browser.env},
    )


def test_a_headed_page_still_a_challenge_when_the_wait_ends_is_blocked(
    site: Site, tmp_path: Path
) -> None:
    browser = FakeBrowser.at(tmp_path / "browser")
    serve_the_challenged_page(site, browser)
    url = site.url("/x/")
    browser.serve(
        url,
        dom=CHALLENGE,
        status=403,
        har=[har_entry(url, "Document", CHALLENGE, "text/html", status=403)],
        headed_dom=CHALLENGE,
        headed_status=403,
        headed_har=[har_entry(url, "Document", CHALLENGE, "text/html", status=403)],
    )
    work = tmp_path / "work"
    work.mkdir()

    began = time.monotonic()
    result = patched_mirror(
        work,
        {"HEADED_WAIT": 1.0, "HEADED_POLL": 0.2},
        "--output=out",
        "--no-sitemap",
        "--no-feeds",
        "--headed",
        site.url("/x/"),
        browser=browser,
    )

    assert result.returncode == 1, (result.stdout, result.stderr)
    assert time.monotonic() - began < 120
    headed_reads = [
        call
        for call in browser.calls()
        if call.command[:1] == ["eval"] and call.flags.get("--headed")
    ]
    assert len(headed_reads) >= 3, "the headed page is polled until the wait ends"
    assert "rung 4 was not enough" in result.stdout


@pytest.mark.parametrize("flag", ["--headed", "--profile=Default"])
def test_a_browser_flag_with_browser_never_is_refused(
    site: Site, tmp_path: Path, flag: str
) -> None:
    site.html("/n/", "<p>n</p>")
    browser = FakeBrowser.at(tmp_path / "browser")
    work = tmp_path / "work"
    work.mkdir()

    result = mirror(work, "--browser=never", flag, site.url("/n/"), browser=browser)

    assert result.returncode == 2, (result.stdout, result.stderr)
    assert flag.partition("=")[0] in result.stdout.splitlines()[0]
    assert result.stdout.rstrip("\n").endswith("see '/mirror --help'")
    assert site.requests == [] and browser.calls() == []
    assert list(work.iterdir()) == []


def test_no_browser_to_launch_stops_the_run_before_it_fetches(
    site: Site, tmp_path: Path
) -> None:
    site.html("/b/", "<p>b</p>")
    browser = FakeBrowser.at(tmp_path / "browser")
    browser.lacks_a_browser()
    work = tmp_path / "work"
    work.mkdir()

    result = mirror(
        work, "--output=out", "--browser=always", site.url("/b/"), browser=browser
    )

    assert result.returncode == 2, (result.stdout, result.stderr)
    assert "agent-browser install" in result.stdout
    assert site.requests == []
    assert browser.commands() == [["doctor", "--json"]]
    assert list(work.iterdir()) == []

    # Under `auto`, the check waits for the first climb to the browser, and still writes nothing.
    site.gate = lambda request: FORBIDDEN
    result = mirror(work, "--output=out", site.url("/b/"), browser=browser)

    assert result.returncode == 2, (result.stdout, result.stderr)
    assert "agent-browser install" in result.stdout
    assert [
        command for command in browser.commands() if command[:1] != ["doctor"]
    ] == []
    assert list(work.iterdir()) == []


def test_the_session_is_closed_when_the_engine_is_interrupted(
    site: Site, tmp_path: Path
) -> None:
    browser = FakeBrowser.at(tmp_path / "browser")
    browser.serve(site.url("/robots.txt"), hang=True)
    work = tmp_path / "work"
    work.mkdir()

    engine = subprocess.Popen(
        ["uv", "run", "--quiet", str(ENGINE), "--browser=always", site.url("/h/")],
        cwd=work,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, **browser.env},
    )
    try:
        deadline = time.monotonic() + 120
        while not browser.opened():
            assert engine.poll() is None, engine.communicate()
            assert time.monotonic() < deadline, "the engine never opened the page"
            time.sleep(0.1)
        session = next(
            call.flags["--session"]
            for call in browser.calls()
            if call.command[:1] == ["open"]
        )
        os.kill(int(str(session).rpartition("-")[2]), signal.SIGTERM)
        engine.communicate(timeout=60)
    finally:
        if engine.poll() is None:
            engine.kill()
            engine.communicate()

    closes = [call for call in browser.calls() if call.command == ["close"]]
    assert [call.flags.get("--session") for call in closes] == [session]


def test_a_page_a_browser_fetched_is_fetched_again_on_the_next_run(
    site: Site, tmp_path: Path
) -> None:
    url = site.url("/v/")
    site.add("/v/", Response(b"<p>v</p>", headers={"ETag": '"v1"'}))
    browser = FakeBrowser.at(tmp_path / "browser")
    browser.serve(
        url,
        dom="<html><body><p>v</p></body></html>",
        har=[
            har_entry(
                url, "Document", "<p>v</p>", "text/html", headers={"ETag": '"v1"'}
            )
        ],
    )

    first = mirror(tmp_path, "--output=out", "--browser=always", url, browser=browser)
    second = mirror(tmp_path, "--output=out", url, browser=browser)

    assert first.returncode == 0, (first.stdout, first.stderr)
    assert second.returncode == 0, (second.stdout, second.stderr)
    asked = site.requested("/v/")
    assert len(asked) == 1 and "If-None-Match" not in asked[0].headers
    row = {row["url"]: row for row in manifest(tmp_path / "out")}[url]
    assert (row["outcome"], row["fetcher"]) == ("fetched", "http")


def test_the_manpage_states_the_browser_rungs() -> None:
    page = (SKILL / "help.md").read_text(encoding="utf-8")
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    synopsis = page.partition("\n## SYNOPSIS\n")[2].partition("\n## ")[0]
    options = page.partition("\n## OPTIONS\n")[2].partition("\n## ")[0]
    arguments = body.partition("## Arguments")[2].partition("\n## ")[0]
    for flag, hint in (
        ("[**--headed**]", "[--headed]"),
        ("[**--profile=**_PROFILE_]", "[--profile=<name>|<path>]"),
    ):
        assert flag in synopsis, flag
        assert flag.strip("[]") in options, flag
        assert hint in body, hint
    for flag in ("`--headed`", "`--profile`", "`always`"):
        assert flag in arguments, flag
    description = page.partition("\n## DESCRIPTION\n")[2].partition("\n## ")[0]
    for statement in (
        "rung 3",
        "rung 4",
        "`agent-browser`",
        "`script` element",
        "`noscript`",
        "application traffic",
        "fetched again",
        "ten minutes",
    ):
        assert statement in description, statement
    dependencies = page.partition("\n## DEPENDENCIES\n")[2].partition("\n## ")[0]
    assert "`agent-browser`" in dependencies and "agent-browser install" in dependencies
    frontmatter = body.partition("\n---\n")[0]
    assert 'kntnt.binaries: "uv agent-browser"' in frontmatter
    assert re.search(r"^compatibility: .*\bagent-browser\b", frontmatter, re.MULTILINE)
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    dependencies = readme.partition("\n## Dependencies\n")[2].partition("\n## ")[0]
    assert "`mirror` requires `agent-browser`" in dependencies
