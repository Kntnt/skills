# Configuration

The tool reads all defaults and linguistic terms from TOML files. Program code contains schema, algorithms, and safety invariants only.

## Files and precedence

Bundled settings live in `config/config.toml`; bundled complete locale files live in `config/locales/`. Neither locale is selected by default.

Personal files live below `~/.kntnt/rename-invoices/`:

```text
~/.kntnt/rename-invoices/
├── config.toml
└── locales/
    ├── en.toml
    └── sv.toml
```

Settings resolve as plan flags, then an explicit `--config=FILE` or discovered personal `config.toml`, then bundled `config/config.toml`. Nested tables merge; scalars and arrays replace earlier values. Unknown fields are errors.

Each selected locale resolves as an explicit repeated `--locale-file=FILE`, then a complete personal `locales/NAME.toml`, then the bundled `config/locales/NAME.toml`. Locale files replace one another as complete packages; their contents are never partially merged.

`--no-config` ignores personal settings and personal locale files but still requires one or more `--locale=NAME` flags. Explicit `--locale-file` flags remain available. A supplied locale file must also be selected with `--locale` or the settings file's `locales` array.

## Start a personal configuration

Copy the valid partial example and any locale that needs local changes:

```bash
mkdir -p ~/.kntnt/rename-invoices/locales
cp "$HERE/config/config.example.toml" ~/.kntnt/rename-invoices/config.toml
cp "$HERE/config/locales/sv.toml" ~/.kntnt/rename-invoices/locales/sv.toml
```

The copied personal locale replaces its bundled counterpart. A new file such as `de.toml` contributes a new selectable locale without program changes.

## Locale selection

At least one locale must be selected in settings or flags:

```toml
version = 2
locales = ["en", "sv"]
```

Repeated flags replace the complete configured list for one run:

```text
--locale=en --locale=sv
```

The first selected locale is the primary output locale and supplies localized standard type prefixes. Every selected locale participates in document recognition. Locale order never resolves conflicting dates; incompatible interpretations leave the date unresolved for review.

## Settings schema

`config/config.toml` is the authoritative complete settings example. A personal settings file starts with `version = 2` and may override `output`, `extraction.owner_markers`, `types`, or the complete `profiles` array.

Each type requires ordered `date_sources`, `counterparty_source = "issuer"` or `"recipient"`, and `identifier_policy = "always"`, `"collision"`, or `"never"`. It also needs either a literal `prefix` or a `prefix_key` resolved through the primary locale's `type_prefixes`. Types may override `template`, `date_format`, `description_template`, or `identifier_template`.

The output template may reference `{prefix}`, `{type}`, `{date}`, `{counterparty}`, `{description}`, `{description_part}`, `{identifier}`, `{identifier_part}`, and `{extension}`. It must retain `{date}`, `{counterparty}`, `{extension}`, and an identifier field whenever the type policy can include identifiers.

Profiles recognize recurring document families through complete content markers. They may provide `date_labels`, `identifier_labels`, descriptions, and a known `numeric_date_order = "dmy"`, `"mdy"`, or `"reject-ambiguous"`. Profiles improve extraction but never select the document type.

## Locale schema

`config/locales/en.toml` and `config/locales/sv.toml` are authoritative complete examples. Each locale file starts with `version = 1`, declares its exact lowercase `locale` identifier, and contains:

- `numeric_date_order`: `dmy`, `mdy`, or `reject-ambiguous`.
- `ordinal_suffixes`: suffixes removed only when attached to a day number.
- `identifier_labels`, `issuer_labels`, and `recipient_labels`.
- `legal_suffixes` and `ignored_counterparty_values`.
- `[type_prefixes]` localized output prefixes keyed by standard or local type identifiers.
- `[date_labels]` arrays grouped by semantic date-source keys.
- `[months]` case-insensitive textual month names mapped to integers 1–12.

Year-first numeric dates are always unambiguous. A locale with `reject-ambiguous` still parses textual months and year-first dates. When several selected locales produce different valid dates from the same evidence, the planner reports `needs_review` rather than using locale order.
