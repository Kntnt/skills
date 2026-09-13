# The mirror engine owns fetching, the URL-to-path mapping, and the rewrite

This record settles where the work of `/mirror` is done. The Skill copies a web page to disk so that it opens in a browser with nothing fetched from the network, and the series it opens extends it ticket by ticket: pages under the root, sitemaps and feeds as sources, a regex scope, incremental reruns, block detection, and a real browser for pages plain HTTP cannot get. The engine the Skill ships, `scripts/mirror.py`, fetches, decides which file each URL becomes, and rewrites every reference in the saved HTML and CSS, and no external tool does any of the three. What the Skill promises is stated in its own `help.md`, which is the authority on it; this record argues rather than legislates.

## Two tools already mirror web sites

**wget and httrack were weighed first, because both exist to do this job.** `wget --mirror --page-requisites --convert-links` fetches a page and what it needs and rewrites the links it saved; httrack does the same with a richer scope language and a cache that makes a second run incremental. Either would have made the first ticket small: parse the flags, build a command line, relay what the tool prints. Both are mature, widely packaged, and better tested against the web's odd corners than a new engine will be on its first day.

**What decides it is the browser fallback, which a later ticket in the series adds.** Some pages are only whole after a script has run, or are only served to something that looks like a browser. Those pages are fetched through a real browser, and what comes back is HTML neither wget nor httrack has seen. Their references still have to be rewritten to the files beside them, so the engine has to rewrite references itself whatever fetches the ordinary pages.

**A rewrite needs the mapping from URL to path, and it needs it to be its own.** Rewriting a reference means knowing which file the target became: which host directory, whether a directory URL is `index.html`, whether an extensionless page gained `.html`, where a query string went, what happens when `/a` is a file and `/a/b` needs `a` as a directory. wget and httrack each decide that for themselves, and neither takes the decision from outside: there is no option in either that hands it a function from URL to path. An engine rewriting browser-fetched pages beside a tool's own output would have to reproduce the tool's mapping exactly, including its handling of the collisions above, and keep reproducing it across the tool's releases, or the two halves of one mirror would point at files that are not there.

**What is left for either tool is a download loop, and the loop is smaller than the coupling.** Once the engine owns the mapping and the rewrite, the tool would contribute the part that sends requests and writes bytes — a queue, a client, retries, a timeout. That is a few dozen lines on `httpx`. Against it stands a binary every machine has to install, which `compatibility` and the dependency lists would have to declare; output parsed back out of a tool's log to learn which URL became which file; and a second copy of the mapping to keep in step with the first.

## What the engine is shaped for

**Fetching sits behind one interface.** `Fetcher` fetches one URL and says what came back, and `HttpFetcher` is its first implementation; the browser fetcher a later ticket adds is a second implementation beside it, and every manifest row names the fetcher that produced it. The mapping and the rewrite do not know which fetcher ran.

**The bytes as served are kept, so a rewrite never needs a fetch.** HTML and CSS are kept under `.mirror/raw/` exactly as the server sent them, and the tree's copies are derived from them in a pass at the end of the run. A change to the mapping or the rewrite can then be applied to an existing mirror by rewriting again, which is what an incremental rerun needs, and what a tool that rewrites in place would have made impossible.

## What it costs

**The engine meets the web's corners on its own.** Encodings, malformed `srcset` values, CSS that tinycss2 parses but a browser reads differently, and servers that answer oddly are this collection's to handle, where wget and httrack have handled many of them for years. The engine leans on libraries for the parts that are hard to get right — `httpx` for HTTP, `selectolax` for HTML, `tinycss2` for CSS — pinned in its PEP 723 block, so what it writes itself is the mapping, the rewrite and the run.

**Three libraries arrive with `uv`, not a binary with the system.** The Skill declares `uv` and nothing else, and `uv run` provisions the pinned versions the first time the engine runs. The type checker names the two typed libraries and the stubs for the third, as `CONTRIBUTING.md` says.
