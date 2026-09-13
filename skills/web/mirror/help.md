# mirror

## NAME

mirror - copy a web page, the pages under it, and everything they need to disk, browsable offline

## SYNOPSIS

**/mirror** [**--output=**_DIR_] [**--resources=**_all_|_in-scope_|_none_] [**--max-pages=**_N_] [**--delay=**_SECONDS_] [**--no-links**] [**--no-sitemap**] [**--no-feeds**] [**--ignore-robots**] [**--include=**_REGEX_ ...] [**--exclude=**_REGEX_ ...] [**--header=**_HEADER_ ...] [**--user-agent=**_STRING_] [**--browser=**_auto_|_always_|_never_] [**--headed**] [**--profile=**_PROFILE_] [**--dry-run**] *URL* [**--** *INSTRUCTION*]

## DESCRIPTION

`mirror` copies a web page, and every page under it that its links, the site's sitemaps and its feeds reach, to disk so that it can be opened in a browser with nothing fetched from the network: an archive of a section as it looked, a copy to read without a connection, or a snapshot to work from.

It follows the URL's redirects, and the page where they end is the start page. From there it crawls, one request at a time and breadth first: it saves the start page and every page and file in scope that a link, a sitemap or a feed names, together with everything each page needs to display: images, including those named in `srcset` and `picture`, stylesheets, scripts, fonts, video, audio, posters, text tracks, icons, preloaded files, the web manifest, and what `iframe`, `object` and `embed` show. Everything a stylesheet references through `url()` and `@import` is fetched too, recursively, and so is every `url()` in a `style` attribute. A resource is fetched whatever host it is on, unless **--resources** or **--exclude** says otherwise; a browser on rung 3 or 4 loads what a page needs itself, and there the two say what of it is saved.

Pages are found three ways, and a page found any of them is a candidate. Links are read from every fetched HTML page in scope: from `a` and `area` elements with `href`, and from `link` elements whose `rel` is `next`, `prev`, `canonical` or `alternate`, except an `alternate` that names a feed, which is read as a feed and never taken as a page. Sitemaps and feeds name the rest, as the next two paragraphs say. A candidate is normalised and tested against the scope: one in scope that has not been seen is fetched, and one out of scope is recorded in the manifest as `out-of-scope`, or as `excluded` where an **--exclude** matches it, and never fetched, though a browser on rung 3 or 4 may already have requested an excluded one while it loaded a page. An HTML page in scope is read for links and feeds in turn, and anything else in scope, a PDF for instance, is saved as it is. A candidate in scope that redirects out of scope is recorded as `redirect-out`, and where it leads is not fetched over plain HTTP; in a browser, which follows the redirect itself, it has already been requested, and nothing of it is saved. **--no-links** turns links off as a source: every fetched page is still read for its resources and its feeds, and the pages fetched are the start page and those sitemaps and feeds name. With **--no-links**, **--no-sitemap** and **--no-feeds** together, the start page and its resources are all that is fetched.

Sitemaps are read after the start page is fetched and before the crawl goes on from it. Every `Sitemap:` line in the `robots.txt` of the start page's host names one, under **--ignore-robots** too, and `/sitemap.xml`, `/sitemap_index.xml` and `/wp-sitemap.xml` at the root of that host are tried on every run, whatever `robots.txt` names. A sitemap index is followed recursively, a gzip-compressed sitemap is read as well as a plain one, and every `loc` in a URL set is a candidate. Each sitemap is read once, so an index that names itself ends. A sitemap on another host is read anyway, and the scope decides about the URLs it names. **--no-sitemap** reads none.

Feeds are named in two ways: by a `link` element with `rel="alternate"` and `type` `application/rss+xml` or `application/atom+xml` on any fetched HTML page in scope, and by `/feed/` at the root of the start page's host and `/feed/` under the root prefix, which are tried on every run. Each feed is read once, on whatever host it is, and the link of every RSS item and Atom entry in it is a candidate. **--no-feeds** reads none.

