# mirror

## NAME

mirror - copy a web page and everything it needs to disk, browsable offline

## SYNOPSIS

**/mirror** [**--output=**_DIR_] [**--resources=**_all_|_in-scope_|_none_] [**--header=**_HEADER_ ...] [**--user-agent=**_STRING_] [**--dry-run**] *URL* [**--** *INSTRUCTION*]

## DESCRIPTION

`mirror` copies a web page to disk so that it can be opened in a browser with nothing fetched from the network: an archive of a page as it looked, a copy to read without a connection, or a snapshot to work from.

It follows the URL's redirects, and the page where they end is the start page. It saves that page together with everything the page needs to display: images, including those named in `srcset` and `picture`, stylesheets, scripts, fonts, video, audio, posters, text tracks, icons, preloaded files, the web manifest, and what `iframe`, `object` and `embed` show. Everything a stylesheet references through `url()` and `@import` is fetched too, recursively, and so is every `url()` in a `style` attribute. A resource is fetched whatever host it is on, unless **--resources** says otherwise.

Every reference in the saved HTML and CSS that points at a file in the mirror is rewritten to a relative path, so the copy works from wherever it is put. A reference to anything not in the mirror, such as a link to another page, is left as an absolute URL: following it leaves the mirror deliberately, and nothing is fetched by itself. `base` elements are honoured when references are resolved, and removed afterwards. An `integrity` attribute is removed where the rewrite changed the bytes of the file it guards, and kept otherwise.

The start page's directory is the root. If the start page's path ends in a slash, that path is the root prefix; otherwise the prefix is the path up to and including its last slash, and the start page itself is always in scope. End the URL with a slash to make it a directory root. A URL is in scope when its host is the start page's host, or that host with `www.` added or removed, its port is the start page's, its scheme is `http` or `https`, and its path starts with the root prefix. Every other subdomain is another site.

Before URLs are compared, the scheme and host are put in lower case, the fragment, the default port and the credentials are removed, dot segments are resolved, percent-encoding is made canonical, `index.html` and `index.php` are read as their directory, and the tracking parameters `utm_*`, `fbclid`, `gclid`, `mc_cid` and `mc_eid` are removed. Every other query parameter is kept, in its order. A URL is fetched once, in that form.

Requests go one at a time over plain HTTP with the identity `kntnt-mirror (+https://github.com/Kntnt/skills)`. Connecting and reading each time out after 30 seconds. A connection error, a timeout, and the statuses `429`, `500`, `502`, `503` and `504` are retried up to three times, after the wait `Retry-After` asks for or otherwise after 1, 2 and 4 seconds. Nothing else is retried.

Resources a script loads while the page runs cannot be found by reading the page, and are not saved; the saved page asks the network for them, or goes without.

Chrome restricts fonts and `type="module"` scripts on pages opened as `file://`. For full fidelity, serve the output directory with any static file server, such as `python3 -m http.server`, and open the page through it.

When the run ends, the Skill prints a short report: the pages and resources fetched, their total size, and every failure with its status and URL.

## POSITIONAL ARGUMENTS

*URL*

The page to mirror. It is required, and absolute with the scheme `http` or `https`. A user name and password for basic auth may stand in it, and are sent to the start page's host only.

## OPTIONS

**--output=**_DIR_

Write the mirror to *DIR*. Defaults to `./`*HOST* in the working directory, *HOST* being the start page's host.

**--resources=**_all_|_in-scope_|_none_

Say which resources are fetched. `all`, the default, fetches every resource the page needs, whatever host it is on. `in-scope` fetches only the resources that are in scope, as DESCRIPTION defines it. `none` fetches no resource. With `in-scope` and `none`, a resource that is left out keeps its absolute reference in the saved page, so the promise that nothing is fetched from the network does not hold for it.

**--header=**_HEADER_

Send *HEADER*, written `name: value`, with every request. Repeatable. It covers `Authorization` and `Cookie`.

**--user-agent=**_STRING_

Send *STRING* as the identity on every request, in place of the Skill's own.

**--dry-run**

Fetch and count everything a real run would, and write nothing: no output directory, no manifest, no log. The report lists every URL that would be fetched, followed by the counts a real run prints.

## FILES

**<output>/<host>/**

One directory per host the mirror holds a file from, such as `x.se/` and `cdn.x.se/`. A host with a port other than its scheme's default is written with the port, as `x.se%3A8080/`. Under it, each file is at its URL's path, as on the site, with percent-encoding decoded.

**URL to path**

A directory URL, one whose path ends in a slash, is saved as `index.html` in that directory. An HTML page whose last path segment has no extension is saved with `.html` appended, so `/docs/guide` becomes `docs/guide.html`. A URL with a query string keeps it in the file name, placed before the extension so that the file keeps its type: `/style.css?v=2` becomes `style%3Fv=2.css`, `/?p=1` becomes `index%3Fp=1.html`, and a name with no extension ends with the query string. In every name, the characters a file name cannot hold on macOS or Linux are percent-encoded: `/`, NUL, `?`, `#`, `%`, `\`, `:`, `*`, `"`, `<`, `>`, `|` and every control character. Where one URL maps to a file whose path another URL needs as a directory, `/a` beside `/a/b`, the file is saved as that directory's `index.html` when it is HTML and with the suffix `~file`, as `a~file`, otherwise. The manifest records the path every file got.

**<output>/.mirror/raw/**

The bytes of every HTML and CSS file as the server sent them, at the same relative path as in the tree. The saved copies in the tree are derived from these at the end of the run. Images, fonts, scripts and every other file the rewrite never changes are kept in the tree only.

**<output>/.mirror/manifest.ndjson**

One JSON object per line, one per URL the run took a position on, each with the same fields: `url`; `final_url`, where its redirects ended; `kind`, one of `page`, `file` and `resource`; `source`, `start` or `resource`, what led to it; `discovered_from`, the URL of the file that referenced it, or `null` for the start page; `fetcher`, `http`; `status`; `content_type`; `size` in bytes; `local_path`, relative to the output directory; `sha256`; `etag`; `last_modified`; `timestamp`; and `outcome`, one of `fetched`, `out-of-scope` and `failed`. A field with nothing to say is `null`.

**<output>/.mirror/run.log**

One line per request the run made, with its timestamp, method, URL, status and elapsed time, and one line per URL the manifest records as `out-of-scope` or `failed`.

## EXIT STATUS

**0**

Everything in scope was fetched.

**1**

The run completed and something failed, as the report names, or the start page could not be fetched, in which case nothing is written.

**2**

The form was invalid, a value was refused, or a dependency is missing. Nothing is written.

**3**

The help page was printed.

## DIAGNOSTICS

An invalid, incomplete, or out-of-order form is refused rather than repaired or ignored. The Skill names the error, prints the SYNOPSIS, writes nothing, and points to `/mirror --help`. A flag is refused rather than ignored where it has no work to do here, and a flag written after the URL is out of order.

A URL that is not absolute with `http` or `https`, a **--resources** value other than `all`, `in-scope` and `none`, and a **--header** without a colon are refused the same way, before anything is fetched.

A start page that cannot be fetched is reported with the reason, and nothing is written. A resource that cannot be fetched is named in the report with its status, or with the error where there was no answer, and the run goes on.

## EXAMPLES

Mirror a page and everything it needs into `./example.com`:

```text
/mirror https://example.com/articles/launch
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
