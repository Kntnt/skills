---
name: brief
description: Interview for, draft from supplied material, or review a Writing Brief against the 13-question writing template. Start it on your own only when the literal token `/brief` appears in the request or the user explicitly asks for a brief according to this 13-question template. Not for a bare mention of the word brief, a request for a short answer, or an unrelated project or delegation brief. A user may also invoke it by name at any time.
disable-model-invocation: false
argument-hint: '[--output=response|<path>] [<material>] [-- <instruction>]'
compatibility: Requires uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# brief

Produce one Writing Brief that can be handed to `/write`, and stop at the brief.

Run `UV_NO_CACHE=1 UV_NO_PROJECT=1 uv run "$HERE/scripts/invoke.py"` — `$HERE` is the directory that holds this SKILL.md — with everything the user typed after `/brief`, verbatim and however many lines, on stdin. Exit 0: do what it prints. On any other exit, if you introduced a known construction error and can correct it while preserving the user's request and authority, account for effects already produced, submit the corrected invocation through the same shim, and continue from the failed boundary; a refusal before the operation starts consumes no operation. Otherwise show what it printed to the user verbatim and stop. Never repair input the user supplied, or automatically retry exact help, an unmet dependency, an unrelated failure, or a failure whose origin or valid correction is unknown.

Run every UV command in this Skill with a fresh private directory as `TMPDIR`, and remove that directory after the command, including when it fails. The private directory belongs to that one command and no other run, so cleanup removes only files this run created.

A model-invoked run submits an empty payload, takes the material and guidance from the current request, and joins the same steps below. A source path selects no destination. Without a Formal Invocation's output option, use a destination explicitly requested in the current turn; otherwise deliver to the response. Ask before writing where a request to save gives no destination.

## Arguments

`<material>` is free text, notes, paths, URLs or documents supplying material for one brief, or an existing brief in any shape. It may be omitted when the Contextual Instruction or conversation supplies it, or to begin an interview.

`--output=response|<path>` selects the response by default or one filesystem destination under `$LIBRARY/references/delivery.md`. An input file is never an output destination; this Skill offers no In-place Editing.

## Steps

1. Gather the supplied material and the options from the JSON. Read supplied files and reachable links; report inaccessible material as missing rather than attributing content to it. Settle the Output Target under `$LIBRARY/references/delivery.md` before writing anything. Refuse a contradictory or unwritable destination, a missing parent directory, or a destination equal to any supplied file, without writing. Done when the material and destination are known, or you have asked or refused.
2. Read `$LIBRARY/references/editorial/writing-brief.md`, the authoritative English template and its quality criteria. Speak and write the brief in the user's working language, translating its questions faithfully with their numbers and order intact. Question 13 names the language of the future text, which can differ from this working language. Ask only if the working language is unclear. Done when the template and working language are in hand.
3. Choose the mode from the request and material: no material means Interview; unstructured source material means Draft; an existing brief means Review regardless of its headings, order or format. An explicit request for one of these modes settles the choice; ask only when it is ambiguous. Follow the selected mode below, using Selection whenever a genre, technique or text language is reached. Done when all 13 points have an answer, a marked gap, or a marked unconfirmed suggestion.
4. Run the template's final check over questions 2–7 and the hook. Correct only relationships the supplied answers already settle; otherwise mark and report the inconsistency, with the question needed to resolve it. Recheck affected answers after a user revisits a point. A failed check stays visible beside the brief; an incomplete brief is never reported ready to write. Done when every check has a supported result or an explicit unresolved finding.
5. Assemble one Markdown brief with the template's 13 numbered questions as headings and the answers beneath them, including the fixed markers below. Keep supplied facts, sources, uncertainty and brand details attributable to the material; invent none. Attach a leading YAML `kntnt` map containing only settled, verified `genre`, `technique` and `language` values under Selection. Omit each unsettled value and omit the frontmatter entirely if none is settled. Done when every point and unresolved finding is represented and the metadata contains no guess.
6. Deliver the brief through `$LIBRARY/references/delivery.md`, with a short account of the check and unresolved questions. For Review, deliver the report specified below alongside it. For Draft and Review, offer an interview about the gaps; for Review also offer a rewritten brief. These offers wait for the user. On a response target, remove every artifact or scratch file this run created and base the delivery account on the filesystem state that remains after cleanup. Stop: the text itself and invoking `/write` remain the user's next action. Done when the brief and its findings are delivered to the selected target and the run's scratch is gone.