A sitemap or feed is fetched with the run's identity and headers and obeys `robots.txt`, as a page does. It is recorded in the manifest with the kind `sitemap` or `feed` and never saved in the tree. One of the well-known locations above that answers `404` or `410` is recorded as `missing`, which is no failure: most sites have only some of them. A sitemap or feed that fails any other way, or that something named and answers `404`, is a failure. A document that is not the XML of a sitemap or feed, such as a page a server answers every unknown path with, names no candidate and fails nothing.

Every reference in the saved HTML and CSS that points at a file in the mirror is rewritten to a relative path, a link to another saved page included, so the copy works from wherever it is put. A reference to anything not in the mirror, such as a link to a page out of scope, is left as an absolute URL: following it leaves the mirror deliberately, and nothing is fetched by itself. `base` elements are honoured when references are resolved, and removed afterwards. An `integrity` attribute is removed where the rewrite changed the bytes of the file it guards, and kept otherwise.

The start page's directory is the root. If the start page's path ends in a slash, that path is the root prefix; otherwise the prefix is the path up to and including its last slash, and the start page itself is always in scope. End the URL with a slash to make it a directory root. A URL lies under the root when its host is the start page's host, its port is the start page's, its scheme is `http` or `https`, and its path starts with the root prefix. Every other subdomain is another site. A URL is in scope when it lies under the root or matches any **--include**, and matches no **--exclude**; a URL an **--include** matches must still be `http` or `https`. **--exclude** wins over everything, the root and every **--include** alike, but may not match the start page, which is always in scope. The same scope governs pages, files, sitemaps, feeds and resources: a page an **--include** brings in is fetched and read for links, feeds and resources like a page under the root, and an **--include** widens the scope without naming a page, so a page it matches is fetched only when a link, a sitemap or a feed names it. Over plain HTTP an excluded URL is never requested, whether a link, a sitemap, a feed, a page's resources or a redirect other than the start page's led to it, and robots.txt is not consulted for it; a browser on rung 3 or 4 may already have requested one while it loaded a page or followed a redirect, and it is still recorded and never saved; one a link, a sitemap, a feed or a page's resources named is recorded in the manifest as `excluded`, even where it lies outside the root or `robots.txt` disallows it, and a reference to it is left absolute. A page, file, resource, sitemap or feed whose redirect leads to an excluded URL stops there over plain HTTP, and in a browser, which follows the redirect itself, nothing of it is saved; either way it is recorded as `redirect-out`, except the start page's redirects, which are followed to their end, where an **--exclude** that matches is refused as DIAGNOSTICS says. A sitemap or feed an **--exclude** matches is not read.

Patterns are compiled by the Python module `regex`, so Perl syntax works in them: possessive quantifiers, recursion, `\K` and Unicode classes among it. A pattern is matched against the normalised absolute URL, the form the next paragraph describes, and unanchored, so it matches anywhere in the URL unless it says otherwise: `^https://ir\.x\.se/` needs its `^` to match only URLs that start there. Matching is case-sensitive unless the pattern says otherwise, and the scheme is part of what is matched, so a pattern that names `https` matches no `http` URL.

Before URLs are compared, the scheme and host are put in lower case, the fragment, the default port and the credentials are removed, dot segments are resolved, percent-encoding is made canonical, `index.html` and `index.php` are read as their directory, and the tracking parameters `utm_*`, `fbclid`, `gclid`, `mc_cid` and `mc_eid` are removed. Every other query parameter is kept, in its order. The start page's host with `www.` added or removed is then written as the start page's host, in the form the start page's final URL has, so `www.x.se` and `x.se` are one site: a page reached through the other form is fetched and saved once, under the start page's host directory, and the tree has no directory for the other form. Only that host folds; `www.` on any other host is left alone. A URL is fetched once, in that form.

