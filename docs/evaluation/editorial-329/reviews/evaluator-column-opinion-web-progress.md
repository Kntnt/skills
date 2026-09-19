# Column/opinion/web-copy evaluator progress

This is a continuation deliverable for the independent technical reviewer/evaluator, not runtime Skill guidance.

Original candidate `d60c4fcc0228ae37b348c57374f4d8c6ead5a0bd`, frozen corpus `6e531f5fe0b610e046ae58787f246cc6239acbcc`: seven pairs completed under `runs/candidate/` (column sv/en_GB, opinion sv/en_GB, web-copy sv/en_GB/en_US). All fourteen private roots are removed, with cleanup.json per invocation. Exact artifacts are `artifact.md` and `final.md` at case level; response.txt retains commentary. Separate complete original records are `write-gpt-2026-09-19-338-part-column-opinion-web.md` and the corresponding redline record. Their final section documents transferred cases.

Filed native sub-issues of #329: #342 (column invented personal self-attribution; sv initial pass explicitly corrected to fail), #343 (opinion en_GB changes non-opposition to support), #345 (web-copy en_GB refers to absent “form below”, missed by original Redline). Local defect bodies and follow-up evidence are under `defects/`. Parent owns product changes and column reruns. Do not modify product files or rerun another provider.

Final candidate authorized by parent: `2bd2afe34f6ec5d9d6587c33b1c16eeaf241579f`. Remaining owned work: the Redline-only regression of the original web-copy-en_GB artifact, then all three web-copy locales plus explicit web-copy-abt in `runs/rerun-345/`; then all three opinion locales in `runs/rerun-343/`. Exact prompts are unchanged under `harness/candidate-prompts/`. Separate write/redline records `*-gpt-2026-09-19-345-web-copy.md` and `*-gpt-2026-09-19-343-opinion.md` are initialized and filled as runs complete.

Current run at this checkpoint: `runs/rerun-345/web-copy-en_GB-regression/redline`, tool exec session 40936. It has identified the absent form and announced correction but is not yet complete. After completion inspect all native child sessions and full before/after claims, retain final artifact, classify exact filesystem changes, then delete the literal root shown by result.json. The run harness registers each root/process group and deliberately leaves roots for evaluator cleanup.

Functions-session helpers are stored as `audit`, `record`, `record345`, `record343`, `startWrite345`, `startRedline345`, `startWrite343`, `startRedline343`. They only capture/format evaluator evidence and start immutable native runs; they do not judge results. Original helpers target d60c4fc and must not start further original runs. All actual runs use `harness/run.py`, with no model/effort override; verify gpt-6-astra/high in every native rollout. Run serially so correction agents have room.

After the batch, parent requests independent final review of the final norm package, parent's column/selection evidence and full coverage. The earlier technical-review.md predates the completed evaluation and must not be misrepresented as final acceptance.

## Checkpoint after web-copy-en_GB rerun

Final revision boundary is now `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd` for all remaining pairs. The #345 regression and complete web-copy-sv pair use `2bd2afe`; both pass, with regression handoff-encryption method limit recorded. web-copy-en_GB complete pair on 1a4 passes. web-copy-en_US Write on 1a4 passes and Redline is currently running (runner exec session 8026). All completed roots are removed with audit evidence. Remaining: finish en_US Redline, web-copy-abt pair, all opinion sv/en_GB/en_US pairs, independent final package/coverage review. Helper functions startWrite345/startRedline345/startWrite343/startRedline343 now use 1a4. All original failed cases and their no-change findings accounts remain visible.
