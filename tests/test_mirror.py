"""The mirror engine, driven against fixture sites a local HTTP server serves.

The engine is run the way its Skill runs it, through `uv run`, which gives it
the dependencies its PEP 723 block pins; the test interpreter has none of them.
Every site is served from `127.0.0.1` on a port the operating system picks, and
`localhost` on the same port stands in for a second host, so no test reaches
the network.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import threading
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


class Site:
    """A fixture site: routes by host-free request path, and what arrived."""

    def __init__(self) -> None:
        self.routes: dict[str, list[Response]] = {}
        self.requests: list[Request] = []
        self.port = 0

    def add(self, path: str, *responses: Response) -> None:
        """Serve *responses* at *path* in turn, the last one from then on."""

        self.routes[path] = list(responses)

    def html(self, path: str, markup: str) -> None:
        self.add(path, Response(markup.encode()))

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
            served.requests.append(
                Request(self.headers.get("Host", ""), self.path, dict(self.headers))
            )
            responses = served.routes.get(self.path)
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
<a href="about">About</a>
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
    site.html("/site/about", "<p>About</p>")


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
    assert [request.path for request in site.requests] == ["/p/"]
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
    assert anchors == [site.url("/site/about")]
    assert not site.requested("/site/about")


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
    assert len(by_url) == len(rows) == 4

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
    assert len(site.requests) == 9
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
    assert len(site.requests) == 9
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
    assert [request.path for request in site.requests] == ["/n/", "/n/img/a.png"]
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
    start = manifest(tmp_path / "out")[0]
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
