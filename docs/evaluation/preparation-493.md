# The #486 preparation and judging mismatch

This is an additive diagnosis for #493, written on 2026-10-03 against
`4cf05813`. The committed #486 plan, fixtures, four validations, eight contrast
judgements and dated record remain unchanged. This diagnosis supplies future
preparation guidance; it does not regrade those results or infer a product
defect from their conformance assumption.

## What was validated and what was frozen

The [plan](editorial-486/plan.md) froze both contrasts and their expectations
before validation. Its [validation brief](editorial-486/validation-brief.md)
asked each reader to examine the lead's assertion, inferential support,
follow-through and class. It explicitly supplied no contract or other file.
Both [inference readers](editorial-486/validation/article-inference-a/validation-a.md)
[agreed](editorial-486/validation/article-inference-b/validation-b.md) that the
denominator-based inference was supported and fulfilled. Both
[promise readers](editorial-486/validation/article-promise-a/validation-a.md)
[agreed](editorial-486/validation/article-promise-b/validation-b.md) that exact
sensor positions and window distances were promised but not supplied. Those
narrow classifications remain supported.

The [inference expectation](editorial-486/inputs/article-inference.expectation.md)
also says the article conforms to the anatomy. The
[promise expectation](editorial-486/inputs/article-promise.expectation.md) says
everything outside its promise finding conforms. Those are stronger claims than
the validation task established.

The actual [anatomy](../../skills/kntnt/library/references/editorial/article-anatomy.md)
requires the body to read complete without the standfirst, the lead to introduce
every person, thing and event it mentions, and nothing in the body to point
back to the standfirst. Its
[review guidance](../../skills/kntnt/library/references/editorial/article-anatomy.review.md)
requires the reviewer to cover the standfirst and name referents available only
there. This requirement existed before the campaign; no new wording or exception
is needed to make it apply.

## The concrete conflict

The [inference input](editorial-486/inputs/article-inference.md) starts its lead
with “De 14 lektionspassen”. The standfirst identifies those periods as the ones
with readings below the office's working threshold; the body only later gives
that condition. The inference remains sound, but support for the mathematical
relationship is separate from the lead's introduction of its subject.

The [promise input](editorial-486/inputs/article-promise.md) replaces the earlier
lead and thereby removes its introduction of the property office. The body's
first section still starts “Kontoret”, whose introduction is then supplied only
by the standfirst. An unfulfilled promise in the lead and a body-dependent
reference elsewhere are distinct findings.

| Actual run | Observed reference edit | Both original judgements |
| --- | --- | --- |
| Inference response | Lead names the measured subset and threshold | R1 fail; reference clarification called taste, alongside separate headline loss |
| Inference file | Lead adds the threshold condition to the fourteen periods | R1 fail, decided by the clarification |
| Promise response | Body names Fastighetskontoret | R1 fail; name expansion called taste, alongside separate headline loss |
| Promise file | Body names Fastighetskontoret | R1 fail, decided by the name expansion |

The two file artifacts establish the exact differences independently of their
reports: [inference before](editorial-486/runs/pre-article-inference-file-1/supplied-input.md)
and [after](editorial-486/runs/pre-article-inference-file-1/captured-output.md);
[promise before](editorial-486/runs/pre-article-promise-file-1/supplied-input.md)
and [after](editorial-486/runs/pre-article-promise-file-1/captured-output.md).
The [source audit](preparation-493-audit.json) retains all source digests,
both complete comparisons and every deciding judgement.

Both [control judge briefs](editorial-486/control-judge-brief.md)
[restricted](editorial-486/control-judge-brief-file.md) readers to the artifact,
reply and frozen expectation, excluding other resources. The judges therefore
applied the stipulated conformance rather than the actual body-independence
contract. The mismatch originated in the replaced fixtures' unexamined anatomy,
was promoted by the expectation, and was reinforced by restricted judging
material. It was not introduced by the two valid target classifications.

The response headline findings remain separate, and no claim here reverses
their failures. The original judges' file-reference readings remain visible
beside the contract-based explanation; the file R1 outcomes are not changed.
The valid denominator inference and genuine unfulfilled promise remain useful
distinctions, without a blanket claim that their original fixtures were clean.

## The prospective correction

[Complete-contract preparation](harness/README.md) now precedes the final
evaluation freeze. Two fresh readers of complete texts and every actual
selected resource assess counted anatomy and semantic anatomy separately,
then assess the target distinction separately from other defects. Known defects
are declared; global conformance requires both complete reports. An invalid
proposal is preserved and replaced only under the preparation's finite bound.

Judge packets carry the applicable frozen contract and complete validation
scope, rather than an unsupported expected pass. A conflict between expectation
and contract is reported as a method obstacle, not evidence that the Skill
needs a wording change. This corrects future preparation and judging without
weakening body independence, broadening correction authority, or editing any
old freeze. [ADR-0245](../adr/0245-complete-contract-preparation-precedes-a-conformance-freeze.md)
records the trade-off.
