- **record** — redline-gpt-2026-08-26
- **date** — 2026-08-26
- **ticket** — #159
- **skill** — redline
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
  - applicability — skipped — These are source-material fixtures for a drafting Skill; Redline receives the resulting Text Artifact and does not compare it with sources.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Every source fixture is named here rather than omitted.

## clean-en-GB

- **fixture** — clean-en-GB
- **invocation** — /redline --language=en_GB --max=3 /tmp/kntnt-gpt-eval.2WAfub/redline-clean/corpus/prose/clean-en-GB.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The short no-change status was returned.
- **side effects** — none
- **criteria** —
  - clean review — pass — No substantive finding or correction was invented.
  - early stop — pass — The budget of three remained unspent and no correction subagent was started.
  - closing Proofread — pass — The trace shows one final explicit en_GB Proofread pass and no later edit.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — This run also exercises response-default and unchanged-result delivery.

## flawed-en-US

- **fixture** — flawed-en-US
- **invocation** — /redline --language=en_US --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-flawed-zero/corpus/prose/flawed-en-US.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The mechanically corrected artifact and four unresolved editorial findings were returned.
- **side effects** — none
- **criteria** —
  - initial review — pass — The review identified unsupported and incomplete argumentation without treating mechanics as findings.
  - zero budget — pass — No substantive correction occurred.
  - closing Proofread — pass — The listed mechanics were corrected at the end while the explanatory comma remained.
  - unresolved delivery — pass — All substantive findings accompanied the complete resulting artifact.
- **unresolved findings** — Four findings about the comparison, unsupported behaviours, unexplained discrepancies and an unrelated sentence.
- **defects filed** — none
- **notes** — none

## flawed-sv

- **fixture** — flawed-sv
- **invocation** — /redline --language=sv --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-flawed-sv-zero/corpus/prose/flawed-sv.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The mechanically corrected Swedish artifact and four unresolved editorial findings were returned in Swedish.
- **side effects** — none
- **criteria** —
  - initial review — pass — The run found contextual and evidentiary losses.
  - zero budget — pass — No substantive correction occurred.
  - closing Proofread — pass — Swedish mechanics were corrected while the valid pronoun hen and the argument were preserved.
- **unresolved findings** — Four findings about unidentified context, indirect support, incomparable counts and an over-certain generalisation.
- **defects filed** — none
- **notes** — none

## slop-heavy

- **fixture** — slop-heavy
- **invocation** — /redline --language=en_GB /tmp/kntnt-gpt-eval.2WAfub/redline-slop-default/corpus/prose/slop-heavy.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — One correction round reduced the six-paragraph body to two short paragraphs and returned one unresolved finding.
- **side effects** — none
- **criteria** —
  - anti-slop detection — pass — The initial review recognized the fixture's named patterns.
  - fresh correction and re-review — pass — The trace shows a fresh correction subagent and a new review before delivery.
  - preservation — fail — The correction removed most claims together with the patterns, a substantive edit outside the permitted smallest repair.
  - unresolved delivery — fail — Removed claims disappeared rather than remaining or being reported unresolved.
- **unresolved findings** — The two surviving paragraphs still assert their central trade-off without evidence or example.
- **defects filed** — #173
- **notes** — The default budget was exhausted after one round.

## slop-heavy-sv — inferred

- **fixture** — slop-heavy-sv
- **invocation** — /redline --max=1 /tmp/kntnt-gpt-eval.2WAfub/redline-slop-sv-infer/corpus/prose/slop-heavy-sv.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — One fresh correction round returned a much shorter Swedish artifact with three unresolved findings.
- **side effects** — none
- **criteria** —
  - language inference — pass — Swedish was inferred and used for review and delivery.
  - Swedish anti-slop — pass — Shared and Swedish-specific patterns were recognized rather than matched only as English strings.
  - fresh correction and re-review — pass — The trace shows a fresh subagent, re-review and then one final Proofread pass.
  - preservation — fail — Entire content-bearing passages were deleted together with their patterns, reproducing #173.
- **unresolved findings** — Three unsupported sets of claims about chatbot learning, behaviour and the effect of service design.
- **defects filed** — #173
- **notes** — none

## code-carrying

- **fixture** — code-carrying
- **invocation** — /redline --language=en_GB --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-code-en/corpus/prose/code-carrying.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The mechanically corrected prose, byte-preserved code and six unresolved editorial findings were returned.
- **side effects** — none
- **criteria** —
  - anti-slop review — pass — Findings named patterns in prose.
  - code boundary — pass — No finding targeted fenced, indented or inline code and every code byte remained unchanged.
  - closing Proofread — pass — Prose mechanics were corrected while baited mechanics inside code remained.
- **unresolved findings** — Six prose-only editorial findings.
- **defects filed** — none
- **notes** — none

