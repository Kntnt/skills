# tldr

Summarise what was just said, and keep replies short by default.

## Synopsis

```
/tldr [instruction]
/tldr --on|--off [--user] [--yes]
/tldr --status
```

## Description

Two things behind one name.

**Typed bare, `/tldr` summarises.** It takes everything the agent has written since you last spoke, plus whatever earlier context that range needs to make sense, and gives it back to you in three parts: what happened, what the agent decided on your behalf, and what needs you. All three always appear, including when the answer is *nothing needs you* — that reassurance is the point, and a section that shows up only sometimes puts you back to scanning for it.

The summary is written at the altitude of someone who was not watching. It answers in the language you were using, and if the reply above was already short, or a compaction has taken part of the range, it says so instead of handing you a summary that looks complete and is not.

**With `--on`, it switches on TL;DR mode**, so replies are short from the outset and you do not have to ask afterwards. The mode is a managed block in the context file your harness already loads, so it works in every harness rather than only in the one that has output styles, and it takes effect on the turn that switches it on rather than at the next session.

The mode is brevity plus the closing verdict, not the three-part template on every turn: that structure appears only when a reply reports work you did not watch, or runs past one list or three paragraphs. It governs what the agent says to you and never what it writes into files — code, comments, commit messages, and documentation keep the register they already have.

## Arguments

Anything after `/tldr` that is not a flag is a free-form instruction, in any language, and it is obeyed. It can widen the range (`all`), name a language (`sv`, `en_GB`, `engelska`, `AmE`, `svara på engelska`), or ask for anything else (`bara säkerhetsdelen`, `max 5 punkter`).

## Options

- `--on` — turn TL;DR mode on.
- `--off` — turn it off.
- `--status` — report both scopes, the resulting verdict, and any staleness. Changes nothing.
- `--user` — target the user scope instead of this session. Writes a managed block into this harness's global context file, and shows you the file and the exact insertion first.
- `--yes` — assume yes: write or remove the block without waiting for a confirmation. Valid only alongside `--on` or `--off`.

## Scopes

`session` is the default and outlives nothing. `--user` is a managed block in this harness's global context file; run the skill in another harness to give that one the mode too.

There is no project scope. Brevity is how one person likes to read rather than a convention a team shares, and a committed block would impose it on everyone who clones the repository.

## Notes

A flag with no work to do on the invocation you typed is refused rather than ignored, because a flag accepted and ignored teaches that flags sometimes do nothing. So `/tldr --yes` on its own is an error, while `/tldr --on --user --yes` is not. An incomplete form is refused the same way: `/tldr --user` alone changes nothing and prints the synopsis, rather than asking which of on, off, or status you meant.

Session state lives in the conversation and nowhere else. A compaction can drop it, and unlike a lost delegation setting you will see that happen in the very next reply — retyping `/tldr --on` is the whole repair.

A block whose text no longer matches the skill's is reported as stale, and `/tldr --on --user` is the fix: it rewrites the block rather than adding a second one.

## Dependencies

None. This is the only skill in the collection with no binary, no capability, and no dependency on another skill, so it runs no dependency check and works on a machine without `uv`.

## See also

`/kntnt select` to enable this skill elsewhere. `/delegation` for the other standing mode in this collection.
