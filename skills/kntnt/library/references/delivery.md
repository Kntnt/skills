# Delivery

Every Skill that produces a Text Artifact delivers it the same way. This document is the complete contract: where a result goes, when a source file may be replaced instead, what happens when nothing changed, and what is refused before anything is written. It is a reference several Skills read rather than a runtime of its own. Each Skill exposes these rules through its own Formal Invocation and owns the names it gives them, so nothing here fixes how an option is spelled; what is fixed is the behaviour behind it.

## The response is the default

The default Output Target is the agent response. A run that keeps the default delivers the complete Text Artifact in the response and changes nothing on the filesystem: it creates no file, touches no file, and makes no directory.

An Output Target is independent of where the source material came from. Supplying a local file as source material selects no destination, and a run that reads a file still delivers to the response until the caller names somewhere else. Persisting a result is the caller's explicit choice, and making that choice is the whole of the authorization for it.

## An explicit destination

An explicit destination is one filesystem path, and what exists at that path decides what happens to it.

**A path that does not exist** creates exactly that one file and writes the complete Text Artifact into it. Exactly one file: nothing else is created beside it, and no directory is made to hold it.

**A path naming an existing file** overwrites that exact file with the complete Text Artifact. No confirmation and no separate force option is required, and none is offered. Naming the path is the authorization, and demanding a second gesture on top of it would teach that naming a destination means something less than it says.

**A path naming an existing directory** delivers into that directory under a filename the run derives, by the rules below. Choosing a directory selects a place, not a file, so it never overwrites a file already in it.

## Deriving a filename for a directory

A directory destination needs a name, and the name comes from what the run already knows. Take the first of these the run has: the basename of the local file that supplied the Text Artifact, the title of a referenced URL, then the Skill's own working title for the text it created. Reduce it to a name the filesystem accepts, and keep a suitable text extension — the source file's own where it had one, and otherwise the one matching the text's format.

That gives a stem and an extension, and the stem stays as it is for every delivery into that directory. Where nothing exists at the derived name, that name is the file written. Where something exists there, the existing file is never overwritten: keep the original stem and take the first free numbered candidate in ascending order, beginning at `-2`. So `my-file.md`, `my-file-2.md`, `my-file-3.md` are one sequence, growing by one name at a time.

A numbered candidate is never adopted as the new stem. A third delivery into a directory already holding the first two is `my-file-3.md` and never `my-file-2-2.md`, whose stem would fork the sequence in two and leave the directory recording how many times the same text arrived rather than which arrival it was. Ascending order with the first free name also means a number freed by a deleted file is used again before a higher one is taken.

## In-place Editing

In-place Editing replaces the single local file that supplied the Text Artifact with the result, instead of delivering it anywhere else. It is available only to a Skill whose work is to return a changed version of a text the caller already has.

A Skill that creates a new Text Artifact never edits its own source material in place. The brief, the interview, the notes, and the article it draws on are where the text came from and not where it goes; a Skill that could overwrite them would make supplying a file a risk rather than a convenience, and would lose the material the result is answerable to.

In-place Editing requires exactly one writable local source file, and it is mutually exclusive with a separate output option. A run replaces its source or delivers elsewhere, never both, and an invocation asking for both has named two destinations for one text.

It is refused wherever there is no such file to replace. Text supplied inline in the invocation or taken from the conversation is not a file. A URL is not a local file, and fetching one grants no right to write anything back. An uploaded source and a read-only file cannot be replaced. More than one Text Artifact leaves the single file the contract is written around undefined.

An explicit output path equal to the input path is refused in favour of In-place Editing, and the refusal says which gesture to use. Replacing a source then has one recognizable authorization: a reader of an invocation sees that a source is about to be replaced from the request itself, without comparing two paths to discover it.

## When nothing changed

A run may finish with nothing to change, and what it does then follows its destination.

A response-targeted run and an in-place run that changed nothing write nothing at all and return a short no-change status in place of the text. Repeating an unchanged text into the response spends output on what the caller is already holding, and rewriting a file with its own contents makes its timestamp claim that something happened.

That status is written in the language of the Text Artifact rather than the language of the invocation, so a Swedish text that needed no work is reported on in Swedish.

An explicitly selected different file or directory still receives the complete Text Artifact when nothing changed. Creating that artifact is what was asked for, and a destination left empty because the text needed no work is a request refused without saying so. A directory destination derives its filename and resolves collisions exactly as it would for a changed text.

## Refusals

Every contradictory, meaningless, or unusable output request is refused before the first side effect. The cases this contract names are more than one Text Artifact where the Skill processes one, an output option together with In-place Editing, an output path equal to the input path, In-place Editing for inline text or a URL or an uploaded or read-only source, and a destination the run cannot write — a path whose parent directory does not exist among them.

Every such check that can be made by reading is made before anything is written, so a refusal leaves no partial effect behind: no file created, none truncated, none renamed, and no directory made. Where a conflict can only be discovered after a legitimate effect, the run stops there and reports the exact partial outcome rather than continuing.

A refusal follows the Collection's ordinary diagnostic and help conventions. It names what was wrong, prints the synopsis of the most specific recognized command page verbatim, and points at that command's own help form. An output option is refused rather than ignored where it has no work to do, a flag accepted and ignored teaching that flags sometimes do nothing.
