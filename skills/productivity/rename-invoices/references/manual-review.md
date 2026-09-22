# Manual review

Read this reference only for plan items whose `status` is `needs_review`. Resolve only the fields named in `issues` and preserve every field the script already established.

## Evidence boundary

Use evidence from extracted PDF contents only. Never use the original filename, surrounding conversation, an assumed document category, download time, or processing order as evidence. The invocation's exact `--type` value is authoritative and must not be inferred or changed during review.

## Date

Use the semantic date sources configured for the selected type, in their configured priority. Exclude due dates, settlement dates, download dates, filing dates, and service periods unless one of those meanings is itself an explicitly configured date source.

Write a reviewed date override as zero-padded ISO `YYYY-MM-DD`. Do not guess the order of an ambiguous numeric date; leave it unresolved when document language or configuration does not establish the order.

## Counterparty

Use the configured party role: `issuer` selects the seller, supplier, or provider, while `recipient` selects the customer or buyer. Do not substitute a payment processor or merchant-of-record intermediary when the PDF explicitly identifies the underlying provider.

Prefer a recognizable common brand when the document establishes it. Remove a legal suffix only when the configured suffix list makes that normalization explicit. Do not guess a party from the source filename.

## Description

Descriptions are optional unless a local filename convention makes them operationally necessary. Use a short product, service, engagement, or period description evidenced by the document. Set `description` to `null` to omit it deliberately.

## Identifier and collision

Preserve an explicit invoice, receipt, credit-note, or transaction identifier exactly, including prefixes, dashes, and leading zeros. An `always` policy requires it for every item. A `collision` policy adds identifiers only when otherwise identical targets collide and every colliding identifier is explicit and unique. A `never` policy omits it.

Never invent sequence suffixes such as `(2)` and never derive an identifier from processing order.

## Overrides

Create a JSON object keyed by each exact source filename and include only fields named in `issues`:

```json
{
  "unknown.pdf": {
    "counterparty": "Acme",
    "date": "2026-09-01"
  }
}
```

Allowed fields are `counterparty`, `date`, `description`, and `identifier`. Use `null` only for an optional description. Run `plan` again with `--overrides=FILE`; editing `plan.json` directly invalidates its `plan_id`.
