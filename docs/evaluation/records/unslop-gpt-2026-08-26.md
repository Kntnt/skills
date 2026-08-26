- **record** — unslop-gpt-2026-08-26
- **date** — 2026-08-26
- **ticket** — #161
- **skill** — unslop
- **provider family** — gpt
- **model** — gpt-5.6-sol
- **harness** — Codex CLI 0.149.1
- **corpus commit** — 46ba9c1

## Source-material fixtures

- **fixture** — brief-short, brief-article-abt, brief-report-pac, brief-press-release-sv, interview-transcript, factual-source-long, and url-source
- **invocation** — none
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — none
- **side effects** — none
- **criteria** —
  - applicability — skipped — These fixtures are material for drafting and source-fidelity evaluation; Unslop reads a finished Text Artifact and never compares it with source material.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Every source fixture is named here rather than omitted.

## clean-en-GB

- **fixture** — clean-en-GB
- **invocation** — /unslop --language=en_GB --max=3 /tmp/kntnt-gpt-eval.2WAfub/unslop-clean/corpus/prose/clean-en-GB.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The short no-change status was returned.
- **side effects** — none
- **criteria** —
  - clean pass — pass — No anti-slop finding or rewrite was invented.
  - early stop — pass — The budget of three remained unspent and no subagent was started.
  - no mechanics — pass — No Proofread pass or mechanical change occurred.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — This also exercises response-default and unchanged-result delivery.

## flawed-en-US

- **fixture** — flawed-en-US
- **invocation** — /unslop --language=en_US --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-flawed-en/corpus/prose/flawed-en-US.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The mechanically flawed artifact and three anti-slop findings were returned.
- **side effects** — none
- **criteria** —
  - anti-slop-only findings — pass — Findings were limited to importance inflation, an empty setup and a false contrast.
  - mechanics preserved — pass — Every spelling, agreement, punctuation and duplication error remained.
  - zero budget — pass — No correction subagent or edit occurred.
- **unresolved findings** — Three anti-slop findings.
- **defects filed** — none
- **notes** — none

## flawed-sv

- **fixture** — flawed-sv
- **invocation** — /unslop --language=sv --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-flawed-sv/corpus/prose/flawed-sv.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — A short Swedish no-change status was returned.
- **side effects** — none
- **criteria** —
  - lens boundary — pass — Mechanical Swedish errors alone produced no anti-slop finding.
  - mechanics preserved — pass — No Proofread pass or correction occurred.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## slop-heavy — default budget

- **fixture** — slop-heavy
- **invocation** — /unslop --language=en_GB /tmp/kntnt-gpt-eval.2WAfub/unslop-slop-en-default/corpus/prose/slop-heavy.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — One correction round returned six short paragraphs and no unresolved finding.
- **side effects** — none
- **criteria** —
  - anti-slop detection — pass — The initial pass recognized the fixture's patterns.
  - fresh correction and re-read — pass — A fresh correction subagent was followed by a new top-to-bottom pass.
  - preservation — fail — Most content was deleted or replaced together with the patterns.
  - unresolved delivery — fail — Lost claims were not retained or reported.
- **unresolved findings** — none reported
- **defects filed** — #175
- **notes** — The default budget was exhausted after one round.

## slop-heavy — higher budget

- **fixture** — slop-heavy
- **invocation** — /unslop --language=en_GB --max=2 /tmp/kntnt-gpt-eval.2WAfub/unslop-slop-en-high/corpus/prose/slop-heavy.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — A higher-budget loop returned six short paragraphs and no unresolved finding.
- **side effects** — none
- **criteria** —
  - higher budget — pass — The positive ceiling was accepted and corrections were re-read.
  - preservation — fail — The result again discarded most of the source's claims.
  - loop verification — fail — Re-reading accepted the content loss as clean rather than stopping on a repair-created defect.
- **unresolved findings** — none reported
- **defects filed** — #175
- **notes** — none

## slop-heavy-sv — inferred

- **fixture** — slop-heavy-sv
- **invocation** — /unslop --max=1 /tmp/kntnt-gpt-eval.2WAfub/unslop-slop-sv-infer/corpus/prose/slop-heavy-sv.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — One correction round returned a shorter Swedish artifact and two unresolved findings.
- **side effects** — none
- **criteria** —
  - language inference — pass — Swedish was inferred and delivery stayed Swedish.
  - Swedish anti-slop — pass — Shared and Swedish-specific patterns were recognized.
  - preservation — fail — Content-bearing passages were removed or flattened, reproducing #175.
  - language-specific patterns — pass — Quotation marks, serial comma, dash and ampersand were corrected because the Swedish anti-slop scope explicitly names those imported writing patterns, not because a mechanical pass ran.
