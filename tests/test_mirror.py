"""The mirror engine, driven against fixture sites a local HTTP server serves.

The engine is run the way its Skill runs it, through `uv run`, which gives it
the dependencies its PEP 723 block pins; the test interpreter has none of them.
Every site is served from `127.0.0.1` on a port the operating system picks, and
`localhost` on the same port stands in for a second host, so no test reaches
the network. A crawl needs three names on that one server, and takes them under
`.localhost`, which resolves to the loopback address: `mirror.localhost` as the
root host, `www.mirror.localhost` as its other form, and `other.mirror.localhost`
as another subdomain. The server answers by the name in the `Host` header.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import threading
import time
from collections.abc import Iterator
from dataclasses import dataclass, field
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest

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
}

# The attributes a saved page references another file through.
REFERENCE_ATTRIBUTES = {"href", "src", "srcset", "poster", "data", "action"}


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


@pytest.fixture
def site() -> Iterator[Site]:
    """Serve a fresh fixture site for one test, and stop it afterwards."""

    served = Site()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            host = self.headers.get("Host", "")
            served.requests.append(Request(host, self.path, dict(self.headers)))
            responses = served.host_routes.get(
                (host.rpartition(":")[0], self.path)
            ) or served.routes.get(self.path)
            if not responses:
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            response = responses.pop(0) if len(responses) > 1 else responses[0]
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


def mirror(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run the engine as its Skill does, from *cwd*."""

    return subprocess.run(
        ["uv", "run", "--quiet", str(ENGINE), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        timeout=300,
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

    result = mirror(tmp_path, "--output=out", site.url("/site/"))

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

    result = mirror(tmp_path, "--output=out", site.url("/site/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    tags = read_page(site.tree(tmp_path / "out") / "site" / "index.html").tags
    assert not [tag for tag, _ in tags if tag == "base"]
    link = next(attributes for tag, attributes in tags if tag == "link")
    script = next(attributes for tag, attributes in tags if tag == "script")
    assert "integrity" not in link
    assert script["integrity"] == SCRIPT_INTEGRITY


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
    assert [request.path for request in site.requests] == ["/robots.txt", "/p/"]
    page = site.tree(nothing / "out") / "p" / "index.html"
    references = [reference for _, _, reference in read_page(page).references]
    assert references == [logo, site.url("/p/here.png"), site.url("/elsewhere/x.png")]


def test_a_link_to_a_page_outside_the_mirror_stays_absolute(
    site: Site, tmp_path: Path
) -> None:
    serve_the_full_page(site)

    result = mirror(tmp_path, "--output=out", site.url("/site/"))

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


def test_html_and_css_keep_their_bytes_as_served_and_nothing_else_does(
    site: Site, tmp_path: Path
) -> None:
    serve_the_full_page(site)

    result = mirror(tmp_path, "--output=out", site.url("/site/"))

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
    assert len(by_url) == len(rows) == 5

    start = by_url[site.url("/site/")]
    assert (start["kind"], start["source"], start["outcome"]) == (
        "page",
        "start",
        "fetched",
    )
    assert start["fetcher"] == "http" and start["status"] == 200
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

    dry = mirror(tmp_path, "--dry-run", site.url("/site/"))

    assert dry.returncode == 0, (dry.stdout, dry.stderr)
    assert list(tmp_path.iterdir()) == []
    for path in ("/site/", "/site/css/theme.css", "/site/img/bg.png"):
        assert site.url(path) in dry.stdout, path

    real = mirror(tmp_path, site.url("/site/"))

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

    result = mirror(tmp_path, "--output=a", site.url("/site/"))

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert len(site.requests) == 10
    assert {request.headers["User-Agent"] for request in site.requests} == {IDENTITY}

    site.requests.clear()
    result = mirror(
        tmp_path,
        "--output=b",
        "--header=X-Token: secret",
        "--header=Cookie: session=1",
        "--user-agent=fixture-bot/2",
        site.url("/site/"),
    )

    assert result.returncode == 0, (result.stdout, result.stderr)
    assert len(site.requests) == 10
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

    result = mirror(tmp_path, "--output=out", site.url("/n/"))

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

    result = mirror(tmp_path, "--output=out", site.url("/site/"))

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


def test_an_unreadable_robots_txt_allows_everything_and_is_reported(
    site: Site, tmp_path: Path
) -> None:
    site.add("/robots.txt", Response(b"", status=503, headers={"Retry-After": "0"}))
    site.html("/u/", '<a href="next">Next</a>')
    site.html("/u/next", "<p>next</p>")

    result = mirror(tmp_path, "--output=out", site.url("/u/"))

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

    result = mirror(tmp_path, "--output=out", site.url("/s/"))

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