Before a page, file, sitemap or feed is fetched from a host, the start page included, the host's `robots.txt` is read, once per run, with the run's identity and headers, and obeyed. A URL it disallows is recorded as `robots` and not fetched, and the report counts them. The rules are those of the group whose `User-agent` line most specifically matches the run's product token, and those of the `*` group only where no group matches, as RFC 9309 says; the longest matching rule decides, and `Allow` wins a tie. The product token is `kntnt-mirror`, or the first word of **--user-agent** without its version. A `Crawl-delay` longer than **--delay** is honoured for its host. A `robots.txt` that answers with any `4xx` status other than a block allows everything; one that answers `5xx`, or not at all after the retries, or that is still blocked on the highest rung, allows everything too, and the report says it could not be read. Resources are exempt: they are fetched on behalf of a page a person would load, and a `Disallow: /` on a CDN would otherwise break the copy without a word. The file itself is recorded in the manifest and never saved in the tree. **--ignore-robots** turns every rule and `Crawl-delay` off, and the file is still read.

A page's own robots directives are obeyed too, in its `meta` elements named `robots` or `kntnt-mirror` and in every `X-Robots-Tag` header its answer carries, a header value that opens with another crawler's name and a colon binding that crawler alone. A page marked `nofollow` or `none` is saved, and its resources are fetched, but no link or feed it names is followed from it; the report counts those pages. `noindex` asks search engines to leave a page out of their index and binds no copy, so it is not obeyed. A `rel="nofollow"` on a single link is not obeyed either. **--ignore-robots** obeys none of these directives.

The crawl stops taking new pages at a cap, 5000 pages and files unless **--max-pages** says otherwise, the start page among them; resources, sitemaps and feeds do not count. A page or file counts when it is admitted to the crawl, whichever source named it, so under a cap of *N* exactly *N* are fetched, however many URLs a sitemap lists. When the cap is reached, discovery stops, what is already queued is fetched, every candidate found afterwards is recorded as `over-cap`, and the report says the cap was reached and what it was.

An HTML page fetched over plain HTTP with at least one `script` element and fewer than 200 characters of text outside `script`, `style`, `noscript` and `template` elements, whitespace collapsed, is counted as a suspected JavaScript shell: what it shows is likely drawn by a script, which plain HTTP does not run. A page a browser fetched is saved without its `script` elements and is never counted. The report says how many there were. It is a warning, and the run does not fail for it.

On a file system that treats names differing only in case as one, as macOS does by default, two URLs that differ only in case map to one file. The run tests the output directory once for it, and where the file system folds case, the later of two such files is saved with `~2`, `~3` and so on before its extension, `page.html` beside `Page.html` becoming `page~2.html`. Links to it are rewritten to that name and the manifest records it, but the name no longer matches the URL, and a copy moved to a file system that does not fold case keeps the suffixed name.

Requests go one at a time, over plain HTTP unless a host's rung is a browser, and **--delay** spaces them. Connecting and reading each time out after 30 seconds. A connection error, a timeout, and the statuses `429`, `500`, `502`, `503` and `504` are retried up to three times, after the wait `Retry-After` asks for or otherwise after 1, 2 and 4 seconds. Nothing else is retried.

Every host the run asks starts on the lowest rung the run may use, rung 1 unless **--browser=always** says otherwise, and climbs when it blocks the run. Rung 1 is plain HTTP with the Skill's own identity, the user-agent `kntnt-mirror (+https://github.com/Kntnt/skills)`. Rung 2 is plain HTTP dressed as Chrome on macOS: a current Chrome user-agent string with the headers a browser sends beside it, `Accept`, `Accept-Language` and the `sec-ch-ua` family. Rung 3 is a headless browser, and rung 4 a visible browser window, both a real Chrome driven through `agent-browser`, with the user's Chrome profile where **--profile** names one. **--user-agent** replaces the user-agent on every rung, the browser's included, and a **--header** whose name a rung also sets replaces that rung's header; in the browser, every **--header** is set for the whole session, so it goes with every request the browser makes, as on HTTP. The rung belongs to the host, a scheme, host name and port, and lasts the run: the next run starts every host on its first rung again, whatever the manifest says the last one ended on.