- **unresolved findings** — Two remaining importance-inflation findings.
- **defects filed** — #175
- **notes** — The mechanics changes are part of the same correction overreach.

## slop-heavy-sv — explicit zero budget

- **fixture** — slop-heavy-sv
- **invocation** — /unslop --language=sv --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-slop-sv-explicit/corpus/prose/slop-heavy-sv.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The byte-unchanged artifact and eleven Swedish findings were returned.
- **side effects** — none
- **criteria** —
  - Swedish anti-slop — pass — Shared and language-specific patterns were found in Swedish.
  - zero budget — pass — No correction occurred.
  - mechanics preserved — pass — Swedish mechanics bait remained untouched.
- **unresolved findings** — Eleven pattern-specific findings.
- **defects filed** — none
- **notes** — none

## code-carrying

- **fixture** — code-carrying
- **invocation** — /unslop --language=en_GB --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-code-en/corpus/prose/code-carrying.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The unchanged artifact and nine prose-only findings were returned.
- **side effects** — none
- **criteria** —
  - code boundary — pass — Fenced, indented and inline code remained byte-identical and produced no finding.
  - mechanics preserved — pass — Prose mechanics errors also remained.
  - anti-slop scope — pass — Findings named only catalogue patterns in prose.
- **unresolved findings** — Nine anti-slop findings.
- **defects filed** — none
- **notes** — none

## code-carrying-sv — inferred

- **fixture** — code-carrying-sv
- **invocation** — /unslop --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-code-sv-infer/corpus/prose/code-carrying-sv.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The unchanged Swedish artifact and seven prose-only findings were returned.
- **side effects** — none
- **criteria** —
  - language inference — pass — Swedish was inferred.
  - code boundary — pass — All code bytes and code-bait errors remained.
  - mechanics preserved — pass — The four prose mechanics errors remained too.
- **unresolved findings** — Seven Swedish anti-slop findings.
- **defects filed** — none
- **notes** — none

## code-carrying-sv — explicit

- **fixture** — code-carrying-sv
- **invocation** — /unslop --language=sv --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-code-sv-explicit/corpus/prose/code-carrying-sv.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The unchanged Swedish artifact and eleven prose-only findings were returned.
- **side effects** — none
- **criteria** —
  - explicit language — pass — Swedish anti-slop guidance was used.
  - code boundary — pass — No code sample produced a finding or change.
  - mechanics preserved — pass — No mechanical pass occurred.
- **unresolved findings** — Eleven Swedish anti-slop findings.
- **defects filed** — none
- **notes** — none

## resembles-abt

- **fixture** — resembles-abt
- **invocation** — /unslop --language=en_GB --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-resembles/corpus/prose/resembles-abt.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — A short no-change status was returned.
- **side effects** — none
- **criteria** —
  - clean anti-slop pass — pass — The genuine connective and competent prose produced no false finding.
  - no technique or mechanics — pass — ABT was not selected and Therefore was not edited.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## mixed-language

- **fixture** — mixed-language
- **invocation** — /unslop --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-mixed/corpus/prose/mixed-language.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The run asked the caller to choose sv, en_GB or en_US.
- **side effects** — none
- **criteria** —
  - ambiguous language — pass — No language was guessed and no pass or write occurred.
- **unresolved findings** — The caller must choose a language resource.
- **defects filed** — none
- **notes** — none

## locale-divergent — en_GB

- **fixture** — locale-divergent
- **invocation** — /unslop --language=en_GB --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-locale-gb/corpus/prose/locale-divergent.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — A short no-change status was returned.
- **side effects** — none
- **criteria** —
  - anti-slop lens — pass — Locale mechanics alone produced no finding.
  - mechanics preserved — pass — No date, spelling or punctuation was edited.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## locale-divergent — en_US

- **fixture** — locale-divergent
- **invocation** — /unslop --language=en_US --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-locale-us/corpus/prose/locale-divergent.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The unchanged artifact and one purported locale finding were returned.
- **side effects** — none
- **criteria** —
  - anti-slop lens — fail — The only finding concerned spelling, vocabulary, currency and date interpretation, none of which is an anti-slop pattern.
  - mechanics preserved — pass — Budget zero caused no edit.
- **unresolved findings** — An out-of-scope locale mismatch finding.
- **defects filed** — #177
- **notes** — none

## handoff-present

- **fixture** — handoff-present
- **invocation** — /unslop --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-handoff-present/corpus/frontmatter/handoff-present.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The unchanged artifact and one false-contrast finding were returned.
- **side effects** — none
- **criteria** —
  - metadata language — pass — en_GB came from the recognized map.
  - metadata preservation — pass — The map and all three values remained unchanged; no synchronization occurred.
  - anti-slop scope — pass — The only finding was the final false contrast.