## code-carrying-sv — inferred

- **fixture** — code-carrying-sv
- **invocation** — /redline --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-code-sv-infer/corpus/prose/code-carrying-sv.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The mechanically corrected Swedish prose, byte-preserved code and six unresolved findings were returned.
- **side effects** — none
- **criteria** —
  - language inference — pass — Swedish was inferred without a prompt.
  - anti-slop review — pass — Findings reached the Swedish prose patterns.
  - code boundary — pass — Fenced, indented and inline code remained byte-identical and produced no finding.
  - closing Proofread — pass — The four prose errors were corrected while their code counterparts remained.
- **unresolved findings** — Six prose-only findings.
- **defects filed** — none
- **notes** — none

## resembles-abt

- **fixture** — resembles-abt
- **invocation** — /redline --language=en_GB --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-resembles/corpus/prose/resembles-abt.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The unchanged artifact and one title finding were returned.
- **side effects** — none
- **criteria** —
  - technique non-inference — pass — ABT was neither selected, reported nor imposed.
  - review scope — pass — The finding concerned the article title, not the unselected technique.
  - closing Proofread — pass — The valid opening Therefore remained unchanged.
- **unresolved findings** — The title names the subject rather than the angle.
- **defects filed** — none
- **notes** — none

## mixed-language

- **fixture** — mixed-language
- **invocation** — /redline --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-mixed/corpus/prose/mixed-language.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The run asked whether Swedish or English rules should apply and stopped.
- **side effects** — none
- **criteria** —
  - ambiguous language — pass — No language was guessed and no review, correction, Proofread pass or write occurred.
- **unresolved findings** — The caller must choose Swedish or English.
- **defects filed** — none
- **notes** — none

## handoff-present

- **fixture** — handoff-present
- **invocation** — /redline --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-handoff-present/corpus/frontmatter/handoff-present.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The complete artifact and three unresolved findings were returned.
- **side effects** — none
- **criteria** —
  - metadata precedence — pass — Article, ABT and en_GB came from the recognized map.
  - metadata synchronization — pass — The normalized map was preserved without unrelated changes.
  - review delivery — pass — Findings accompanied the artifact and no source-verification caveat appeared.
- **unresolved findings** — Genre mismatch, a title promise not fulfilled and an unsupported false contrast.
- **defects filed** — none
- **notes** — none

## handoff-conflicting

- **fixture** — handoff-conflicting
- **invocation** — /redline --genre=article --language=sv --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-handoff-conflicting/corpus/frontmatter/handoff-conflicting.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The complete Swedish artifact was returned with synchronized metadata and no unresolved finding.
- **side effects** — none
- **criteria** —
  - per-field precedence — pass — Formal article and Swedish values overrode metadata while PAC fell through independently.
  - metadata synchronization — pass — The delivered map contains article, PAC and sv.
  - review and mechanics — pass — No substantive correction occurred and the closing pass left the clean body alone.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## handoff-partial

- **fixture** — handoff-partial
- **invocation** — /redline --genre=report --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-handoff-partial/corpus/frontmatter/handoff-partial.md -- Swedish is the language.
- **contextual instruction** — Swedish is the language.
- **output target** — response
- **observed delivery** — The complete artifact, synchronized map and five unresolved findings were returned.
- **side effects** — none
- **criteria** —
  - per-field precedence — pass — Genre came from the flag, technique from the partial map and language from Contextual Instruction.
  - metadata synchronization — pass — The map now contains report, ABT and sv.
  - full-contract review — pass — The mixed-language body remained a finding under explicitly resolved Swedish.
- **unresolved findings** — Five report, support, decision-criteria, language-consistency and claim-support findings.
- **defects filed** — none
- **notes** — none

## handoff-unusable

- **fixture** — handoff-unusable
- **invocation** — /redline --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-handoff-unusable/corpus/frontmatter/handoff-unusable.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The run reported en_UK as unusable metadata and stopped.
- **side effects** — none
- **criteria** —
  - unusable metadata — pass — The value was not reinterpreted as en_GB.
  - atomicity — pass — No review, Proofread pass or write preceded the stop.
- **unresolved findings** — The caller must choose an installed language.
- **defects filed** — none
- **notes** — none

## slop-heavy-sv — explicit

- **fixture** — slop-heavy-sv
- **invocation** — /redline --language=sv --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-slop-sv-explicit/corpus/prose/slop-heavy-sv.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The complete Swedish artifact and nine detailed findings were returned.
- **side effects** — none
- **criteria** —
  - Swedish anti-slop — pass — Shared and language-specific patterns were found throughout.
  - zero budget — pass — No substantive correction occurred.
  - closing Proofread — fail — The run changed quotation marks but left several mechanics errors that direct Proofread corrects, so the required complete closing pass did not occur.