## Interview

Ask the questions one at a time in template order, showing each question's guidance in short form. Keep answers and the number of follow-ups for each point in the conversation. For an answer that misses a quality criterion, ask a targeted follow-up naming the missing part. Ask at most two follow-up questions per point; after the second, accept the answer and append `[WEAK: <the quality criterion not met>]` if it remains weak. A request to revisit a point does not restart its follow-up allowance.

Accept "don't know" immediately as `[MISSING: <the question the user needs to answer>]` and move on. The user may return to any earlier point at any time; keep the other answers and resume at the next unanswered point. When an answer supplies a later point, offer that answer when the point is reached and ask for confirmation. A suggestion derived from previous answers remains `[SUGGESTED: <inference>]` until the user confirms it. If the user ends the interview early, deliver all 13 headings with the remaining questions marked missing.

## Draft

Map only what the material supports onto the 13 points. Keep any inference visibly `[SUGGESTED: <inference>]`; no plausible completion counts as a supplied fact. Mark each absent answer or missing part `[MISSING: <the question the user needs to answer>]`. Identify quality shortfalls beside supplied answers without silently repairing them into stronger claims. Deliver this draft before offering the gap interview.

## Review

Map the content of the existing brief onto the 13 questions, wherever its answers appear. Judge the presence and quality of answers, not whether the original uses the template's form. Report every point as answered, weak or missing; a weak point names its unmet quality criterion and a missing point asks the unanswered question. Include the template's check and end the report with all unanswered issues phrased as questions.

The required 13-heading brief is a mapping of the supplied answers with their gaps and unconfirmed inferences marked, not permission to invent repairs. Deliver it with the report even when the user has not accepted the offer of a rewrite. A later rewrite can improve the supplied wording; the gap interview can settle missing content. Offer both after the report's closing questions.

## Selection

Read the installed directories at run time: `$LIBRARY/references/editorial/genres/` and `$LIBRARY/references/editorial/techniques/`. Only lowercase-letter base filenames ending in `.md` are choices; review halves, README files, dotfiles and nested support are not. The filenames without extensions are the normalised values. The template's examples explain choices; they are not an installed inventory.

Map a genre the user names in any language against the installed filenames and each resource's `# <Name>` heading and opening paragraph, reading no further of an unselected resource. Load the selected genre's base resource only after it is settled. If the name maps ambiguously, ask or leave it missing; an inferred genre remains a suggestion until confirmed. Never default an unanswered question to `general`.

For a technique suggestion, read the resolved genre's ordinary technique first. Where it names an installed technique, suggest that and explain why. Where it names none, use question 8's tell-or-reason distinction to propose a choice, still subject to confirmation. Read the selected technique resource to check its fit with the hook and angle. A technique the genre advises against is weak: quote the genre's reason in the finding. An ordinary technique of `none` alone does not advise against an arc; selecting an installed arc there is legitimate. In an interview apply the two-follow-up limit before accepting a weak answer; in a draft or review report the weakness immediately.

An explicitly chosen free structure is `technique: none`, which names no resource. A technique deliberately left to the genre is omitted from the map, with that choice stated under question 8, so `/write` can resolve it from the genre. A tentative suggestion also stays out of the map. For a choice that cannot be found installed, retain the user's words with the missing question about a usable choice and omit its metadata value; never replace it with a guess.

Verify question 13's language through `uv run --no-cache --no-project "$LIBRARY/scripts/languages.py" resolve --scope=composition "<selector>"`. Use the returned `code` in the map. For an unlisted human description, interpret it, propose one candidate from the resolver's `list` command, and verify through the same `resolve` command. If no unique installed language can be established, ask or mark it missing and omit `language`; never take it from the brief's working language. The resolver's scope content is a terminal result, not a pointer to other language scopes.

## Markers

Keep the tokens English in every working language; write their explanations in that language. Use `[MISSING: <the question the user needs to answer>]` for every gap and `[SUGGESTED: <inference>]` for every unconfirmed inference. Append `[WEAK: <the quality criterion not met>]` to an answer accepted after two interview follow-ups; in Draft and Review use it to expose an identified weakness without waiting for an interview. A user confirmation settles an inference but does not turn a quality failure into a passing answer. Keep deliberate omissions of I, V or a web search phrase explicit, so they cannot be confused with gaps.