- **unresolved findings** — One false-contrast finding.
- **defects filed** — none
- **notes** — none

## handoff-conflicting

- **fixture** — handoff-conflicting
- **invocation** — /unslop --language=sv --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-handoff-conflicting/corpus/frontmatter/handoff-conflicting.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — A short Swedish no-change status was returned.
- **side effects** — none
- **criteria** —
  - precedence — pass — Formal Swedish suppressed metadata en_US.
  - no synchronization — pass — The source map remained deliberately unchanged because Unslop resolves only language.
  - clean pass — pass — No unrelated full-contract finding was imposed.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## handoff-unusable

- **fixture** — handoff-unusable
- **invocation** — /unslop --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-handoff-unusable/corpus/frontmatter/handoff-unusable.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Unsupported metadata language en_UK was reported and the run stopped.
- **side effects** — none
- **criteria** —
  - unusable metadata — pass — en_UK was not reinterpreted.
  - atomicity — pass — No pass or write occurred.
- **unresolved findings** — The caller must choose an installed language.
- **defects filed** — none
- **notes** — none

## handoff-partial

- **fixture** — handoff-partial
- **invocation** — /unslop --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-handoff-partial/corpus/frontmatter/handoff-partial.md -- Swedish is the language.
- **contextual instruction** — Swedish is the language.
- **output target** — response
- **observed delivery** — The unchanged artifact and two Swedish anti-slop findings were returned.
- **side effects** — none
- **criteria** —
  - contextual precedence — pass — The absent metadata language fell through to Contextual Instruction despite the mixed body.
  - metadata preservation — pass — The partial Kntnt map remained byte-identical and no key was added.
  - anti-slop scope — pass — Findings were limited to imported dash and serial-comma patterns named by Swedish guidance.
- **unresolved findings** — Two Swedish punctuation-pattern findings.
- **defects filed** — none
- **notes** — none

## frontmatter-unrelated

- **fixture** — frontmatter-unrelated
- **invocation** — /unslop --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-frontmatter-unrelated/corpus/frontmatter/frontmatter-unrelated.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The unchanged artifact and one vague-attribution finding were returned.
- **side effects** — none
- **criteria** —
  - configuration boundary — pass — Top-level language and genre bait was ignored.
  - frontmatter preservation — pass — Every frontmatter line remained unchanged and no Kntnt map was added.
  - anti-slop scope — pass — The literature suggests was reported as vague attribution; structural title promises were not imposed.
- **unresolved findings** — One vague-attribution finding.
- **defects filed** — none
- **notes** — none

## frontmatter-absent

- **fixture** — frontmatter-absent
- **invocation** — /unslop --max=0 /tmp/kntnt-gpt-eval.2WAfub/unslop-frontmatter-absent/corpus/frontmatter/frontmatter-absent.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — A short no-change status was returned.
- **side effects** — none
- **criteria** —
  - metadata optionality — pass — No metadata was demanded or created.
  - clean pass — pass — No rewrite or mechanical pass occurred.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Same artifact produced legitimate findings in some independent output runs; judging is per run.

## new-file

- **fixture** — new-file
- **invocation** — /unslop --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/unslop-new-file/out/draft.md /tmp/kntnt-gpt-eval.2WAfub/unslop-new-file/corpus/frontmatter/frontmatter-absent.md
- **contextual instruction** — none
- **output target** — out/draft.md
- **observed delivery** — The unchanged artifact was written and two findings were reported beside the path.
- **side effects** — Created exactly out/draft.md; the source was unchanged.
- **criteria** —
  - new file — pass — The complete artifact reached the exact destination without response duplication.
  - unresolved routing — pass — Synonym-cycling and vague-attribution findings remained in the response.
- **unresolved findings** — Roster/rota cycling and Most teams vague attribution.
- **defects filed** — none
- **notes** — none

## existing-file

- **fixture** — existing-file
- **invocation** — /unslop --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/unslop-existing-file/corpus/output/existing-target.md /tmp/kntnt-gpt-eval.2WAfub/unslop-existing-file/corpus/frontmatter/frontmatter-absent.md
- **contextual instruction** — none
- **output target** — the staged existing-target.md
- **observed delivery** — The occupant was replaced and one finding was reported beside the path.
- **side effects** — Replaced exactly existing-target.md; no sibling was created.
- **criteria** —
  - existing destination — pass — Explicit naming authorized replacement without confirmation.
  - unchanged artifact — pass — The source text was copied byte-for-byte because budget zero permits no correction.
