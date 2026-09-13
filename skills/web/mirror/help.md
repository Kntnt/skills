# mirror

## NAME

mirror - copy a web page, the pages under it, and everything they need to disk, browsable offline

## SYNOPSIS

**/mirror** [**--output=**_DIR_] [**--resources=**_all_|_in-scope_|_none_] [**--max-pages=**_N_] [**--delay=**_SECONDS_] [**--no-links**] [**--ignore-robots**] [**--header=**_HEADER_ ...] [**--user-agent=**_STRING_] [**--dry-run**] *URL* [**--** *INSTRUCTION*]

## DESCRIPTION

`mirror` copies a web page, and every page under it that its links reach, to disk so that it can be opened in a browser with nothing fetched from the network: an archive of a section as it looked, a copy to read without a connection, or a snapshot to work from.

It follows the URL's redirects, and the page where they end is the start page. From there it crawls, one request at a time and breadth first: it saves the start page and every page and file under the root that can be reached by following links, together with everything each page needs to display: images, including those named in `srcset` and `picture`, stylesheets, scripts, fonts, video, audio, posters, text tracks, icons, preloaded files, the web manifest, and what `iframe`, `object` and `embed` show. Everything a stylesheet references through `url()` and `@import` is fetched too, recursively, and so is every `url()` in a `style` attribute. A resource is fetched whatever host it is on, unless **--resources** says otherwise.

Links are read from every fetched HTML page in scope: from `a` and `area` elements with `href`, and from `link` elements whose `rel` is `next`, `prev`, `canonical` or `alternate`. A link in scope that has not been seen is fetched. A link out of scope is recorded in the manifest as `out-of-scope` and never fetched. An HTML page in scope is read for links in turn, and anything else in scope, a PDF for instance, is saved as it is. A link in scope that redirects out of scope is recorded as `redirect-out`, and where it leads is not fetched. **--no-links** turns link discovery off, and then the start page and its resources are all that is fetched.

Every reference in the saved HTML and CSS that points at a file in the mirror is rewritten to a relative path, a link to another saved page included, so the copy works from wherever it is put. A reference to anything not in the mirror, such as a link to a page out of scope, is left as an absolute URL: following it leaves the mirror deliberately, and nothing is fetched by itself. `base` elements are honoured when references are resolved, and removed afterwards. An `integrity` attribute is removed where the rewrite changed the bytes of the file it guards, and kept otherwise.

The start page's directory is the root. If the start page's path ends in a slash, that path is the root prefix; otherwise the prefix is the path up to and including its last slash, and the start page itself is always in scope. End the URL with a slash to make it a directory root. A URL is in scope when its host is the start page's host, its port is the start page's, its scheme is `http` or `https`, and its path starts with the root prefix. Every other subdomain is another site.

Before URLs are compared, the scheme and host are put in lower case, the fragment, the default port and the credentials are removed, dot segments are resolved, percent-encoding is made canonical, `index.html` and `index.php` are read as their directory, and the tracking parameters `utm_*`, `fbclid`, `gclid`, `mc_cid` and `mc_eid` are removed. Every other query parameter is kept, in its order. The start page's host with `www.` added or removed is then written as the start page's host, in the form the start page's final URL has, so `www.x.se` and `x.se` are one site: a page reached through the other form is fetched and saved once, under the start page's host directory, and the tree has no directory for the other form. Only that host folds; `www.` on any other host is left alone. A URL is fetched once, in that form.

Before a page or file is fetched from a host, the start page included, the host's `robots.txt` is read, once per run, with the run's identity and headers, and obeyed. A URL it disallows is recorded as `robots` and not fetched, and the report counts them. The rules are those of the group whose `User-agent` line most specifically matches the run's product token, and those of the `*` group only where no group matches, as RFC 9309 says; the longest matching rule decides, and `Allow` wins a tie. The product token is `kntnt-mirror`, or the first word of **--user-agent** without its version. A `Crawl-delay` longer than **--delay** is honoured for its host. A `robots.txt` that answers with any `4xx` status allows everything; one that answers `5xx`, or not at all after the retries, allows everything too, and the report says it could not be read. Resources are exempt: they are fetched on behalf of a page a person would load, and a `Disallow: /` on a CDN would otherwise break the copy without a word. The file itself is recorded in the manifest and never saved in the tree. **--ignore-robots** turns every rule and `Crawl-delay` off, and the file is still read.

