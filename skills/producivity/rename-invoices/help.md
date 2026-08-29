# rename-invoices

## NAME

rename-invoices - plan and apply safe filenames for accounting PDFs

## SYNOPSIS

**/rename-invoices** **--folder=**_PATH_ **--type=**_NAME_ [**--config=**_FILE_|**--no-config**] [**--locale=**_NAME_ ...] [**--locale-file=**_FILE_ ...] [**--prefix=**_TEXT_] [**--template=**_TEMPLATE_] [**--date-format=**_FORMAT_] [**--description-template=**_TEMPLATE_] [**--extension=**_EXTENSION_] [**--identifier-template=**_TEMPLATE_] [**--date-source=**_SOURCE_ ...] [**--counterparty-source=**_issuer_|_recipient_] [**--identifier-policy=**_always_|_collision_|_never_] [**--overrides=**_FILE_] [**--apply**] [**--** *INSTRUCTION*]

## DESCRIPTION

`rename-invoices` reads every PDF directly inside one deliberately selected folder, extracts text with Poppler, and builds deterministic filenames from an explicit document type and one or more configured locales. It does not search subdirectories, infer the document type, use OCR, or treat an existing filename as evidence.

The default run is non-mutating: it reports proposed old-to-new mappings, files already carrying their verified canonical names, and documents whose date, counterparty, description, identifier, extraction, or target collision still needs review. `--apply` authorizes only the fresh validated plan created during the same run. Source bytes and destinations are checked again before the first rename, and an edited or stale plan is refused.

Bundled settings define supplier invoices, receipts, customer invoices, and credit notes. A personal configuration below `~/.kntnt/rename-invoices/` may select locales, replace filename conventions, add document types, or add complete locales without changing the Skill.

## OPTIONS

**--folder=**_PATH_

Process the direct PDF children of this directory. The filesystem root and the user's home directory are refused as dangerously broad targets.

**--type=**_NAME_

Use this exact configured document type. The Skill never infers or aliases it.

**--config=**_FILE_

Use this TOML settings file instead of a discovered personal `config.toml`. It remains layered over the bundled defaults.

**--no-config**

Ignore discovered personal settings and personal locale files. One or more `--locale` flags are then required; explicit `--locale-file` flags remain valid.

**--locale=**_NAME_

Select a document locale. Repeat the flag for mixed-language folders; the first locale supplies localized standard filename prefixes. Repeated flags replace the configured locale list for this run.

**--locale-file=**_FILE_

Use one complete locale TOML file for its declared locale. Repeat as needed. Each supplied locale must also be selected by `--locale` or the settings file.

**--prefix=**_TEXT_

Override the selected document type's filename prefix.

**--template=**_TEMPLATE_

Override the complete filename template. It must retain the required date, counterparty, extension, and policy-dependent identifier fields.

**--date-format=**_FORMAT_

Override the `strftime` format used for the resolved document date.

**--description-template=**_TEMPLATE_

Override the optional description segment template.

**--extension=**_EXTENSION_

Override the output filename extension.

**--identifier-template=**_TEMPLATE_

Override the optional identifier segment template.

**--date-source=**_SOURCE_

Override the selected type's semantic date-source priority. Repeat in descending priority.

**--counterparty-source=**_issuer_|_recipient_

Choose which accounting party becomes the counterparty in the filename.

**--identifier-policy=**_always_|_collision_|_never_

Require identifiers on every filename, add them only to otherwise colliding filenames, or omit them.

**--overrides=**_FILE_

Read reviewed per-file semantic decisions from a JSON object keyed by exact source filename. Only unresolved fields may be supplied, and direct edits to a generated plan remain invalid.

**--apply**

Apply the fresh validated plan after review. This is the only form that renames files.

## FILES

**~/.kntnt/rename-invoices/config.toml**

Optional partial personal settings layered over the bundled defaults.

**~/.kntnt/rename-invoices/locales/**

Optional complete personal locale files named for their lowercase locale identifiers.

**config/config.toml**

Bundled complete settings and the authoritative settings example.

**config/locales/**

Bundled complete locale files.

## DIAGNOSTICS

An invalid, incomplete, unknown, or out-of-order form is refused rather than repaired or ignored. The Skill names the error, prints the SYNOPSIS, changes nothing, and points to `/rename-invoices --help`. A flag with no work to do is refused rather than ignored.

A missing `pdftotext`, invalid TOML, unknown configuration field, missing locale, unknown document type, empty folder, broad target folder, unreadable PDF, ambiguous date, unresolved counterparty, required identifier, or filename collision is reported before application. Reviewable document uncertainty remains visible as `needs_review`; application requires that count to be zero.

If a source changed, disappeared, or gained an occupied destination after planning, application is refused. A filesystem failure during the two-phase rename is reported after a best-effort rollback; the reported folder state is authoritative.

## EXAMPLES

Plan Swedish supplier-invoice names without changing files:

```text
/rename-invoices --folder=~/Accounting/Incoming --type=supplier-invoice --locale=sv
```

Apply receipt names across a mixed English and Swedish folder using personal defaults:

```text
/rename-invoices --folder=~/Accounting/Receipts --type=receipt --locale=en --locale=sv --apply
```

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Unaddressable is guidance with no addressable effect at all — guidance touching nothing this Skill's contract addresses — and never guidance a documented precedence has already settled against, which is suppressed instead: suppression is that precedence working, so the run continues and the delivery names the suppressed guidance beside the resolved configuration where saying so is useful. Only guidance that is part invalid — part conflicting, part scope-widening, or part unaddressable — goes unapplied as a whole; one parameter suppressed and another landing is an ordinary invocation. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

The following schematic cases pin the split independently of any one Skill's Formal Invocation grammar; `\n\n` denotes two newline characters in one payload.

| Case | Envelope | Formal Invocation | Contextual Instruction | Outcome |
| --- | --- | --- | --- | --- |
| Same line | `/skill --force -- Preserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Blank lines | `/skill --force --\n\nPreserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Empty suffix | `/skill --force --   ` | `/skill --force` | — | Syntax refusal |
| Later separator | `/skill -- Preserve -- deployment facts` | `/skill` | `Preserve -- deployment facts` | Envelope valid; formal grammar next |
| No separator | `/skill Preserve deployment facts` | `/skill Preserve deployment facts` | — | No split; formal grammar decides |
| Attached and quoted | ``/skill --force foo--bar `--` "--"`` | ``/skill --force foo--bar `--` "--"`` | — | No split; formal grammar decides |
| Exact help | `/skill --help -- Explain this page` | `/skill --help` | `Explain this page` | Context refusal; render nothing |

## DEPENDENCIES

**Binaries**

`pdftotext` from Poppler and `uv` on `PATH`.

**Skills**

The Manager must be Enabled.

## SEE ALSO

**/kntnt select**