- **unresolved findings** — Vague attribution plus unsupported superlative inflation in the final sentence.
- **defects filed** — none
- **notes** — none

## existing-directory

- **fixture** — existing-directory
- **invocation** — /unslop --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/unslop-existing-dir/out /tmp/kntnt-gpt-eval.2WAfub/unslop-existing-dir/corpus/frontmatter/frontmatter-absent.md
- **contextual instruction** — none
- **output target** — the staged empty out directory
- **observed delivery** — frontmatter-absent.md was created and one finding was reported.
- **side effects** — Created exactly out/frontmatter-absent.md.
- **criteria** —
  - derived filename — pass — The name came from the source and retained a text extension.
  - unresolved routing — pass — The finding appeared in the response.
- **unresolved findings** — Most teams is vague attribution.
- **defects filed** — none
- **notes** — none

## derived-name-collision

- **fixture** — derived-name-collision
- **invocation** — /unslop --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/unslop-collision/corpus/output/collision /tmp/kntnt-gpt-eval.2WAfub/unslop-collision/corpus/output/interview-notes.md
- **contextual instruction** — none
- **output target** — the staged collision directory
- **observed delivery** — The clean unchanged text was written to interview-notes-3.md.
- **side effects** — Created only interview-notes-3.md; both occupants remained unchanged.
- **criteria** —
  - collision sequence — pass — The first free suffix from the original stem was selected.
  - clean pass — pass — No finding or correction was invented.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## read-only-source

- **fixture** — read-only-source
- **invocation** — /unslop --language=en_GB --max=0 --in-place /tmp/kntnt-gpt-eval.2WAfub/unslop-readonly/corpus/output/readonly-source.md
- **contextual instruction** — none
- **output target** — in place
- **observed delivery** — The read-only source was refused before the pass.
- **side effects** — none; permissions and bytes were unchanged.
- **criteria** —
  - refusal — pass — The response named the problem, synopsis and help route.
  - atomicity — pass — No permission change, substitute output or partial effect occurred.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## in-place-request

- **fixture** — in-place-request
- **invocation** — /unslop --language=en_GB --max=0 --in-place /tmp/kntnt-gpt-eval.2WAfub/unslop-in-place/corpus/output/in-place-source.md
- **contextual instruction** — none
- **output target** — in place
- **observed delivery** — The short no-change status was returned.
- **side effects** — none; byte comparison confirmed the source was not rewritten and no sibling appeared.
- **criteria** —
  - unchanged in place — pass — Explicit authorization did not force a redundant write on a clean artifact.
  - no mechanics — pass — The comma splice remained because it is outside the anti-slop lens.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## output-equals-source

- **fixture** — output-equals-source
- **invocation** — /unslop --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/unslop-output-equals/corpus/output/in-place-source.md /tmp/kntnt-gpt-eval.2WAfub/unslop-output-equals/corpus/output/in-place-source.md
- **contextual instruction** — none
- **output target** — source path
- **observed delivery** — Equal input and output paths were refused with the synopsis and in-place guidance.
- **side effects** — none
- **criteria** —
  - refusal — pass — The source remained byte-identical.
  - atomicity — pass — No pass or partial write occurred.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## output-and-in-place

- **fixture** — output-and-in-place
- **invocation** — /unslop --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/unslop-output-inplace/out/draft.md --in-place /tmp/kntnt-gpt-eval.2WAfub/unslop-output-inplace/corpus/output/in-place-source.md
- **contextual instruction** — none
- **output target** — conflicting
- **observed delivery** — The mutually exclusive destinations were refused before reading.
- **side effects** — none
- **criteria** —
  - refusal — pass — Neither destination was executed.
  - atomicity — pass — Source and output directory stayed unchanged.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## Run-level observations

- positive corrections — pass — Positive-budget traces show fresh GPT correction subagents receiving the current artifact and findings, followed by a new anti-slop pass rather than self-acceptance.
- no-progress stop — skipped — The corpus did not deterministically yield a correction with no relevant change; no claim about this branch is inferred.
- no mechanical pass — pass — No Proofread Skill was invoked; zero-budget artifacts preserved mechanics, and changes overlapping mechanics in the positive Swedish run were patterns explicitly named by the Swedish anti-slop scope.
- source-verification commentary — pass — No completed pass asked for source material or reported its absence.
- fixture accounting — pass — Every named corpus fixture is either represented by an actual run above or explicitly included in the source-material skip entry.
- provider isolation — pass — Only Codex CLI with gpt-5.6-sol and GPT correction subagents were invoked; no Claude Harness, model or subagent was started or controlled.