An answer is a block when, its retries spent, its status is `403`, `429` or `503`, or when it carries a marker a bot defence answers with. A `403` is not retried and is a block at once; a `429` or `503` is retried as above, after the wait its `Retry-After` asks for, and is a block only if it is still the answer when the retries are spent. The markers are those of Cloudflare, Akamai, PerimeterX (HUMAN), DataDome and Imperva (Incapsula), such as Cloudflare's header `cf-mitigated: challenge` and its challenge page's title `Just a moment...`, and the table of them is the engine's: a header marker is matched on every answer, a redirect included, a title marker on every HTML answer, whatever its status, and a marker in the body only on an HTML answer whose status is `403`, `429` or `503`, so a page that merely mentions one moves nothing. Matching is case-insensitive. A `robots.txt` disallow is not a block: it is the site's wish, and it is obeyed on every rung.

Every request counts, `robots.txt`, sitemaps and feeds as much as pages, files and resources, and the host a request is counted against is the one its URL names, whichever host its redirects end on. The first block on a host moves it one rung up: the blocked URL is asked again on the new rung at once, and every later request to that host goes there too. **--browser** decides which rungs the run may reach. Under `auto`, the default, a host climbs from rung 1 through rung 2 to rung 3, and to rung 4 only when **--headed** is given. Under `always`, every host starts on rung 3, or on rung 4 when **--headed** is given, and no request goes over plain HTTP. Under `never`, rung 2 is the ceiling and no browser is ever started. A URL still blocked on the highest rung the run can reach is recorded as `blocked` and fails the run as any failure does, except a `robots.txt`, which then allows everything. Where that rung is rung 3, the report names the URLs still blocked and prints the command to run next: the invocation as given with **--headed** added, on a line of its own, ready to paste.

Before its first browser fetch, the run asks `agent-browser doctor` whether it can launch a browser; where it cannot, the run stops, says to run `agent-browser install`, and writes nothing. The run keeps one `agent-browser` session of its own, named `kntnt-mirror-` and the engine's process id so that it cannot touch a session of the user's, and closes it when the run ends, however it ends, an interrupt included.

A host on rung 3 or 4 is fetched only through the browser: its pages, its files, the resources a page names on it, its `robots.txt`, its sitemaps and its feeds. For each URL the browser starts a HAR recording that keeps every response body, opens the URL, waits for the network to go quiet, scrolls once to the bottom so that lazily loaded content loads, reads the rendered DOM and stops the recording. A page is saved as that rendered DOM, with its doctype, and with every `script` element removed and every `noscript` element kept: a script run again against a DOM that already holds its output breaks the page more often than it completes it. Its resources are those the browser actually fetched while it loaded, taken from the recording without another request and saved at their URL paths as **--resources** and **--exclude** allow, together with every resource a reading of the rendered DOM finds, as on HTTP; a resource the recording lacks is fetched on the rung of its own host. What the recording holds as a document, stylesheet, image, font, media, script, manifest or text track is saved; an XHR or `fetch` answer, a WebSocket, an event stream, a ping and anything else the browser calls other are not, since no script remains in the saved page to read them, and neither is an entry of no type whose content is JSON. Links are read from the rendered DOM, so a link only a script draws is followed. A file that is no HTML, opened in the browser, is saved as the recording holds its bytes. A browser follows redirects itself, so one that leads out of scope has already been requested when it is recorded as `redirect-out`, and nothing of it is saved.

With **--headed**, the browser window is visible, so that the person at it can pass a challenge or log in. On each page it opens, the run waits until the page is no longer a challenge, looking every two seconds, for at most ten minutes, and treats a page that is still one then as blocked. A challenge is what the table of markers above calls a block, judged on the page as it stands.

