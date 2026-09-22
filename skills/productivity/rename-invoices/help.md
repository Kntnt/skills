# rename-invoices

## NAME

rename-invoices - plan and apply safe filenames for accounting PDFs

## SYNOPSIS

**/rename-invoices** [**--folder=**_PATH_] **--type=**_NAME_ [**--config=**_FILE_|**--no-config**] [**--locale=**_NAME_ ...] [**--locale-file=**_FILE_ ...] [**--prefix=**_TEXT_] [**--template=**_TEMPLATE_] [**--date-format=**_FORMAT_] [**--description-template=**_TEMPLATE_] [**--extension=**_EXTENSION_] [**--identifier-template=**_TEMPLATE_] [**--date-source=**_SOURCE_ ...] [**--counterparty-source=**_issuer_|_recipient_] [**--identifier-policy=**_always_|_collision_|_never_] [**--overrides=**_FILE_] [**--yes**|**--dry-run**] [**--** *INSTRUCTION*]

## DESCRIPTION

`rename-invoices` extracts text from PDFs directly inside one folder and builds deterministic filenames from an explicit document type and configured locales. It does not recurse, infer the type, use OCR, or trust existing filenames as evidence.

By default, the Skill applies the reviewed plan after asking `Apply these filename changes? Yes/No.` **--yes** answers yes; **--dry-run** reports the plan without changes.

Every source and destination is rechecked before application. Stale, edited, unresolved, or colliding plans are refused.

Bundled settings cover supplier invoices, receipts, customer invoices, and credit notes. Personal settings under `~/.kntnt/rename-invoices/` can add or override types, locales, and filename conventions.

## OPTIONS

**--folder=**_PATH_

Process direct PDF children of *PATH*. Defaults to `.`; filesystem root and the user's home directory are refused.

**--type=**_NAME_

Select an exact configured document type. It is never inferred or aliased.

**--config=**_FILE_

Use this TOML file instead of discovered personal settings, layered over bundled defaults.

**--no-config**

Ignore discovered personal settings and locales. At least one **--locale** is then required; explicit **--locale-file** remains valid.

**--locale=**_NAME_

Select a locale; repeat for mixed-language folders. The first locale supplies standard filename prefixes. Explicit values replace configured locales.

**--locale-file=**_FILE_

Use a complete locale TOML file; repeat as needed. Its locale must also be selected.

**--prefix=**_TEXT_

Override the selected document type's filename prefix.

**--template=**_TEMPLATE_

Override the filename template while retaining required date, counterparty, extension, and identifier fields.

**--date-format=**_FORMAT_

Override the `strftime` format used for the resolved document date.

**--description-template=**_TEMPLATE_

Override the optional description segment template.

**--extension=**_EXTENSION_

Override the output filename extension.

**--identifier-template=**_TEMPLATE_

Override the optional identifier segment template.

**--date-source=**_SOURCE_

Override date-source priority; repeat in descending order.

**--counterparty-source=**_issuer_|_recipient_

Choose the filename's counterparty.

**--identifier-policy=**_always_|_collision_|_never_

Always include identifiers, include them only for collisions, or omit them.

**--overrides=**_FILE_

Read reviewed unresolved fields from JSON keyed by exact source filename. Direct plan edits remain invalid.

**--yes**

Apply without waiting for confirmation. Incompatible with **--dry-run**.

**--dry-run**

Report the reviewed plan without renaming or confirmation. Incompatible with **--yes**.

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

An invalid, incomplete, conflicting, or out-of-order form is refused rather than repaired or ignored. The Skill names the error, prints the SYNOPSIS, changes nothing, and points to `/rename-invoices --help`. A flag is refused rather than ignored where it has no work to do here.

Configuration, extraction, broad-target, evidence, and collision errors are reported before application. Every `needs_review` item must be resolved.

Changed sources or occupied destinations refuse application. A rename failure triggers best-effort rollback and an authoritative folder-state report.

## EXAMPLES

Preview Swedish supplier-invoice names:

```text
/rename-invoices --type=supplier-invoice --locale=sv --dry-run
```

Apply receipt names in a mixed English and Swedish folder after confirmation:

```text
/rename-invoices --folder=~/Accounting/Receipts --type=receipt --locale=en --locale=sv
```

Apply without confirmation:

```text
/rename-invoices --folder=~/Accounting/Receipts --type=receipt --locale=en --locale=sv --yes
```

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`pdftotext` from Poppler and `uv` on `PATH`.

**Skills**

The Manager must be Enabled.

## SEE ALSO

**/kntnt select**