- **unresolved findings** — Nine angle, support, attribution, opening, cycling, rhythm, inflation, connective and conclusion findings.
- **defects filed** — #174
- **notes** — none

## code-carrying-sv — explicit

- **fixture** — code-carrying-sv
- **invocation** — /redline --language=sv --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-code-sv-explicit/corpus/prose/code-carrying-sv.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Corrected Swedish prose, byte-preserved code and five unresolved findings were returned.
- **side effects** — none
- **criteria** —
  - explicit language — pass — Swedish rules were applied without relying on inference.
  - code boundary — pass — All three code forms remained byte-identical and produced no finding.
  - closing Proofread — pass — The four prose mechanics errors were corrected and their code counterparts remained.
- **unresolved findings** — Five prose-only findings.
- **defects filed** — none
- **notes** — none

## locale-divergent — en_GB

- **fixture** — locale-divergent
- **invocation** — /redline --language=en_GB --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-locale-gb/corpus/prose/locale-divergent.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — A British English result and two unresolved content findings were returned.
- **side effects** — none
- **criteria** —
  - British forms — pass — Organised, licence, judgement and the pound figure remained valid.
  - ambiguous date — fail — The closing Proofread expanded 3/4 to 3 April on a locale assumption.
  - review scope — pass — The two unresolved findings concern missing licence identities and unsupported treatment of the smaller tool.
- **unresolved findings** — Two content findings.
- **defects filed** — #166
- **notes** — This reproduces the already filed nested Proofread defect.

## locale-divergent — en_US

- **fixture** — locale-divergent
- **invocation** — /redline --language=en_US --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-locale-us/corpus/prose/locale-divergent.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — An American English result and three unresolved locale-register findings were returned.
- **side effects** — none
- **criteria** —
  - locale mechanics — pass — Spelling and quotation punctuation were normalized while numeric 3/4 remained untouched.
  - review delivery — pass — British lexical choices outside mechanics were reported rather than silently rewritten at budget zero.
- **unresolved findings** — Autumn, minute and has got were reported as British lexical choices under en_US.
- **defects filed** — none
- **notes** — none

## frontmatter-unrelated

- **fixture** — frontmatter-unrelated
- **invocation** — /redline --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-frontmatter-unrelated/corpus/frontmatter/frontmatter-unrelated.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The artifact and three unresolved findings were returned.
- **side effects** — none
- **criteria** —
  - configuration boundary — pass — Top-level bait keys were ignored.
  - frontmatter preservation — pass — Every unrelated frontmatter line remained unchanged and no Kntnt map was added.
- **unresolved findings** — Missing third note and two unsupported-claim findings.
- **defects filed** — none
- **notes** — none

## frontmatter-absent

- **fixture** — frontmatter-absent
- **invocation** — /redline --max=0 /tmp/kntnt-gpt-eval.2WAfub/redline-frontmatter-absent/corpus/frontmatter/frontmatter-absent.md
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — The artifact and one unresolved support finding were returned.
- **side effects** — none
- **criteria** —
  - metadata optionality — pass — No metadata was demanded and no map was added.
  - review delivery — pass — The complete artifact accompanied the finding.
- **unresolved findings** — Broad team-behaviour claims lack support.
- **defects filed** — none
- **notes** — Same material is used for several output situations below.

## new-file

- **fixture** — new-file
- **invocation** — /redline --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/redline-new-file/out/draft.md /tmp/kntnt-gpt-eval.2WAfub/redline-new-file/corpus/frontmatter/frontmatter-absent.md
- **contextual instruction** — none
- **output target** — /tmp/kntnt-gpt-eval.2WAfub/redline-new-file/out/draft.md
- **observed delivery** — The response named the created file and reported one unresolved finding without repeating the artifact.
- **side effects** — Created exactly out/draft.md; the source was unchanged.
- **criteria** —
  - new file — pass — The full result reached the exact destination.
  - unresolved routing — pass — The finding remained in the response beside the file.
- **unresolved findings** — Unsupported broad claims about teams.
- **defects filed** — none
- **notes** — none

## existing-file

- **fixture** — existing-file
- **invocation** — /redline --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/redline-existing-file/corpus/output/existing-target.md /tmp/kntnt-gpt-eval.2WAfub/redline-existing-file/corpus/frontmatter/frontmatter-absent.md
- **contextual instruction** — none
- **output target** — the staged existing-target.md
- **observed delivery** — The occupant was replaced and two findings were reported beside the path.
- **side effects** — Replaced exactly existing-target.md; no sibling was created.
- **criteria** —
  - existing destination — pass — The explicit path authorized replacement without confirmation.
  - unresolved routing — pass — Findings appeared in the response rather than inside the file.
- **unresolved findings** — Unsupported broad claims and inconsistent roster/rota terminology.
- **defects filed** — none
- **notes** — none