A rerun into an output directory that holds an earlier run's manifest is incremental: discovery is done in full every run, and only fetching is conditional. Every URL the run comes to whose row in that manifest names a saved file that is still there, and for an HTML page or a stylesheet its copy under `.mirror/raw/` too, is requested with `If-None-Match` from the row's `ETag` and `If-Modified-Since` from its `Last-Modified`, whichever of the two the row has; a row with neither, and a URL the manifest does not know, are fetched as on a first run. A `304` keeps the file as it is and records the URL as `unchanged`, carrying the earlier row's `ETag`, `Last-Modified`, digest, size and content type, replaced by whatever the `304` itself supplies, so the run after it is as conditional; an unchanged page or stylesheet is read for links and resources from its raw copy, as a fetched one is. Any other success replaces the file and, for HTML and CSS, its raw copy. The rewrite runs over every raw file, unchanged ones included, so a reference left absolute because its target was not yet in the mirror becomes relative once the target is, and it writes a file only where its bytes differ, so an unchanged file keeps its modification time. A URL an earlier run saved that this run did not discover keeps its file on disk and is recorded as `absent`: nothing is ever deleted from the tree. A browser makes no conditional request, and a row whose `fetcher` is `browser` sends none on the next run either: a page, file or resource a browser fetched is fetched again on every rerun.

On plain HTTP, resources a script loads while the page runs cannot be found by reading the page, and are not saved; the saved page asks the network for them, or goes without. In the browser, those it loaded are saved, as the paragraphs on rungs 3 and 4 say, but a saved page runs no script.

Chrome restricts fonts and `type="module"` scripts on pages opened as `file://`. For full fidelity, serve the output directory with any static file server, such as `python3 -m http.server`, and open the page through it.

When the run ends, the Skill prints a short report: the pages, files and resources fetched, their total size, the pages, files and resources a conditional request found unchanged, how many sitemaps and feeds were read, how many candidates links, sitemaps and feeds each contributed, counting each URL once under the source that named it first, how many candidates were out of scope, excluded, redirected out of scope, stopped by `robots.txt` and over the cap, how many pages' links a `nofollow` kept unfollowed, how many saved files are absent, whether the cap was reached, how many pages were suspected shells, how many URLs ended `blocked`, how many hosts stayed on rung 1, a line for every host that climbed, started above rung 1 or ended blocked naming the rung, 1 to 4, it ended on and the status or marker that moved it, and saying where that rung was not enough, the URLs still blocked in the headless browser with the command that adds **--headed**, any `robots.txt` that could not be read, and every failure with its status, or for a blocked URL what blocked it, and URL.

## POSITIONAL ARGUMENTS

*URL*

The page to mirror. It is required, and absolute with the scheme `http` or `https`. A user name and password for basic auth may stand in it, and are sent to the start page's host only.

## OPTIONS

**--output=**_DIR_

Write the mirror to *DIR*. Defaults to `./`*HOST* in the working directory, *HOST* being the start page's host.

**--resources=**_all_|_in-scope_|_none_

Say which resources are fetched. `all`, the default, fetches every resource the page needs, whatever host it is on. `in-scope` fetches only the resources that are in scope, as DESCRIPTION defines it. `none` fetches no resource. On rungs 3 and 4 the browser loads every resource a page needs itself, and the value says which of them are saved. With `in-scope` and `none`, a resource that is left out keeps its absolute reference in the saved page, so the promise that nothing is fetched from the network does not hold for it.

**--max-pages=**_N_

Fetch at most *N* pages and files, the start page among them; resources do not count. Defaults to `5000`, and `0` sets no cap. Candidates found once the cap is reached, from links, sitemaps or feeds, are recorded as `over-cap` and not fetched.

**--delay=**_SECONDS_

