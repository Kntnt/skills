# Independent source-fidelity diagnosis

Read-only diagnosis against `7ff6ec048f136ad797117a71c7b148843ab2e15e`. No product edits or model evaluations were performed. The complete original handoff, current Write body/help/quotation policy, base and web craft contracts, opinion and case-study genres, the three composition scopes, evaluation protocol, and full #349/#352 threads were read. This report is a reviewer deliverable, not a new runtime contract.

## Observations

Both defects violate the existing source-fidelity contract. Neither is excused by genre convention, brevity, or an otherwise accurate draft.

- **#349 is repeatable in the retained samples.** The source withholds an association's claim to have costed or funded a trial. Final Swedish Write says it has not costed the trial or arranged funding; final GB and US Write say it has neither costed nor funded the proposal. The `rerun-349-source-check` traces show actual loading of both the base distinction between unknown/unclaimed and known absent and Write step 6's requirement to check each factual or attributed claim. This is not explained by missing resources. It occurs in both first and third person and in Swedish as well as English, so pronoun conversion and translation cannot independently explain it. The previous GB attempt preserved the funding qualification but still asserted absent costing; the failure concerns semantic scope, not one fixed string.
- **#352 invents a small event in connective narration.** The supplied material establishes an email interview and Lind's actual assessment. The final US case adds “Asked to assess the experience”. That a question is plausible does not establish that it was asked. The quotation itself is accurate. The trace loads base Claims, including circumstantial detail, Write's source-check completion criterion, the quotation policy, and the selected case genre. This is not a quotation-repair permission being applied correctly; it is an added claim outside the quotation.
- **The local check has no observable output boundary.** In all three final opinion traces and the final US case trace, the tool sequence reads the source, invokes the skill, loads the contracts and composition scope, checks scratch cleanup, and delivers the draft. There is no separate draft/check artifact or separate checker execution. That observation does **not** establish that the model performed no internal checking; the available evidence establishes only that whatever checking occurred did not reject these claims.
- **The accounts can repeat the mistake.** The Swedish final opinion account says the gaps are preserved in the text even though its body asserts categorical absence. A writer's own completion account is therefore not an adequate independent correctness signal.

Primary evidence:

- [Opinion source](../../../corpus/editorial-quality/sources/opinion.md) and final [sv](../../runs/rerun-349-source-check/opinion-sv/write/response.txt), [GB](../../runs/rerun-349-source-check/opinion-en_GB/write/response.txt), [US](../../runs/rerun-349-source-check/opinion-en_US/write/response.txt) responses. Each response's directory contains `trace.jsonl`, `run.json`, native sessions, and full inventories.
- [Case source](../../../corpus/editorial-quality/sources/case-study.md), [US artifact](../../runs/rerun-341-translation/case-study-en_US/write/artifact.md), and [US trace](../../runs/rerun-341-translation/case-study-en_US/write/trace.jsonl).
- The opinion reruns used instruction revision `d0b2c99`; the case used `29ff204`. Both used corpus `6e531f5`, native Codex CLI 0.155.1 and observed `gpt-6-astra/high`. The current product preserves the relevant rules.

## Contract and execution seams

There is no literal instruction authorising either false claim. The base forbids invented connections, demands supported circumstantial details, and explicitly preserves the state of knowledge. Case-study's request for a bridge that prepares a quotation is bounded by those rules. Opinion's demand for a persuasive voice expressly preserves supplied positions.

There is, however, a workflow seam worth testing. Write prominently says “No review pass” and ends by reserving reviewing for later invocations, while step 6 incorporates claim checking into composition. These statements can be reconciled: checking source support is part of producing a truthful first draft, while Redline performs a broader editorial review. Yet the body does not give that check a distinct task boundary or an independently inspectable result. Adding another general reminder has already failed to demonstrate a repair. A separately assigned, source-aware comparison would materially change execution rather than merely restate the invariant.

A second seam is the unit of attention. Main propositions, figures and quotation wording are conspicuous. Negation over a claim and a small introductory participial phrase can be treated as paraphrase or connecting language even though both change what happened. Current rules cover them semantically; the evidence does not show that the writer consistently recognises them as claims to compare.