The crawl stops taking new pages at a cap, 5000 pages and files unless **--max-pages** says otherwise, the start page among them; resources do not count. A page or file counts when it is admitted to the crawl, so under a cap of *N* exactly *N* are fetched. When the cap is reached, discovery stops, what is already queued is fetched, every link found afterwards is recorded as `over-cap`, and the report says the cap was reached and what it was.

A fetched HTML page with at least one `script` element and fewer than 200 characters of text outside `script`, `style`, `noscript` and `template` elements, whitespace collapsed, is counted as a suspected JavaScript shell: what it shows is likely drawn by a script, which this Skill does not run. The report says how many there were. It is a warning, and the run does not fail for it.

On a file system that treats names differing only in case as one, as macOS does by default, two URLs that differ only in case map to one file. The run tests the output directory once for it, and where the file system folds case, the later of two such files is saved with `~2`, `~3` and so on before its extension, `page.html` beside `Page.html` becoming `page~2.html`. Links to it are rewritten to that name and the manifest records it, but the name no longer matches the URL, and a copy moved to a file system that does not fold case keeps the suffixed name.

Requests go one at a time over plain HTTP with the identity `kntnt-mirror (+https://github.com/Kntnt/skills)`, and **--delay** spaces them. Connecting and reading each time out after 30 seconds. A connection error, a timeout, and the statuses `429`, `500`, `502`, `503` and `504` are retried up to three times, after the wait `Retry-After` asks for or otherwise after 1, 2 and 4 seconds. Nothing else is retried.

Resources a script loads while the page runs cannot be found by reading the page, and are not saved; the saved page asks the network for them, or goes without.

Chrome restricts fonts and `type="module"` scripts on pages opened as `file://`. For full fidelity, serve the output directory with any static file server, such as `python3 -m http.server`, and open the page through it.

When the run ends, the Skill prints a short report: the pages, files and resources fetched, their total size, how many links were out of scope, redirected out of scope, stopped by `robots.txt` and over the cap, whether the cap was reached, how many pages were suspected shells, any `robots.txt` that could not be read, and every failure with its status and URL.

## POSITIONAL ARGUMENTS

*URL*

The page to mirror. It is required, and absolute with the scheme `http` or `https`. A user name and password for basic auth may stand in it, and are sent to the start page's host only.

## OPTIONS

**--output=**_DIR_

Write the mirror to *DIR*. Defaults to `./`*HOST* in the working directory, *HOST* being the start page's host.

**--resources=**_all_|_in-scope_|_none_

Say which resources are fetched. `all`, the default, fetches every resource the page needs, whatever host it is on. `in-scope` fetches only the resources that are in scope, as DESCRIPTION defines it. `none` fetches no resource. With `in-scope` and `none`, a resource that is left out keeps its absolute reference in the saved page, so the promise that nothing is fetched from the network does not hold for it.

**--max-pages=**_N_

Fetch at most *N* pages and files, the start page among them; resources do not count. Defaults to `5000`, and `0` sets no cap. Links found once the cap is reached are recorded as `over-cap` and not fetched.

**--delay=**_SECONDS_

Wait *SECONDS*, a number of 0 or more, between one request and the next. Defaults to `0`. A `Crawl-delay` in a host's `robots.txt` that is longer applies to that host instead.

**--no-links**

Follow no links. The start page is saved with its resources, and no other page or file is fetched.

**--ignore-robots**

Obey no `robots.txt` rule and no `Crawl-delay`. The file is still read and recorded in the manifest.

**--header=**_HEADER_

Send *HEADER*, written `name: value`, with every request, to whatever host, each hop of a redirect included. Repeatable. It covers `Authorization` and `Cookie`.

**--user-agent=**_STRING_

Send *STRING* as the identity on every request, in place of the Skill's own.

**--dry-run**

Fetch and count everything a real run would, and write nothing: no output directory, no manifest, no log. The report lists every URL that would be fetched, followed by the counts a real run prints.

## FILES