Wait *SECONDS*, a number of 0 or more, between one request and the next. Defaults to `0`. A `Crawl-delay` in a host's `robots.txt` that is longer applies to that host instead.

**--no-links**

Follow no links. Pages are still read for their resources and feeds, and the pages fetched are the start page and those sitemaps and feeds name in scope. With **--no-sitemap** and **--no-feeds** as well, the start page is saved with its resources, and no other page or file is fetched.

**--no-sitemap**

Read no sitemap: neither those `robots.txt` names nor `/sitemap.xml`, `/sitemap_index.xml` and `/wp-sitemap.xml`, so a page only a sitemap names is not fetched.

**--no-feeds**

Read no feed: neither those a page names with `link rel="alternate"` nor `/feed/` at the host's root and under the root prefix, so a page only a feed names is not fetched.

**--ignore-robots**

Obey no `robots.txt` rule, no `Crawl-delay`, and no `nofollow` in a page's robots `meta` elements or `X-Robots-Tag` headers. The file is still read and recorded in the manifest.

**--include=**_REGEX_

Bring every `http` or `https` URL that *REGEX* matches into scope, beside the root's subtree, as DESCRIPTION says. Repeatable: a URL any of them matches is in. *REGEX* is written in the syntax of the Python module `regex` and matched, unanchored, against the normalised absolute URL, so `^https://ir\.x\.se/` needs its `^`.

**--exclude=**_REGEX_

Keep every URL that *REGEX* matches out: it is never requested over plain HTTP and never saved, though a browser on rung 3 or 4 may already have requested it while it loaded a page or followed a redirect, and the manifest records one a link, a sitemap, a feed or a page's resources named as `excluded`, and a URL whose redirect leads to it as `redirect-out`, except the start page's redirects, which are followed to their end, where a pattern that matches is refused as DIAGNOSTICS says. Repeatable: a URL any of them matches is out, whatever the root or an **--include** says. Written and matched as **--include** is. A pattern that matches the start page is refused.

**--header=**_HEADER_

Send *HEADER*, written `name: value`, with every request, to whatever host, each hop of a redirect included, on every rung. Repeatable. It covers `Authorization` and `Cookie`. A header whose name a rung also sets, such as `Accept-Language`, replaces the rung's.

**--user-agent=**_STRING_

Send *STRING* as the user-agent on every request, on every rung, in place of the Skill's own identity on rung 1, Chrome's on rung 2 and the browser's own on rungs 3 and 4. The headers rung 2 sends beside it stay.

**--browser=**_auto_|_always_|_never_

Say where a host may be fetched from. Defaults to `auto`, under which a host that blocks plain HTTP climbs to a headless browser, rung 3, and to a visible one, rung 4, only with **--headed**. `always` starts every host in the browser, on rung 3, or on rung 4 with **--headed**, and makes no request over plain HTTP. `never` keeps every host on HTTP, rungs 1 and 2, starts no browser, and reports a URL still blocked there as `blocked`.

**--headed**

Let the browser be a visible window, rung 4, where the person at it can pass a challenge or log in. Under `auto`, a host still blocked in the headless browser moves there; under `always`, every host starts there. On each page, the run waits until the page is no longer a challenge, for at most ten minutes, and treats it as blocked after that. Refused with **--browser=never**.

**--profile=**_PROFILE_

Run the browser with the Chrome profile *PROFILE*, a profile name such as `Default` or a directory path, a relative one read from the working directory, passed to `agent-browser --profile`, so that it carries the user's logins and a real browser's fingerprint. Applies on rungs 3 and 4. Refused with **--browser=never**.

**--dry-run**

Fetch and count everything a real run would, and write nothing: no output directory, no manifest, no log, and against an existing mirror no change to it. The report lists every URL that would be fetched, with the word `conditional` after each one that would be requested conditionally, as DESCRIPTION says, followed by the counts a real run prints.

## FILES

