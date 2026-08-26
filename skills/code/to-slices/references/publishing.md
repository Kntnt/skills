# Recoverable GitHub publication

Read this reference after the owner has approved one complete graph. Publication is a recoverable transaction implemented with ordinary `gh` calls. The Frame Record path and framing commit are its identity, and the record remains the recovery baton until a complete read-back proves success.

## Prepare the expected set

Materialise the approved parent and child bodies in temporary files outside the repository. The parent carries the complete approved snapshot before the first child is created, with the Frame Record path and framing commit in `## Provenance`. Preserve those files until verification completes so the tracker can be compared with the approved bytes rather than with a reconstruction from memory.

Give every child a stable child provenance marker before any write. Hash the Frame Record's relative path, the full framing commit, and the child's one-based position in the approved snapshot as three newline-terminated UTF-8 fields with `git hash-object --stdin`; append `<!-- kntnt.to-slices-child:<object-id> -->` after the child's Vantage point content. This marker identifies publication recovery only: native relations remain the live graph, and later pipeline Skills continue to read the shared headings as their contract.

Resolve the repository owner and name from `git remote`, and resolve label and milestone identifiers before the first write. The decision issue receives the applicable scope labels and milestone but no executable ready label. Every executable child receives the scope labels, configured ready state, and milestone.

## Recover the parent

List issues in all states and select the one whose provenance contains the exact Frame Record path and framing commit. No match creates the decision issue with `gh issue create`; one exact match resumes it; several matches are a conflict and stop publication.

On recovery, compare the published parent with the approved parent. Permit only the mechanical replacement of provisional child titles by the issue references created from that same snapshot. A material body, label, milestone, or state difference means another actor changed the publication: report the conflict and preserve the Frame Record rather than overwriting it.

## Publish children and relations

Create or recover children in dependency order so every blocker has an issue identity before its downstream edge is written. Before creating one, list issues in all states and recover every child globally by its stable child provenance marker: no match creates it, one exact match recovers it even when interruption left it without a parent relation, and several matches are a conflict. Compare a recovered issue's title and body with its expected temporary file before repairing relations; a same-titled issue without the marker is not the child.

Create a missing child with `gh issue create --body-file=<path>` and the configured labels and milestone. Attach it through GitHub's native parent relation with `gh api --method POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<child-database-id>`. If the repository's GitHub surface does not expose sub-issues, add the contract's `Parent: #<parent>` fallback to the child body instead. A transient or authorization error is a failed write, not evidence that the feature is absent.

After every child identity exists, write each native blocking relation with `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-database-id>`. If the repository's GitHub surface does not expose issue dependencies, write the contract's `Blocked by: #<blocker>, ...` fallback instead. A child with no blockers uses the explicit textual `Blocked by: None` only on that fallback surface.

Replace each provisional child title in the parent snapshot with its published `#<number>` reference while retaining delivered behaviour, seam, blockers, and Solo Ticket status. Edit only the parent recovered from the provenance pair.

## Verify before consumption

Use `gh issue view` for bodies, state, labels, and milestone, and `gh api` for the relation surfaces, then read the decision issue and every child back. Compare the parent and children with the approved set, including body, state, labels, milestone, parentage, and every blocking edge. On a fallback surface, verify the exact `Parent` and `Blocked by` lines instead of native relations.

The successful fixture is the complete expected parent, every expected child, and every expected relation. The partial fixture is any missing, extra, or conflicting member of that set. A create or edit command returning successfully does not move the partial fixture into the successful one; only the complete read-back does.

| Fixture | Read-back | Required action |
| --- | --- | --- |
| Complete | Parent `#200`; children `#201` and `#202`; both parent relations; `#202` blocked by `#201`; every body, state, label, and milestone agrees | Delete the Frame Record |
| Partial | Parent `#200`; children `#201` and `#202`; parent relation for `#202` missing; every other field agrees | Preserve the Frame Record; recover `#202` by its marker and repair only the relation |

Only after every comparison succeeds, delete the Frame Record. If any comparison or `gh` call fails, preserve the Frame Record and report the parent, each child created or recovered, each relation present, every missing relation or issue, and the exact conflict or command failure. Re-invocation repeats discovery from provenance, creates only what is missing, repairs only missing relations, and never duplicates or silently overwrites tracker state.
