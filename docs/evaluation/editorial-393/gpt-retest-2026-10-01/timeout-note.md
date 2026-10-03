# Native-session outer timeout

Recorded before further invocations on 2026-10-01. The preserved native runner accepts an explicit timeout argument; its default is 1 800 seconds. That was used by `r01`, the refused `r15`, and the currently running `r02` and `w01`.

Observed same-seat work in the parallel unchanged-product evaluation already took 1 530.67 and 1 821.36 seconds for two completed Write sessions with two source comparisons. The latter was not interrupted because that evaluation set a longer outer timeout. This demonstrates that the historical default can cut off a normally progressing xhigh session.

Further invocations here therefore select 5 400 seconds. This changes no product, input, repetition count, criterion, judge brief, seat or frozen plan. It removes an outer evaluator deadline as a plausible false failure. A started invocation keeps the timeout with which it started. If one is cut off, its complete retained partial evidence is classified as an instrumentally interrupted void and rerun on the same input under the existing interruption rule. It is never scored as a quotation defect or omitted.