**<output>/<host>/**

One directory per host the mirror holds a file from, such as `x.se/` and `cdn.x.se/`. A host with a port other than its scheme's default is written with the port, as `x.se%3A8080/`. Under it, each file is at its URL's path, as on the site, with percent-encoding decoded.

**URL to path**

A directory URL, one whose path ends in a slash, is saved as `index.html` in that directory. An HTML page whose last path segment has no extension is saved with `.html` appended, so `/docs/guide` becomes `docs/guide.html`. A URL with a query string keeps it in the file name, placed before the extension so that the file keeps its type: `/style.css?v=2` becomes `style%3Fv=2.css`, `/?p=1` becomes `index%3Fp=1.html`, and a name with no extension ends with the query string. In every name, the characters a file name cannot hold on macOS or Linux are percent-encoded: `/`, NUL, `?`, `#`, `%`, `\`, `:`, `*`, `"`, `<`, `>`, `|` and every control character. Where one URL maps to a file whose path another URL needs as a directory, `/a` beside `/a/b`, the file is saved as that directory's `index.html` when it is HTML and with the suffix `~file`, as `a~file`, otherwise. Where the file system folds case, the later of two paths that differ only in case takes `~2`, `~3` and so on before its extension, as DESCRIPTION says. The manifest records the path every file got.

**<output>/.mirror/raw/**

The bytes of every HTML and CSS file as the server sent them, at the same relative path as in the tree; for a page a browser fetched, the rendered DOM with its scripts removed, which is what the tree's copy is derived from. The saved copies in the tree are derived from these at the end of every run, unchanged ones included. Images, fonts, scripts and every other file the rewrite never changes are kept in the tree only.

**<output>/.mirror/manifest.ndjson**

Rewritten whole every run: one JSON object per line, one per URL the run took a position on and one per URL an earlier run saved that this run did not discover, each with the same fields: `url`; `final_url`, where its redirects ended; `kind`, one of `page`, `file`, `resource`, `robots`, `sitemap` and `feed`, a candidate not fetched being a `page`; `source`, what led to it: `start`, `link`, `resource`, `robots` for a `robots.txt` and for a sitemap a `robots.txt` names, `sitemap`, `feed`, or `probe` for a sitemap or feed at a well-known location; `discovered_from`, the URL of the page, file, `robots.txt`, sitemap or feed that named it, or `null` for the start page, a `robots.txt` and a well-known location; `fetcher`, `http` on rungs 1 and 2 and `browser` on rungs 3 and 4, and `rung`, `1` to `4`, both those of the last request made for the URL, a resource taken from a browser's recording carrying the page's, so a URL blocked on rung 1 and fetched on rung 2 shows `2`, and both `null` for a URL no request was made for; `status`, `304` for an unchanged file; `content_type`; `charset`, the character encoding the server declared, which a rerun decodes an unchanged page or stylesheet with; `robots_tag`, every `X-Robots-Tag` header the answer carried, as a list, which a rerun obeys for a page a `304` found unchanged; `size` in bytes; `local_path`, relative to the output directory; `sha256`; `etag`; `last_modified`; `timestamp`; and `outcome`, one of `fetched`, `out-of-scope`, `excluded`, `redirect-out`, `robots`, `over-cap`, `missing`, `failed`, `blocked` for a URL still blocked on the highest rung, `unchanged` for a URL a conditional request found as the earlier run saved it, and `absent` for a file an earlier run saved whose URL this run did not discover, its row otherwise as that run left it. A field with nothing to say is `null`. A URL that normalises to one already recorded, a fragment or tracking-parameter variant for instance, gets no row of its own. A `robots.txt` that could not be read is `failed`, or `blocked` where a block kept it unread, without failing the run, and a well-known sitemap or feed location that is not there is `missing`.

**<output>/.mirror/run.log**

One line per request the run made, with its timestamp, method, URL, status and elapsed time, and one line per URL the manifest records as `out-of-scope`, `excluded`, `redirect-out`, `robots`, `over-cap`, `missing`, `failed`, `blocked` or `absent`, and one line per rung a host climbed, naming the host, the rung, what blocked it and the URL.

## EXIT STATUS

**0**

Everything was fetched: nothing the run set out to fetch failed.

**1**

The run completed and something failed or ended blocked, as the report names, or the start page could not be fetched, blocked on the highest rung included, or is disallowed by `robots.txt`, in which case nothing is written.

**2**

The form was invalid, a value was refused, or a dependency is missing. Nothing is written.

**3**

The help page was printed.

## DIAGNOSTICS

An invalid, incomplete, or out-of-order form is refused rather than repaired or ignored. The Skill names the error, prints the SYNOPSIS, writes nothing, and points to `/mirror --help`. A flag is refused rather than ignored where it has no work to do here, and a flag written after the URL is out of order.

A URL that is not absolute with `http` or `https`, a **--resources** value other than `all`, `in-scope` and `none`, a **--header** without a colon, a **--delay** that is not a number of 0 or more, a **--max-pages** that is not a whole number of 0 or more, a **--browser** value other than `auto`, `always` and `never`, a **--headed** or **--profile** given with **--browser=never**, an empty **--profile**, an **--include** or **--exclude** pattern that the `regex` module cannot compile, and an **--exclude** that matches the start page are refused the same way, before anything is fetched; a refused pattern is named with the compiler's error. An **--exclude** that matches only where the start page's redirects end is refused the same way once they are followed, and nothing is written.

A start page that cannot be fetched, or that `robots.txt` disallows, is reported with the reason, and nothing is written; one still blocked in the headless browser is reported with the command that adds **--headed**. Where a host needs the browser and `agent-browser` is not installed or cannot launch a browser, the run stops on exit 2 with the instruction to run `agent-browser install`, and nothing is written. A resource that cannot be fetched is named in the report with its status, or with the error where there was no answer, and the run goes on.

## EXAMPLES

Mirror a section, every page under `/docs/` its links, sitemaps and feeds reach and everything those pages need, into `./example.com`:

```text
/mirror https://example.com/docs/
```

Mirror one page and what it needs, and no other page:

```text
/mirror --no-links --no-sitemap --no-feeds https://example.com/articles/launch
```

Mirror a blog's posts from its sitemaps and feeds only, following no link:

```text
/mirror --no-links https://example.com/blog/
```

Crawl a large site gently, a second between requests and at most 200 pages:

```text
/mirror --max-pages=200 --delay=1 https://example.com/
```

See what a mirror of a section would fetch, keeping only the resources that lie under it, without writing anything:

```text
/mirror --resources=in-scope --dry-run https://example.com/docs/
```

Mirror a site's docs together with its investor-relations subdomain, leaving out the drafts under both:

```text
/mirror --include='^https://ir\.x\.se/' --exclude='/drafts/' https://x.se/docs/
```

Mirror a site behind a bot challenge in a visible browser with your own Chrome profile, passing the challenge by hand where one appears:

```text
/mirror --headed --profile=Default https://example.com/
```

Mirror a page behind a login, with the session cookie:

```text
/mirror --output=~/Archive/intranet --header="Cookie: session=abc123" https://intranet.example.com/
```

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate. Here it can add no flag, change no flag's value, and supply no URL; it may only shape how the report is relayed.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv`, which runs the Manager's invocation engine and this Skill's own, and gives the engine the libraries it pins. `agent-browser`, which drives the browser on rungs 3 and 4: install it with `brew install agent-browser`, then run `agent-browser install` for the browser binaries. The Skill requires it in every mode, **--browser=never** included, since a mirror that cannot fall back to a browser is not this Skill. The Manager must be Enabled. No peer Skill and no Harness Capability.

## SEE ALSO

**/kntnt select**