**<output>/<host>/**

One directory per host the mirror holds a file from, such as `x.se/` and `cdn.x.se/`. A host with a port other than its scheme's default is written with the port, as `x.se%3A8080/`. Under it, each file is at its URL's path, as on the site, with percent-encoding decoded.

**URL to path**

A directory URL, one whose path ends in a slash, is saved as `index.html` in that directory. An HTML page whose last path segment has no extension is saved with `.html` appended, so `/docs/guide` becomes `docs/guide.html`. A URL with a query string keeps it in the file name, placed before the extension so that the file keeps its type: `/style.css?v=2` becomes `style%3Fv=2.css`, `/?p=1` becomes `index%3Fp=1.html`, and a name with no extension ends with the query string. In every name, the characters a file name cannot hold on macOS or Linux are percent-encoded: `/`, NUL, `?`, `#`, `%`, `\`, `:`, `*`, `"`, `<`, `>`, `|` and every control character. Where one URL maps to a file whose path another URL needs as a directory, `/a` beside `/a/b`, the file is saved as that directory's `index.html` when it is HTML and with the suffix `~file`, as `a~file`, otherwise. Where the file system folds case, the later of two paths that differ only in case takes `~2`, `~3` and so on before its extension, as DESCRIPTION says. The manifest records the path every file got.

**<output>/.mirror/raw/**

The bytes of every HTML and CSS file as the server sent them, at the same relative path as in the tree. The saved copies in the tree are derived from these at the end of the run. Images, fonts, scripts and every other file the rewrite never changes are kept in the tree only.

**<output>/.mirror/manifest.ndjson**

One JSON object per line, one per URL the run took a position on, each with the same fields: `url`; `final_url`, where its redirects ended; `kind`, one of `page`, `file`, `resource` and `robots`, a link not fetched being a `page`; `source`, `start`, `link`, `resource` or `robots`, what led to it; `discovered_from`, the URL of the page or file that referenced it, or `null` for the start page and a `robots.txt`; `fetcher`, `http`; `status`; `content_type`; `size` in bytes; `local_path`, relative to the output directory; `sha256`; `etag`; `last_modified`; `timestamp`; and `outcome`, one of `fetched`, `out-of-scope`, `redirect-out`, `robots`, `over-cap` and `failed`. A field with nothing to say is `null`. A URL that normalises to one already recorded, a fragment or tracking-parameter variant for instance, gets no row of its own. A `robots.txt` that could not be read is `failed` without failing the run.

**<output>/.mirror/run.log**

One line per request the run made, with its timestamp, method, URL, status and elapsed time, and one line per URL the manifest records as `out-of-scope`, `redirect-out`, `robots`, `over-cap` or `failed`.

## EXIT STATUS

**0**

Everything was fetched: nothing the run set out to fetch failed.

**1**

The run completed and something failed, as the report names, or the start page could not be fetched or is disallowed by `robots.txt`, in which case nothing is written.

**2**

The form was invalid, a value was refused, or a dependency is missing. Nothing is written.

**3**

The help page was printed.

## DIAGNOSTICS

An invalid, incomplete, or out-of-order form is refused rather than repaired or ignored. The Skill names the error, prints the SYNOPSIS, writes nothing, and points to `/mirror --help`. A flag is refused rather than ignored where it has no work to do here, and a flag written after the URL is out of order.

A URL that is not absolute with `http` or `https`, a **--resources** value other than `all`, `in-scope` and `none`, a **--header** without a colon, a **--delay** that is not a number of 0 or more, and a **--max-pages** that is not a whole number of 0 or more are refused the same way, before anything is fetched.

A start page that cannot be fetched, or that `robots.txt` disallows, is reported with the reason, and nothing is written. A resource that cannot be fetched is named in the report with its status, or with the error where there was no answer, and the run goes on.

## EXAMPLES

Mirror a section, every page under `/docs/` its links reach and everything those pages need, into `./example.com`:

```text
/mirror https://example.com/docs/
```

Mirror one page and what it needs, and no page it links to:

```text
/mirror --no-links https://example.com/articles/launch
```

Crawl a large site gently, a second between requests and at most 200 pages:

```text
/mirror --max-pages=200 --delay=1 https://example.com/
```

See what a mirror of a section would fetch, fetching only what lies under it, without writing anything:

```text
/mirror --resources=in-scope --dry-run https://example.com/docs/
```

Mirror a page behind a login, with the session cookie:

```text
/mirror --output=~/Archive/intranet --header="Cookie: session=abc123" https://intranet.example.com/
```

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate. Here it can add no flag, change no flag's value, and supply no URL; it may only shape how the report is relayed.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv`, which runs the Manager's invocation engine and this Skill's own, and gives the engine the libraries it pins. The Manager must be Enabled. No peer Skill and no Harness Capability.

## SEE ALSO

**/kntnt select**