## Three falsifiable causes

These are hypotheses, not findings about hidden reasoning.

| Hypothesis | Discriminating experiment | Evidence against it |
|---|---|---|
| **Source meaning is compressed into its likely practical implication.** “No claim of funding” becomes “no funding”, helped by the following need for a cost decision. | Freeze contrast sets where work is explicitly completed, explicitly not completed, unclaimed, or unstated. Hold the practical decision constant; compare original-language and translated drafts. Also present the exact failed claim and original source to a checker without the writer's explanation. | A checker still accepts categorical absence after explicitly identifying the no-claim scope; or the same failures occur on simple affirmative facts. That would point beyond paraphrase compression alone. |
| **Narrative bridges escape claim identification.** A standard interview transition is classified as form rather than a factual event. | Use matched source packages containing an actual question/request in one version and only the answer in another. Add fresh cases involving sequence, motive or observation in connective wording. Check the complete article, not just quotations and numbers. | Equal false-event rates in prominent standalone claims and small bridges, or a checker lists the bridge as an unsupported event but the delivered version retains it. That would shift blame to integration rather than detection. |
| **Composition and self-check share the same mistaken interpretation.** The same agent validates its own fluent paraphrase without confronting the completed wording against source passages. | Compare unchanged Write with a bounded, fresh source-aware check of its completed draft, using the same model identity and fixed cases. Record detection separately from the parent's accepted repair and final text. A same-context check can serve as a cheaper comparison if feasible. | Fresh checking offers no consistent detection/repair advantage, or its benefit disappears on new cases while retaining only the known examples. That would undermine the proposed context boundary as the remedy. |

The current evidence already rejects “first-person conversion alone”, “English translation alone”, and “the rule was not loaded” as sufficient explanations for #349. It does not establish a population failure rate or prove that all source-fidelity defects share one cause.

## Assessment of a separate check

A fresh source-aware check **is warranted as a bounded experiment**. Repeated reminders have not fixed #349, while #352 supplies an additional kind of overlooked claim. It is not yet justified to promise that delegation solves either problem or to add a broad editorial pipeline to Write.

The useful comparison task would receive the complete assembled source material, the exact candidate artifact including headings, and the existing source-fidelity standard. It would identify unsupported or strengthened claims and the relevant source support or absence, without judging general style. The writer would own the repair. The delivered text, rather than the checker report, remains the acceptance object. If a parent changes wording after a check, the unchecked wording cannot inherit the check's approval.

Costs and risks requiring explicit treatment:

- One extra model task adds latency and token cost; both grow with source length. Measure actual overhead on the ordinary five-genre cases as well as the failures.
- A mandatory child introduces a `subagents` capability dependency to a Skill currently requiring none. Body, help, metadata and tests must agree; an unavailable checker must not silently masquerade as completed verification.
- Passing a source summary would recreate the very loss of scope being investigated. Full relevant source access matters, including conversational material and the meaning of omissions.
- A checker can itself share the model's entailment error, miss a claim, invent a problem, or remove warranted certainty. Positive controls with explicit negation, genuine questions, supported causal facts and intentional voice are necessary.
- Broad “improvement” would duplicate Redline and risk blandness or scope creep. Source fidelity has to remain the bounded task; new review halves and generic style editing would confound the experiment.
- Reports and temporary artifacts create observable file effects. Preserve them in evaluation evidence, but ordinary response delivery must clean its own scratch and not alter source files.
- A source-aware correction may fix these cases while generating a new unsupported inference elsewhere. Judge the complete final text and keep every failed attempt. A later single pass does not establish reliability.

#341 remains a separate lower-priority idiom problem. Its source is intelligible; the final Swedish Write translates the building-start metonymy awkwardly, while the later source-blind Redline repairs it. A source-support checker might reasonably accept the original as semantically faithful and cannot be counted as a language-quality fix. Keep a translation preservation case in regression coverage without widening this source-check task into idiom review.