## existing-directory

- **fixture** — existing-directory
- **invocation** — /redline --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/redline-existing-dir/out /tmp/kntnt-gpt-eval.2WAfub/redline-existing-dir/corpus/frontmatter/frontmatter-absent.md
- **contextual instruction** — none
- **output target** — the staged empty out directory
- **observed delivery** — The derived frontmatter-absent.md was created and two findings were reported.
- **side effects** — Created exactly out/frontmatter-absent.md; the source was unchanged.
- **criteria** —
  - derived filename — pass — The name came from the source and retained a text extension.
  - closing Proofread — pass — One comma splice was corrected only in the delivered result.
- **unresolved findings** — Two unsupported broad-claim findings.
- **defects filed** — none
- **notes** — none

## derived-name-collision

- **fixture** — derived-name-collision
- **invocation** — /redline --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/redline-collision/corpus/output/collision /tmp/kntnt-gpt-eval.2WAfub/redline-collision/corpus/output/interview-notes.md
- **contextual instruction** — none
- **output target** — the staged collision directory
- **observed delivery** — interview-notes-3.md was created and two findings were reported.
- **side effects** — Created only interview-notes-3.md; both occupants remained unchanged.
- **criteria** —
  - collision sequence — pass — The first free suffix was selected from the original stem.
  - unresolved routing — pass — Findings stayed in the response.
- **unresolved findings** — One unidiomatic phrase and one paragraph-movement finding.
- **defects filed** — none
- **notes** — none

## read-only-source

- **fixture** — read-only-source
- **invocation** — /redline --language=en_GB --max=0 --in-place /tmp/kntnt-gpt-eval.2WAfub/redline-readonly/corpus/output/readonly-source.md
- **contextual instruction** — none
- **output target** — in place
- **observed delivery** — The read-only source was refused before review.
- **side effects** — none; permissions and content remained unchanged.
- **criteria** —
  - refusal — pass — The problem, synopsis and help route were supplied.
  - atomicity — pass — No substitute output or partial effect occurred.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## in-place-request

- **fixture** — in-place-request
- **invocation** — /redline --language=en_GB --max=0 --in-place /tmp/kntnt-gpt-eval.2WAfub/redline-in-place/corpus/output/in-place-source.md
- **contextual instruction** — none
- **output target** — in place
- **observed delivery** — The source was replaced, one comma splice was corrected and three unresolved findings were reported.
- **side effects** — Replaced only in-place-source.md; no sibling was created.
- **criteria** —
  - explicit authorization — pass — Replacement occurred only under the in-place flag.
  - unresolved routing — pass — Findings remained in the response.
- **unresolved findings** — One contradiction and two unsupported-absolutes findings.
- **defects filed** — none
- **notes** — none

## output-equals-source

- **fixture** — output-equals-source
- **invocation** — /redline --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/redline-output-equals/corpus/output/in-place-source.md /tmp/kntnt-gpt-eval.2WAfub/redline-output-equals/corpus/output/in-place-source.md
- **contextual instruction** — none
- **output target** — source path
- **observed delivery** — The run refused the equal paths and pointed at in-place editing.
- **side effects** — none
- **criteria** —
  - refusal — pass — The source remained byte-identical.
  - atomicity — pass — No review or partial write occurred.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## output-and-in-place

- **fixture** — output-and-in-place
- **invocation** — /redline --language=en_GB --max=0 --output=/tmp/kntnt-gpt-eval.2WAfub/redline-output-inplace/out/draft.md --in-place /tmp/kntnt-gpt-eval.2WAfub/redline-output-inplace/corpus/output/in-place-source.md
- **contextual instruction** — none
- **output target** — conflicting
- **observed delivery** — The mutually exclusive destinations were refused with the synopsis.
- **side effects** — none
- **criteria** —
  - refusal — pass — Neither destination was executed.
  - atomicity — pass — Source and output directory stayed unchanged.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## Run-level observations

- positive corrections — pass — Each positive-budget correction visible in the Harness trace was delegated to a fresh GPT subagent with the complete current artifact and current findings, then reviewed again before delivery.
- no-progress stop — skipped — The corpus did not deterministically produce a correction that changed none of its named findings; no claim about that branch is inferred from another stop condition.
- source-verification commentary — pass — No completed review asked for source material or remarked that source verification was unavailable.
- closing Proofread — fail — Most runs show exactly one final pass and no later substantive edit, but the explicit Swedish slop run performed an incomplete pass as #174 records.
- fixture accounting — pass — Every named corpus fixture is either represented by an actual run above or explicitly included in the source-material skip entry.
- provider isolation — pass — Only Codex CLI with gpt-5.6-sol and GPT correction subagents were invoked; no Claude Harness, model or subagent was started or controlled.
