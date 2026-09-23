# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Plan and safely apply configurable accounting-document filenames."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import string
import subprocess
import sys
import tomllib
import uuid
from collections import defaultdict
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path
from typing import Any

# Expose the injected text adapter as the only production-dependency seam needed
# by tests.
TextExtractor = Callable[[Path], str]

# Version plans independently from configuration so incompatible decisions fail
# closed.
PLAN_VERSION = 3
CONFIG_VERSION = 2
LOCALE_VERSION = 1
TOOL_NAME = "rename-invoices"

# Resolve bundled data relative to the script and personal data through the
# fixed user seam.
SKILL_ROOT = Path(__file__).resolve().parents[1]
BUNDLED_CONFIG_PATH = SKILL_ROOT / "config" / "config.toml"
BUNDLED_LOCALE_DIRECTORY = SKILL_ROOT / "config" / "locales"

# Limit review overrides to semantic facts established from document contents.
OVERRIDE_FIELDS = {"counterparty", "date", "description", "identifier"}

# Restrict declarative templates to values the planner can verify and sanitize.
TEMPLATE_FIELDS = {
    "counterparty",
    "date",
    "description",
    "description_part",
    "extension",
    "identifier",
    "identifier_part",
    "prefix",
    "type",
}
INVALID_FILENAME_CHARACTERS = re.compile(r"[/\\:*?\"<>|]+")


class PlanError(RuntimeError):
    """Report an invariant that prevents safe planning or application."""


@dataclass(frozen=True)
class OutputDefinition:
    """Define the shared filename rendering defaults."""

    template: str
    date_format: str
    description_template: str
    identifier_template: str
    extension: str


@dataclass(frozen=True)
class LocaleDefinition:
    """Define labels and date semantics for one document language."""

    name: str
    source: Path
    numeric_date_order: str
    date_labels: Mapping[str, tuple[str, ...]]
    identifier_labels: tuple[str, ...]
    issuer_labels: tuple[str, ...]
    recipient_labels: tuple[str, ...]
    months: Mapping[str, int]
    ordinal_suffixes: tuple[str, ...]
    legal_suffixes: tuple[str, ...]
    ignored_counterparty_values: tuple[str, ...]
    type_prefixes: Mapping[str, str]


@dataclass(frozen=True)
class DocumentTypeDefinition:
    """Define semantics and optional output overrides for one explicit type."""

    name: str
    prefix: str | None
    prefix_key: str | None
    date_sources: tuple[str, ...]
    counterparty_source: str
    identifier_policy: str
    template: str | None = None
    date_format: str | None = None
    description_template: str | None = None
    identifier_template: str | None = None


@dataclass(frozen=True)
class DocumentProfile:
    """Define deterministic extraction for one recurring document family."""

    name: str
    markers: tuple[str, ...]
    counterparty: str
    document_types: tuple[str, ...] = ()
    date_labels: tuple[str, ...] = ()
    identifier_labels: tuple[str, ...] = ()
    numeric_date_order: str | None = None
    descriptions: tuple[tuple[str, str], ...] = ()

    def matches(self, text: str, document_type: str) -> bool:
        """Return whether the profile applies to this text and explicit type."""

        # Restrict type-specific profiles before evaluating their content
        # markers.
        if self.document_types and document_type not in self.document_types:
            return False

        # Require every marker case-insensitively to avoid weak single-token
        # matches.
        normalized = text.casefold()

        return all(marker.casefold() in normalized for marker in self.markers)

    def description(self, text: str) -> str | None:
        """Return the first configured recognition description present in the text."""

        # Preserve configuration order from most specific marker to least
        # specific marker.
        normalized = text.casefold()
        for marker, value in self.descriptions:
            if marker.casefold() in normalized:
                return value

        return None


@dataclass(frozen=True)
class Configuration:
    """Hold one validated merged configuration and its provenance."""

    bundled_source: Path
    source: Path | None
    digest: str
    locale_names: tuple[str, ...]
    output: OutputDefinition
    locales: Mapping[str, LocaleDefinition]
    document_types: Mapping[str, DocumentTypeDefinition]
    profiles: tuple[DocumentProfile, ...]
    owner_markers: tuple[str, ...]
    legal_suffixes: tuple[str, ...]
    ignored_counterparty_values: tuple[str, ...]


@dataclass(frozen=True)
class EffectiveSettings:
    """Hold one document type after configuration and CLI precedence is resolved."""

    configuration: Configuration
    locales: tuple[LocaleDefinition, ...]
    document_type: DocumentTypeDefinition
    output: OutputDefinition


def reject_unknown_keys(
    values: Mapping[str, Any], allowed: set[str], context: str
) -> None:
    """Reject misspelled configuration fields with their exact location."""

    # Fail closed so an apparent override cannot silently fall back to a
    # default.
    unknown = set(values) - allowed
    if unknown:
        raise PlanError(f"Unknown configuration fields in {context}: {sorted(unknown)}")


def require_mapping(value: Any, context: str) -> Mapping[str, Any]:
    """Return one mapping or raise a contextual configuration error."""

    # Keep schema diagnostics at the declarative configuration seam.
    if not isinstance(value, Mapping):
        raise PlanError(f"Configuration field {context} must be a table")

    return value


def require_string(value: Any, context: str) -> str:
    """Return one non-empty string or raise a contextual error."""

    # Reject blank values because they create filenames that appear configured
    # but are not.
    if not isinstance(value, str) or not value.strip():
        raise PlanError(f"Configuration field {context} must be a non-empty string")

    return value


def require_optional_string(value: Any, context: str) -> str | None:
    """Return one optional non-empty string."""

    # Preserve omitted type-level output overrides while validating supplied
    # values.
    if value is None:
        return None

    return require_string(value, context)


def require_string_sequence(
    value: Any, context: str, *, allow_empty: bool = True
) -> tuple[str, ...]:
    """Return a tuple of non-empty strings from one configuration array."""

    # Exclude scalar strings and mappings even though both are iterable.
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise PlanError(f"Configuration field {context} must be an array of strings")
    values = tuple(require_string(item, f"{context}[]") for item in value)
    if not allow_empty and not values:
        raise PlanError(f"Configuration field {context} must not be empty")

    return values


def deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """Merge nested configuration tables while replacing scalar and array values."""

    # Copy the built-ins so no resolution can mutate defaults shared by later
    # calls.
    merged: dict[str, Any] = copy.deepcopy(dict(base))
    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)

    return merged


def user_config_directory() -> Path:
    """Return the fixed personal configuration directory."""

    # Keep every personal setting and locale below one predictable user-owned
    # path.
    return Path.home() / ".kntnt" / TOOL_NAME


def default_config_path() -> Path:
    """Return the discovered personal configuration file."""

    # Keep discovery independent of platform-specific configuration conventions.
    return user_config_directory() / "config.toml"


def personal_locale_path(name: str) -> Path:
    """Return the discovered personal file for one locale name."""

    # Locale names are already validated as simple identifiers before path
    # construction.
    return user_config_directory() / "locales" / f"{name}.toml"


def select_config_path(explicit: Path | None, use_user_config: bool) -> Path | None:
    """Select an explicit or discovered user configuration without reading it."""

    # Treat an explicit path as authoritative and report a typo instead of
    # falling back.
    if explicit is not None:
        selected = explicit.expanduser().resolve()
        if not selected.is_file():
            raise PlanError(f"Configuration file does not exist: {selected}")

        return selected

    # Skip discovery only when the caller explicitly requested built-in
    # defaults.
    if not use_user_config:
        return None
    discovered = default_config_path()

    return discovered.resolve() if discovered.is_file() else None


def load_toml(path: Path) -> Mapping[str, Any]:
    """Load one TOML configuration with a concise parse error."""

    # Keep filesystem and syntax failures inside the CLI's shared error
    # contract.
    try:
        with path.open("rb") as stream:
            value = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise PlanError(f"Could not read configuration {path}: {error}") from error
    if not isinstance(value, Mapping):
        raise PlanError(f"Configuration root must be a table: {path}")

    return value


def parse_output(values: Mapping[str, Any]) -> OutputDefinition:
    """Validate shared output configuration."""

    # Restrict output fields to the supported rendering interface.
    allowed = {
        "template",
        "date_format",
        "description_template",
        "identifier_template",
        "extension",
    }
    reject_unknown_keys(values, allowed, "output")

    return OutputDefinition(
        template=require_string(values.get("template"), "output.template"),
        date_format=require_string(values.get("date_format"), "output.date_format"),
        description_template=require_string(
            values.get("description_template"), "output.description_template"
        ),
        identifier_template=require_string(
            values.get("identifier_template"), "output.identifier_template"
        ),
        extension=require_string(values.get("extension"), "output.extension").lstrip(
            "."
        ),
    )


def validate_locale_name(name: str, context: str) -> str:
    """Require one locale identifier that is safe for file discovery."""

    # Restrict names to portable language or language-region identifiers.
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise PlanError(
            f"{context} must contain lowercase letters, digits, and hyphens only: {name!r}"
        )

    return name


def parse_locale(values: Mapping[str, Any], source: Path) -> LocaleDefinition:
    """Validate one complete standalone locale file."""

    # Keep every linguistic extraction term in the locale file rather than
    # program code.
    allowed = {
        "version",
        "locale",
        "numeric_date_order",
        "date_labels",
        "identifier_labels",
        "issuer_labels",
        "recipient_labels",
        "months",
        "ordinal_suffixes",
        "legal_suffixes",
        "ignored_counterparty_values",
        "type_prefixes",
    }
    reject_unknown_keys(values, allowed, str(source))
    if values.get("version") != LOCALE_VERSION:
        raise PlanError(
            f"Unsupported locale version in {source}: {values.get('version')!r}"
        )
    name = validate_locale_name(
        require_string(values.get("locale"), f"{source}.locale"), f"{source}.locale"
    )
    numeric_date_order = require_string(
        values.get("numeric_date_order"), f"{source}.numeric_date_order"
    )
    if numeric_date_order not in {"dmy", "mdy", "reject-ambiguous"}:
        raise PlanError(
            f"Locale {name!r} numeric_date_order must be dmy, mdy, or reject-ambiguous"
        )

    # Validate each semantic date-source group independently.
    raw_date_labels = require_mapping(
        values.get("date_labels"), f"{source}.date_labels"
    )
    date_labels = {
        require_string(
            date_source, f"{source}.date_labels key"
        ): require_string_sequence(
            labels,
            f"{source}.date_labels.{date_source}",
            allow_empty=False,
        )
        for date_source, labels in raw_date_labels.items()
    }

    # Normalize textual month keys and require real calendar month numbers.
    raw_months = require_mapping(values.get("months"), f"{source}.months")
    months: dict[str, int] = {}
    for month_name, month_number in raw_months.items():
        if (
            not isinstance(month_name, str)
            or not isinstance(month_number, int)
            or not 1 <= month_number <= 12
        ):
            raise PlanError(f"Locale {name!r} months must map strings to integers 1-12")
        months[month_name.casefold()] = month_number

    # Resolve localized standard prefixes by stable document-type keys.
    raw_prefixes = require_mapping(
        values.get("type_prefixes"), f"{source}.type_prefixes"
    )
    type_prefixes = {
        require_string(key, f"{source}.type_prefixes key"): require_string(
            value, f"{source}.type_prefixes.{key}"
        )
        for key, value in raw_prefixes.items()
    }

    return LocaleDefinition(
        name=name,
        source=source,
        numeric_date_order=numeric_date_order,
        date_labels=date_labels,
        identifier_labels=require_string_sequence(
            values.get("identifier_labels"), f"{source}.identifier_labels"
        ),
        issuer_labels=require_string_sequence(
            values.get("issuer_labels"), f"{source}.issuer_labels"
        ),
        recipient_labels=require_string_sequence(
            values.get("recipient_labels"), f"{source}.recipient_labels"
        ),
        months=months,
        ordinal_suffixes=require_string_sequence(
            values.get("ordinal_suffixes", []), f"{source}.ordinal_suffixes"
        ),
        legal_suffixes=require_string_sequence(
            values.get("legal_suffixes", []), f"{source}.legal_suffixes"
        ),
        ignored_counterparty_values=require_string_sequence(
            values.get("ignored_counterparty_values", []),
            f"{source}.ignored_counterparty_values",
        ),
        type_prefixes=type_prefixes,
    )


def parse_document_type(name: str, values: Mapping[str, Any]) -> DocumentTypeDefinition:
    """Validate one explicit document type definition."""

    # Keep type behavior compact while allowing narrow output overrides.
    allowed = {
        "prefix",
        "prefix_key",
        "date_sources",
        "counterparty_source",
        "identifier_policy",
        "template",
        "date_format",
        "description_template",
        "identifier_template",
    }
    reject_unknown_keys(values, allowed, f"types.{name}")
    counterparty_source = require_string(
        values.get("counterparty_source"), f"types.{name}.counterparty_source"
    )
    if counterparty_source not in {"issuer", "recipient"}:
        raise PlanError(
            f"Configuration field types.{name}.counterparty_source must be issuer or recipient"
        )
    identifier_policy = require_string(
        values.get("identifier_policy"), f"types.{name}.identifier_policy"
    )
    if identifier_policy not in {"always", "collision", "never"}:
        raise PlanError(
            f"Configuration field types.{name}.identifier_policy must be always, collision, or never"
        )
    prefix = require_optional_string(values.get("prefix"), f"types.{name}.prefix")
    prefix_key = require_optional_string(
        values.get("prefix_key"), f"types.{name}.prefix_key"
    )
    if prefix is None and prefix_key is None:
        raise PlanError(f"Configuration type {name!r} must define prefix or prefix_key")

    return DocumentTypeDefinition(
        name=name,
        prefix=prefix,
        prefix_key=prefix_key,
        date_sources=require_string_sequence(
            values.get("date_sources"),
            f"types.{name}.date_sources",
            allow_empty=False,
        ),
        counterparty_source=counterparty_source,
        identifier_policy=identifier_policy,
        template=require_optional_string(
            values.get("template"), f"types.{name}.template"
        ),
        date_format=require_optional_string(
            values.get("date_format"), f"types.{name}.date_format"
        ),
        description_template=require_optional_string(
            values.get("description_template"),
            f"types.{name}.description_template",
        ),
        identifier_template=require_optional_string(
            values.get("identifier_template"),
            f"types.{name}.identifier_template",
        ),
    )


def parse_profile(values: Mapping[str, Any], index: int) -> DocumentProfile:
    """Validate one recurring-document extraction profile."""

    # Keep profile fields semantic and independent of output formatting.
    context = f"profiles[{index}]"
    allowed = {
        "name",
        "markers",
        "counterparty",
        "types",
        "date_labels",
        "identifier_labels",
        "numeric_date_order",
        "descriptions",
    }
    reject_unknown_keys(values, allowed, context)
    numeric_date_order = require_optional_string(
        values.get("numeric_date_order"), f"{context}.numeric_date_order"
    )
    if numeric_date_order is not None and numeric_date_order not in {
        "dmy",
        "mdy",
        "reject-ambiguous",
    }:
        raise PlanError(
            f"Configuration field {context}.numeric_date_order must be dmy, mdy, or reject-ambiguous"
        )

    # Preserve description marker order from the TOML table.
    raw_descriptions = require_mapping(
        values.get("descriptions", {}), f"{context}.descriptions"
    )
    descriptions = tuple(
        (
            require_string(marker, f"{context}.descriptions key"),
            require_string(value, f"{context}.descriptions.{marker}"),
        )
        for marker, value in raw_descriptions.items()
    )

    return DocumentProfile(
        name=require_string(values.get("name"), f"{context}.name"),
        markers=require_string_sequence(
            values.get("markers"), f"{context}.markers", allow_empty=False
        ),
        counterparty=require_string(
            values.get("counterparty"), f"{context}.counterparty"
        ),
        document_types=require_string_sequence(
            values.get("types", []), f"{context}.types"
        ),
        date_labels=require_string_sequence(
            values.get("date_labels", []), f"{context}.date_labels"
        ),
        identifier_labels=require_string_sequence(
            values.get("identifier_labels", []),
            f"{context}.identifier_labels",
        ),
        numeric_date_order=numeric_date_order,
        descriptions=descriptions,
    )


def parse_configuration(
    values: Mapping[str, Any],
    *,
    bundled_source: Path,
    source: Path | None,
    locales: Mapping[str, LocaleDefinition],
    locale_values: Mapping[str, Mapping[str, Any]],
) -> Configuration:
    """Convert merged settings and complete locale files into one validated module."""

    # Keep linguistic data outside the settings schema and require an explicit
    # locale list.
    allowed = {"version", "locales", "output", "extraction", "types", "profiles"}
    reject_unknown_keys(values, allowed, "root")
    if values.get("version") != CONFIG_VERSION:
        raise PlanError(f"Unsupported configuration version: {values.get('version')!r}")
    locale_names = require_string_sequence(
        values.get("locales", []), "locales", allow_empty=False
    )
    if len(set(locale_names)) != len(locale_names):
        raise PlanError("Configuration field locales must not contain duplicates")
    if set(locale_names) != set(locales):
        raise PlanError("Loaded locale files do not match the configured locale list")

    # Parse settings that apply across every selected locale.
    extraction = require_mapping(values.get("extraction"), "extraction")
    reject_unknown_keys(extraction, {"owner_markers"}, "extraction")
    owner_markers = require_string_sequence(
        extraction.get("owner_markers", []), "extraction.owner_markers"
    )
    raw_types = require_mapping(values.get("types"), "types")
    document_types = {
        name: parse_document_type(name, require_mapping(value, f"types.{name}"))
        for name, value in raw_types.items()
    }

    # Validate recurring-document profiles and their exact type references.
    raw_profiles = values.get("profiles", [])
    if not isinstance(raw_profiles, list):
        raise PlanError("Configuration field profiles must be an array of tables")
    profiles = tuple(
        parse_profile(require_mapping(value, f"profiles[{index}]"), index)
        for index, value in enumerate(raw_profiles)
    )
    for profile in profiles:
        unknown_types = set(profile.document_types) - set(document_types)
        if unknown_types:
            raise PlanError(
                f"Profile {profile.name!r} references unknown types: {sorted(unknown_types)}"
            )

    # Hash every effective settings and locale value so the plan binds all
    # language decisions.
    digest_material = {"configuration": values, "locales": locale_values}
    encoded = json.dumps(
        digest_material, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    legal_suffixes = unique(
        tuple(
            suffix for name in locale_names for suffix in locales[name].legal_suffixes
        )
    )
    ignored_values = unique(
        tuple(
            value
            for name in locale_names
            for value in locales[name].ignored_counterparty_values
        ),
    )

    return Configuration(
        bundled_source=bundled_source,
        source=source,
        digest=hashlib.sha256(encoded).hexdigest(),
        locale_names=locale_names,
        output=parse_output(require_mapping(values.get("output"), "output")),
        locales=locales,
        document_types=document_types,
        profiles=profiles,
        owner_markers=owner_markers,
        legal_suffixes=legal_suffixes,
        ignored_counterparty_values=ignored_values,
    )


def load_explicit_locale_files(
    paths: Sequence[Path],
) -> tuple[dict[str, Path], dict[str, Mapping[str, Any]]]:
    """Load explicitly supplied complete locale files by their declared names."""

    # Let file contents establish locale identity while rejecting duplicate
    # overrides.
    sources: dict[str, Path] = {}
    values_by_name: dict[str, Mapping[str, Any]] = {}
    for raw_path in paths:
        path = raw_path.expanduser().resolve()
        if not path.is_file():
            raise PlanError(f"Locale file does not exist: {path}")
        values = load_toml(path)
        name = validate_locale_name(
            require_string(values.get("locale"), f"{path}.locale"), f"{path}.locale"
        )
        if name in sources:
            raise PlanError(f"More than one explicit locale file declares {name!r}")
        sources[name] = path
        values_by_name[name] = values

    return sources, values_by_name


def select_locale_source(
    name: str, explicit: Mapping[str, Path], use_user_config: bool
) -> Path:
    """Select one complete locale file through explicit, personal, and bundled precedence."""

    # Apply explicit file flags before personal replacement files and bundled
    # packages.
    if name in explicit:
        return explicit[name]
    personal = personal_locale_path(name)
    if use_user_config and personal.is_file():
        return personal.resolve()
    bundled = BUNDLED_LOCALE_DIRECTORY / f"{name}.toml"
    if bundled.is_file():
        return bundled.resolve()

    raise PlanError(
        f"No locale file found for {name!r}; add {personal_locale_path(name)} or pass --locale-file=FILE",
    )


def load_configuration(
    config_path: Path | None = None,
    *,
    use_user_config: bool = True,
    locale_names: Sequence[str] | None = None,
    locale_files: Sequence[Path] = (),
) -> Configuration:
    """Load bundled settings, one user overlay, and every explicitly selected locale."""

    # Require the bundled defaults as an ordinary validated file rather than
    # program constants.
    bundled_source = BUNDLED_CONFIG_PATH.resolve()
    if not bundled_source.is_file():
        raise PlanError(f"Bundled configuration file is missing: {bundled_source}")
    bundled_values = load_toml(bundled_source)
    selected = select_config_path(config_path, use_user_config)
    user_values: Mapping[str, Any] = load_toml(selected) if selected is not None else {}
    merged = deep_merge(bundled_values, user_values)
    if locale_names is not None:
        merged["locales"] = list(locale_names)

    # Require locale selection from flags or configuration and validate each
    # portable name.
    selected_names = require_string_sequence(
        merged.get("locales", []), "locales", allow_empty=False
    )
    selected_names = tuple(
        validate_locale_name(name, "locales") for name in selected_names
    )
    merged["locales"] = list(selected_names)
    explicit_sources, explicit_values = load_explicit_locale_files(locale_files)
    unused_explicit = set(explicit_sources) - set(selected_names)
    if unused_explicit:
        raise PlanError(
            f"Explicit locale files were not selected with --locale: {sorted(unused_explicit)}"
        )

    # Load each locale as a complete replacement and preserve its provenance.
    locales: dict[str, LocaleDefinition] = {}
    locale_values: dict[str, Mapping[str, Any]] = {}
    for name in selected_names:
        locale_source = select_locale_source(name, explicit_sources, use_user_config)
        values = explicit_values.get(name) or load_toml(locale_source)
        locale = parse_locale(values, locale_source)
        if locale.name != name:
            raise PlanError(
                f"Locale file {locale_source} declares {locale.name!r}, expected {name!r}"
            )
        locales[name] = locale
        locale_values[name] = values

    return parse_configuration(
        merged,
        bundled_source=bundled_source,
        source=selected,
        locales=locales,
        locale_values=locale_values,
    )


def template_fields(template: str, context: str) -> set[str]:
    """Validate one format template and return its referenced field names."""

    # Parse through the standard formatter so malformed braces produce a concise
    # configuration error.
    try:
        parts = tuple(string.Formatter().parse(template))
    except ValueError as error:
        raise PlanError(f"Invalid template in {context}: {error}") from error

    # Keep literal syntax cross-platform and fields limited to the stable
    # rendering interface.
    fields: set[str] = set()
    for literal, field, _, _ in parts:
        if INVALID_FILENAME_CHARACTERS.search(literal):
            raise PlanError(
                f"Template {context} contains a path or cross-platform filename separator"
            )
        if field is None:
            continue
        if field not in TEMPLATE_FIELDS:
            raise PlanError(f"Unknown template field {field!r} in {context}")
        fields.add(field)

    return fields


def validate_effective_settings(settings: EffectiveSettings) -> None:
    """Validate the fully resolved type, locale, and output combination."""

    # Require complete semantic source groups in every selected locale.
    for locale in settings.locales:
        missing_sources = set(settings.document_type.date_sources) - set(
            locale.date_labels
        )
        if missing_sources:
            raise PlanError(
                f"Type {settings.document_type.name!r} uses date sources missing from locale "
                f"{locale.name!r}: {sorted(missing_sources)}",
            )

    # Require the main template to retain the core accounting-document fields.
    fields = template_fields(settings.output.template, "output.template")
    required = {"counterparty", "date", "extension"}
    if missing := required - fields:
        raise PlanError(
            f"Output template is missing required fields: {sorted(missing)}"
        )
    if settings.document_type.identifier_policy != "never" and not fields & {
        "identifier",
        "identifier_part",
    }:
        raise PlanError(
            "Output template must include identifier or identifier_part for this identifier policy"
        )

    # Restrict conditional segment templates to their single semantic values.
    description_fields = template_fields(
        settings.output.description_template, "output.description_template"
    )
    if description_fields - {"description"}:
        raise PlanError("Description template may only reference description")
    identifier_fields = template_fields(
        settings.output.identifier_template, "output.identifier_template"
    )
    if identifier_fields - {"identifier"}:
        raise PlanError("Identifier template may only reference identifier")

    # Validate the date format and extension before touching any user documents.
    sample_date = date(2001, 2, 3).strftime(settings.output.date_format)
    if not sample_date or INVALID_FILENAME_CHARACTERS.search(sample_date):
        raise PlanError(
            "Date format must produce a non-empty cross-platform filename segment"
        )
    if not settings.output.extension or INVALID_FILENAME_CHARACTERS.search(
        settings.output.extension
    ):
        raise PlanError("Output extension must be a cross-platform filename segment")


def resolve_settings(
    configuration: Configuration,
    document_type: str,
    cli_overrides: Mapping[str, Any] | None = None,
) -> EffectiveSettings:
    """Resolve one explicit type after applying CLI overrides last."""

    # Require the flag-selected type without aliases or conversation-derived
    # inference.
    if document_type not in configuration.document_types:
        raise PlanError(
            f"Unknown document type {document_type!r}; choose one of: {sorted(configuration.document_types)}"
        )
    selected_type = configuration.document_types[document_type]
    overrides = {
        key: value for key, value in (cli_overrides or {}).items() if value is not None
    }
    reject_unknown_keys(
        overrides,
        {
            "locales",
            "prefix",
            "date_sources",
            "counterparty_source",
            "identifier_policy",
            "template",
            "date_format",
            "description_template",
            "extension",
            "identifier_template",
        },
        "CLI overrides",
    )

    # Apply semantic type flags after user configuration.
    type_changes: dict[str, Any] = {}
    for field in ("prefix", "counterparty_source", "identifier_policy"):
        if field in overrides:
            type_changes[field] = require_string(
                overrides[field], f"--{field.replace('_', '-')}"
            )
    if "date_sources" in overrides:
        type_changes["date_sources"] = require_string_sequence(
            overrides["date_sources"],
            "--date-source",
            allow_empty=False,
        )
    selected_type = replace(selected_type, **type_changes)
    if selected_type.counterparty_source not in {"issuer", "recipient"}:
        raise PlanError("--counterparty-source must be issuer or recipient")
    if selected_type.identifier_policy not in {"always", "collision", "never"}:
        raise PlanError("--identifier-policy must be always, collision, or never")

    # Resolve a localized standard prefix from the first selected output locale.
    selected_locales = tuple(
        configuration.locales[name] for name in configuration.locale_names
    )
    if selected_type.prefix is None:
        prefix_key = require_string(
            selected_type.prefix_key, f"types.{selected_type.name}.prefix_key"
        )
        prefix = selected_locales[0].type_prefixes.get(prefix_key)
        if prefix is None:
            raise PlanError(
                f"Primary locale {selected_locales[0].name!r} has no type_prefixes entry for {prefix_key!r}",
            )
        selected_type = replace(selected_type, prefix=prefix)

    # Apply type-level and CLI output overrides over the shared output defaults.
    output_changes = {
        field: value
        for field in (
            "template",
            "date_format",
            "description_template",
            "identifier_template",
        )
        if (value := getattr(selected_type, field)) is not None
    }
    for field in (
        "template",
        "date_format",
        "description_template",
        "identifier_template",
        "extension",
    ):
        if field in overrides:
            value = require_string(overrides[field], f"--{field.replace('_', '-')}")
            output_changes[field] = value.lstrip(".") if field == "extension" else value
    output = replace(configuration.output, **output_changes)
    settings = EffectiveSettings(
        configuration=configuration,
        locales=selected_locales,
        document_type=selected_type,
        output=output,
    )
    validate_effective_settings(settings)

    return settings


def validate_folder(folder: Path) -> Path:
    """Resolve one deliberately narrow document folder."""

    # Refuse broad roots because every PDF directly inside the folder enters the
    # plan.
    resolved = folder.expanduser().resolve()
    if not resolved.is_dir():
        raise PlanError(f"Document folder does not exist: {resolved}")
    if resolved in {Path(resolved.anchor), Path.home().resolve()}:
        raise PlanError(f"Refusing broad document folder: {resolved}")

    return resolved


def poppler_installation_hint() -> str:
    """Return a concise platform-aware Poppler installation hint."""

    # Prefer the package manager already present on the host.
    if sys.platform == "darwin":
        return "Install Poppler with `brew install poppler`, then run `pdftotext -v`."
    if sys.platform.startswith("linux"):
        candidates = (
            ("apt", "sudo apt install poppler-utils"),
            ("apt-get", "sudo apt-get install poppler-utils"),
            ("dnf", "sudo dnf install poppler-utils"),
            ("yum", "sudo yum install poppler-utils"),
            ("pacman", "sudo pacman -S poppler"),
            ("zypper", "sudo zypper install poppler-tools"),
            ("apk", "sudo apk add poppler-utils"),
        )
        for executable, command in candidates:
            if shutil.which(executable):
                return f"Install Poppler with `{command}`, then run `pdftotext -v`."

    return (
        "Install Poppler so `pdftotext` is available on PATH, then run `pdftotext -v`."
    )


def check_poppler() -> dict[str, str]:
    """Require the single external PDF extraction dependency."""

    # Check executable discovery only; document extraction provides the
    # functional error boundary.
    executable = shutil.which("pdftotext")
    if executable is None:
        raise PlanError(
            f"Poppler pdftotext was not found on PATH. {poppler_installation_hint()}"
        )

    return {
        "status": "ok",
        "tool": "Poppler pdftotext",
        "executable": executable,
    }


def check_environment(
    config_path: Path | None = None,
    *,
    use_user_config: bool = True,
    locale_names: Sequence[str] | None = None,
    locale_files: Sequence[Path] = (),
) -> dict[str, Any]:
    """Validate dependencies and configuration without opening a document folder."""

    # Gate on the required executable before configuration or document work
    # consumes attention.
    poppler = check_poppler()
    configuration = load_configuration(
        config_path,
        use_user_config=use_user_config,
        locale_names=locale_names,
        locale_files=locale_files,
    )
    for document_type in configuration.document_types:
        resolve_settings(configuration, document_type)

    return {
        "status": "ok",
        "dependency": poppler,
        "configuration": {
            "bundled_source": str(configuration.bundled_source),
            "user_source": str(configuration.source) if configuration.source else None,
            "digest": configuration.digest,
            "locales": list(configuration.locale_names),
            "locale_sources": {
                name: str(configuration.locales[name].source)
                for name in configuration.locale_names
            },
            "types": sorted(configuration.document_types),
        },
    }


def extract_pdf_text(path: Path) -> str:
    """Extract layout-preserving text through Poppler pdftotext."""

    # Keep Poppler as the sole production extractor and capture output without
    # temporary artifacts. It inherits the caller's working directory on
    # purpose: the document folder is resolved absolute before any file reaches
    # here and the text comes back on standard output, so nothing this call
    # touches is named relative to a directory — and the one it starts in is
    # the user's own, which no run of this Skill replaces.
    process = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True,
        check=False,
        text=True,
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or f"exit status {process.returncode}"
        raise PlanError(f"Could not extract text from {path.name}: {detail}")
    if not process.stdout.strip():
        raise PlanError(
            f"No text was extracted from {path.name}; this tool does not perform OCR. "
            "Provide a text-based PDF before retrying.",
        )

    return process.stdout


def file_digest(path: Path) -> str:
    """Hash one source file for apply-time integrity verification."""

    # Stream large documents so integrity checking has bounded memory use.
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def unique(values: Sequence[str]) -> tuple[str, ...]:
    """Return non-empty values once while preserving their evidence order."""

    # Preserve the first label match because configuration order expresses
    # priority.
    return tuple(dict.fromkeys(value.strip() for value in values if value.strip()))


def labeled_candidates(text: str, labels: Sequence[str]) -> tuple[str, ...]:
    """Return values found beside or immediately below configured labels."""

    # Search line-by-line to prevent one missing value from consuming an
    # unrelated block.
    lines = text.splitlines()
    candidates: list[str] = []
    for index, line in enumerate(lines):
        normalized = line.strip()
        for label in labels:
            match = re.search(
                rf"(?:^|\s{{2,}}){re.escape(label)}\s*(?::|#|-)?\s*(.*)$",
                normalized,
                flags=re.IGNORECASE,
            )
            if match is None:
                continue
            inline = match.group(1).strip()
            if inline:
                candidates.append(inline)
                break
            for following in lines[index + 1 : index + 4]:
                candidate = following.strip()
                if candidate and not re.fullmatch(r"[._-]+", candidate):
                    candidates.append(candidate)
                    break
            break

    return unique(candidates)


def parse_date_value(
    raw: str,
    *,
    numeric_date_order: str,
    months: Mapping[str, int],
    ordinal_suffixes: Sequence[str] = (),
) -> date | None:
    """Parse one configured-language date without guessing ambiguous numeric order."""

    # Remove only configured ordinal suffixes while preserving date separators.
    value = raw.strip()
    if ordinal_suffixes:
        suffixes = "|".join(
            sorted(
                (re.escape(suffix) for suffix in ordinal_suffixes),
                key=len,
                reverse=True,
            )
        )
        value = re.sub(rf"(?<=\d)(?:{suffixes})\b", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value).strip(" ,.;")

    # Prefer unambiguous year-first dates regardless of locale.
    match = re.search(r"\b(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\b", value)
    if match:
        try:
            return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            return None

    # Support both day-month-name and month-name-day using the selected locale's
    # month table.
    month_names = "|".join(
        sorted((re.escape(name) for name in months), key=len, reverse=True)
    )
    if month_names:
        day_month = re.search(
            rf"\b(\d{{1,2}})\s+({month_names})\.?[,]?\s+(\d{{4}})\b",
            value,
            flags=re.IGNORECASE,
        )
        month_day = re.search(
            rf"\b({month_names})\.?\s+(\d{{1,2}})[,]?\s+(\d{{4}})\b",
            value,
            flags=re.IGNORECASE,
        )
        if day_month:
            parts = (
                int(day_month.group(3)),
                months[day_month.group(2).casefold()],
                int(day_month.group(1)),
            )
        elif month_day:
            parts = (
                int(month_day.group(3)),
                months[month_day.group(1).casefold()],
                int(month_day.group(2)),
            )
        else:
            parts = None
        if parts is not None:
            try:
                return date(*parts)
            except ValueError:
                return None

    # Parse numeric dates only when the originating locale defines their order.
    numeric = re.search(r"\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})\b", value)
    if numeric and numeric_date_order != "reject-ambiguous":
        first, second, year = map(int, numeric.groups())
        month, day = (second, first) if numeric_date_order == "dmy" else (first, second)
        try:
            return date(year, month, day)
        except ValueError:
            return None

    return None


def find_profile(text: str, settings: EffectiveSettings) -> DocumentProfile | None:
    """Find the first deterministic profile matching the explicit document type."""

    # Configuration order resolves intentionally overlapping recurring-document
    # profiles.
    for profile in settings.configuration.profiles:
        if profile.matches(text, settings.document_type.name):
            return profile

    return None


def find_document_date(
    text: str,
    settings: EffectiveSettings,
    profile: DocumentProfile | None,
) -> date | None:
    """Find one unambiguous date while preserving locale provenance."""

    # Let a recurring profile supply precise labels and optional vendor-specific
    # numeric order.
    if profile and profile.date_labels:
        profile_dates: set[date] = set()
        for candidate in labeled_candidates(text, profile.date_labels):
            for locale in settings.locales:
                numeric_order = profile.numeric_date_order or locale.numeric_date_order
                parsed = parse_date_value(
                    candidate,
                    numeric_date_order=numeric_order,
                    months=locale.months,
                    ordinal_suffixes=locale.ordinal_suffixes,
                )
                if parsed:
                    profile_dates.add(parsed)
        if len(profile_dates) == 1:
            return next(iter(profile_dates))
        if len(profile_dates) > 1:
            return None

    # Evaluate each semantic source in priority order without using locale order
    # to break conflicts.
    for date_source in settings.document_type.date_sources:
        source_dates: set[date] = set()
        for locale in settings.locales:
            for candidate in labeled_candidates(text, locale.date_labels[date_source]):
                parsed = parse_date_value(
                    candidate,
                    numeric_date_order=locale.numeric_date_order,
                    months=locale.months,
                    ordinal_suffixes=locale.ordinal_suffixes,
                )
                if parsed:
                    source_dates.add(parsed)
        if len(source_dates) == 1:
            return next(iter(source_dates))
        if len(source_dates) > 1:
            return None

    return None


def find_identifier(
    text: str,
    settings: EffectiveSettings,
    profile: DocumentProfile | None,
) -> str | None:
    """Find an explicit accounting-document identifier."""

    # Prefer profile labels, then selected locale labels in their explicit
    # order.
    locale_labels = tuple(
        label for locale in settings.locales for label in locale.identifier_labels
    )
    labels = (*profile.identifier_labels, *locale_labels) if profile else locale_labels
    for candidate in labeled_candidates(text, labels):
        value = candidate.split()[0].strip(" ,.;")
        if value and len(value) <= 120:
            return value

    return None


def clean_counterparty(
    value: str,
    legal_suffixes: Sequence[str],
    ignored_values: Sequence[str],
) -> str | None:
    """Normalize one evidenced legal name to a safe common counterparty name."""

    # Reject PDF column boundaries before whitespace normalization erases the
    # evidence that the candidate combines unrelated fields.
    if re.search(r"(?:\t|\s{2,})", value.strip()):
        return None

    # Keep the source spelling while removing only configured terminal legal
    # suffixes.
    candidate = re.sub(r"\s+", " ", value).strip(" ,.;:-")
    for suffix in sorted(legal_suffixes, key=len, reverse=True):
        candidate = re.sub(
            rf"(?:,?\s+){re.escape(suffix)}\.?$", "", candidate, flags=re.IGNORECASE
        ).strip()
    if not candidate or len(candidate) > 160:
        return None
    if candidate.casefold() in {value.casefold() for value in ignored_values}:
        return None

    return candidate


def matches_owner_identity(
    candidate: str,
    owner_markers: Sequence[str],
    legal_suffixes: Sequence[str],
    ignored_values: Sequence[str],
) -> bool:
    """Return whether a candidate contains one configured owner identity."""

    # Compare contiguous Unicode word sequences so PDF layout prefixes and
    # punctuation cannot disguise the document owner's name.
    candidate_words = tuple(
        "".join(
            character if character.isalnum() else " "
            for character in candidate.casefold()
        ).split()
    )
    for marker in owner_markers:
        cleaned_marker = clean_counterparty(marker, legal_suffixes, ignored_values)
        marker_words = tuple(
            "".join(
                character if character.isalnum() else " "
                for character in (cleaned_marker or marker).casefold()
            ).split()
        )
        if marker_words and any(
            candidate_words[index : index + len(marker_words)] == marker_words
            for index in range(len(candidate_words) - len(marker_words) + 1)
        ):
            return True

    return False


def find_counterparty(
    text: str,
    settings: EffectiveSettings,
    profile: DocumentProfile | None,
) -> str | None:
    """Find the configured issuer or recipient without using the source filename."""

    # A matching profile is the strongest deterministic counterparty evidence.
    if profile:
        return profile.counterparty

    # Prefer an explicitly labeled party block for the selected document-type
    # semantics.
    labels = tuple(
        label
        for locale in settings.locales
        for label in (
            locale.issuer_labels
            if settings.document_type.counterparty_source == "issuer"
            else locale.recipient_labels
        )
    )
    for candidate in labeled_candidates(text, labels):
        cleaned = clean_counterparty(
            candidate,
            settings.configuration.legal_suffixes,
            settings.configuration.ignored_counterparty_values,
        )
        if cleaned and not matches_owner_identity(
            cleaned,
            settings.configuration.owner_markers,
            settings.configuration.legal_suffixes,
            settings.configuration.ignored_counterparty_values,
        ):
            return cleaned

    # Fall back only to a complete legal-entity line, excluding configured owner
    # identities.
    suffix_pattern = "|".join(
        sorted(
            (re.escape(suffix) for suffix in settings.configuration.legal_suffixes),
            key=len,
            reverse=True,
        ),
    )
    if suffix_pattern:
        for line in text.splitlines():
            candidate = line.strip()
            if not re.search(
                rf"(?:^|\s)(?:{suffix_pattern})\.?$", candidate, flags=re.IGNORECASE
            ):
                continue
            cleaned = clean_counterparty(
                candidate,
                settings.configuration.legal_suffixes,
                settings.configuration.ignored_counterparty_values,
            )
            if cleaned and not matches_owner_identity(
                cleaned,
                settings.configuration.owner_markers,
                settings.configuration.legal_suffixes,
                settings.configuration.ignored_counterparty_values,
            ):
                return cleaned

    return None


def sanitize_filename_value(value: str, field: str) -> str:
    """Normalize one semantic value into a cross-platform filename segment."""

    # Remove path syntax and control characters while preserving human-readable
    # Unicode.
    candidate = INVALID_FILENAME_CHARACTERS.sub("-", value)
    candidate = "".join(character for character in candidate if character.isprintable())
    candidate = re.sub(r"\s+", " ", candidate).strip()
    if not candidate or not candidate.strip("."):
        raise PlanError(f"Field {field} becomes empty after filename sanitization")

    return candidate


def normalize_override_date(value: Any, source_name: str) -> str:
    """Require override dates to use an unambiguous ISO representation."""

    # Keep human review overrides portable across every configured locale.
    if not isinstance(value, str):
        raise PlanError(f"Override date for {source_name} must be YYYY-MM-DD")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as error:
        raise PlanError(
            f"Override date for {source_name} must be YYYY-MM-DD"
        ) from error


def validate_overrides(
    overrides: Mapping[str, Mapping[str, Any]] | None,
    source_names: set[str],
) -> dict[str, dict[str, Any]]:
    """Validate semantic review overrides against the current folder inventory."""

    # Reject stale filenames and unsupported decisions before extracting
    # documents.
    result: dict[str, dict[str, Any]] = {}
    for source_name, raw_fields in (overrides or {}).items():
        if source_name not in source_names:
            raise PlanError(
                f"Override references a PDF not present in the folder: {source_name}"
            )
        if not isinstance(raw_fields, Mapping):
            raise PlanError(f"Override for {source_name} must be an object")
        reject_unknown_keys(raw_fields, OVERRIDE_FIELDS, f"override {source_name}")
        fields: dict[str, Any] = {}
        for field, value in raw_fields.items():
            if field == "date":
                fields[field] = normalize_override_date(value, source_name)
            elif field == "description" and value is None:
                fields[field] = None
            else:
                fields[field] = require_string(value, f"override {source_name}.{field}")
        result[source_name] = fields

    return result


def extract_metadata(
    path: Path,
    text: str,
    settings: EffectiveSettings,
    override: Mapping[str, Any],
) -> dict[str, Any]:
    """Extract semantic metadata for one explicitly selected document type."""

    # Derive only content facts; the document type has already been fixed by the
    # required flag.
    profile = find_profile(text, settings)
    document_date = find_document_date(text, settings, profile)
    counterparty = find_counterparty(text, settings, profile)
    identifier = find_identifier(text, settings, profile)
    description = profile.description(text) if profile else None
    metadata: dict[str, Any] = {
        "counterparty": counterparty,
        "date": document_date.isoformat() if document_date else None,
        "description": description,
        "identifier": identifier,
        "profile": profile.name if profile else None,
    }

    # Apply explicit human or agent review decisions after deterministic
    # extraction.
    metadata.update(override)
    issues = [field for field in ("date", "counterparty") if not metadata[field]]
    if (
        settings.document_type.identifier_policy == "always"
        and not metadata["identifier"]
    ):
        issues.append("identifier")
    metadata["issues"] = issues

    return metadata


def render_filename(
    metadata: Mapping[str, Any],
    settings: EffectiveSettings,
    *,
    include_identifier: bool,
) -> str:
    """Render one complete filename from validated semantic fields."""

    # Convert the ISO semantic date only at the presentation boundary.
    document_date = date.fromisoformat(str(metadata["date"]))
    description = metadata.get("description") or ""
    identifier = metadata.get("identifier") or ""
    values = {
        "counterparty": sanitize_filename_value(
            str(metadata["counterparty"]), "counterparty"
        ),
        "date": document_date.strftime(settings.output.date_format),
        "description": sanitize_filename_value(str(description), "description")
        if description
        else "",
        "extension": sanitize_filename_value(settings.output.extension, "extension"),
        "identifier": sanitize_filename_value(str(identifier), "identifier")
        if identifier
        else "",
        "prefix": sanitize_filename_value(
            require_string(
                settings.document_type.prefix, "resolved document type prefix"
            ),
            "prefix",
        ),
        "type": sanitize_filename_value(settings.document_type.name, "type"),
    }
    values["description_part"] = (
        settings.output.description_template.format(description=values["description"])
        if values["description"]
        else ""
    )
    values["identifier_part"] = (
        settings.output.identifier_template.format(identifier=values["identifier"])
        if include_identifier and values["identifier"]
        else ""
    )

    # Sanitize the final literal result as a single filename, never a path.
    rendered = settings.output.template.format_map(values)
    if Path(rendered).name != rendered or rendered in {".", ".."}:
        raise PlanError("Output template produced a path instead of a filename")
    rendered = "".join(
        character for character in rendered if character.isprintable()
    ).strip(" .")
    if not rendered or INVALID_FILENAME_CHARACTERS.search(rendered):
        raise PlanError("Output template produced an invalid cross-platform filename")
    if len(rendered.encode()) > 240:
        raise PlanError("Output template produced a filename longer than 240 bytes")

    return rendered


def summarize(items: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    """Count plan items by their stable workflow status."""

    # Always return every status so callers need no missing-key behavior.
    counts = {"already_correct": 0, "needs_review": 0, "ready": 0}
    for item in items:
        counts[str(item["status"])] += 1

    return counts


def calculate_plan_id(plan: Mapping[str, Any]) -> str:
    """Hash every executable plan decision except the identifier itself."""

    # Canonical JSON makes direct plan edits detectable before mutation.
    material = {key: value for key, value in plan.items() if key != "plan_id"}
    encoded = json.dumps(
        material, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()

    return hashlib.sha256(encoded).hexdigest()


def build_plan(
    folder: Path,
    document_type: str,
    *,
    config_path: Path | None = None,
    use_user_config: bool = True,
    cli_overrides: Mapping[str, Any] | None = None,
    locale_files: Sequence[Path] = (),
    overrides: Mapping[str, Mapping[str, Any]] | None = None,
    extractor: TextExtractor | None = None,
) -> dict[str, Any]:
    """Build a complete non-mutating rename plan for one explicit document type."""

    # Gate the production path before configuration, folder inventory, or PDF
    # extraction.
    if extractor is None:
        check_poppler()
        extractor = extract_pdf_text
    resolved_cli_overrides = dict(cli_overrides or {})
    configuration = load_configuration(
        config_path,
        use_user_config=use_user_config,
        locale_names=resolved_cli_overrides.get("locales"),
        locale_files=locale_files,
    )
    settings = resolve_settings(configuration, document_type, resolved_cli_overrides)
    resolved_folder = validate_folder(folder)

    # Inventory direct PDF children only and validate review input against that
    # fixed set.
    sources = sorted(
        (
            path
            for path in resolved_folder.iterdir()
            if path.is_file() and path.suffix.casefold() == ".pdf"
        ),
        key=lambda path: path.name.casefold(),
    )
    if not sources:
        raise PlanError(f"No PDF files found directly in: {resolved_folder}")
    source_names = {path.name for path in sources}
    validated_overrides = validate_overrides(overrides, source_names)

    # Extract and hash each document before resolving cross-document filename
    # collisions.
    items: list[dict[str, Any]] = []
    for path in sources:
        try:
            text = extractor(path)
            metadata = extract_metadata(
                path, text, settings, validated_overrides.get(path.name, {})
            )
            extraction_error = None
        except PlanError as error:
            metadata = {
                "counterparty": None,
                "date": None,
                "description": None,
                "identifier": None,
                "profile": None,
                "issues": ["extraction"],
            }
            extraction_error = str(error)
        item: dict[str, Any] = {
            "source_name": path.name,
            "source_size": path.stat().st_size,
            "source_sha256": file_digest(path),
            "metadata": {
                key: value for key, value in metadata.items() if key != "issues"
            },
            "issues": list(metadata["issues"]),
            "status": "needs_review" if metadata["issues"] else "ready",
            "target_name": None,
        }
        if extraction_error:
            item["error"] = extraction_error
        items.append(item)

    # Render base candidates before deciding whether collision identifiers are
    # necessary.
    candidate_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        if item["status"] != "ready":
            continue
        include_identifier = settings.document_type.identifier_policy == "always"
        target = render_filename(
            item["metadata"], settings, include_identifier=include_identifier
        )
        item["target_name"] = target
        candidate_groups[target.casefold()].append(item)

    # Resolve same-name groups with stable identifiers only when the selected
    # policy permits it.
    if settings.document_type.identifier_policy == "collision":
        for group in candidate_groups.values():
            if len(group) < 2:
                continue
            identifiers = [item["metadata"].get("identifier") for item in group]
            if any(not identifier for identifier in identifiers) or len(
                {str(value).casefold() for value in identifiers}
            ) != len(group):
                for item in group:
                    item["target_name"] = None
                    item["status"] = "needs_review"
                    item["issues"] = unique((*item["issues"], "identifier"))
                continue
            for item in group:
                item["target_name"] = render_filename(
                    item["metadata"], settings, include_identifier=True
                )

    # Detect any remaining target collision and distinguish verified no-op
    # filenames.
    final_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        if item["target_name"]:
            final_groups[str(item["target_name"]).casefold()].append(item)
    for group in final_groups.values():
        if len(group) > 1:
            for item in group:
                item["target_name"] = None
                item["status"] = "needs_review"
                item["issues"] = unique((*item["issues"], "target_collision"))
    for item in items:
        if item["status"] == "ready" and item["source_name"] == item["target_name"]:
            item["status"] = "already_correct"

    # Bind the exact configuration and source decisions into a portable plan
    # document.
    plan: dict[str, Any] = {
        "version": PLAN_VERSION,
        "folder": str(resolved_folder),
        "document_type": settings.document_type.name,
        "locales": list(configuration.locale_names),
        "configuration_sources": [
            str(configuration.bundled_source),
            *([str(configuration.source)] if configuration.source else []),
        ],
        "locale_sources": {
            name: str(configuration.locales[name].source)
            for name in configuration.locale_names
        },
        "configuration_digest": configuration.digest,
        "items": items,
        "summary": summarize(items),
    }
    plan["plan_id"] = calculate_plan_id(plan)

    return plan


def validate_plan(plan: Mapping[str, Any]) -> tuple[Path, list[Mapping[str, Any]]]:
    """Validate a serialized plan before any filesystem mutation."""

    # Require the supported schema and an intact content-addressed plan
    # identifier.
    if plan.get("version") != PLAN_VERSION:
        raise PlanError(f"Unsupported plan version: {plan.get('version')!r}")
    if plan.get("plan_id") != calculate_plan_id(plan):
        raise PlanError("Plan content does not match its plan_id; create a fresh plan")
    raw_items = plan.get("items")
    if not isinstance(raw_items, list):
        raise PlanError("Plan items must be an array")
    items: list[Mapping[str, Any]] = [
        require_mapping(item, "plan item") for item in raw_items
    ]
    if any(item.get("status") == "needs_review" for item in items):
        raise PlanError(
            "Plan contains needs_review items; resolve them and create a fresh plan"
        )
    if any(item.get("status") not in {"ready", "already_correct"} for item in items):
        raise PlanError("Plan contains an unsupported item status")
    folder = validate_folder(Path(require_string(plan.get("folder"), "plan.folder")))

    # Verify every source and destination remains within the one planned folder.
    source_names: set[str] = set()
    source_names_casefolded: set[str] = set()
    target_names: set[str] = set()
    for item in items:
        source_name = require_string(item.get("source_name"), "plan item source_name")
        target_name = require_string(item.get("target_name"), "plan item target_name")
        if (
            Path(source_name).name != source_name
            or Path(target_name).name != target_name
        ):
            raise PlanError(
                "Plan contains a source or target path instead of a filename"
            )
        if source_name in source_names or target_name.casefold() in target_names:
            raise PlanError("Plan contains duplicate sources or targets")
        source_names.add(source_name)
        source_names_casefolded.add(source_name.casefold())
        target_names.add(target_name.casefold())

    # Reject changed sources and destinations occupied outside the planned
    # rename set.
    for item in items:
        source = folder / str(item["source_name"])
        target = folder / str(item["target_name"])
        if not source.is_file():
            raise PlanError(f"Source is missing since planning: {source.name}")
        if source.stat().st_size != item.get("source_size") or file_digest(
            source
        ) != item.get("source_sha256"):
            raise PlanError(f"Source changed since planning: {source.name}")
        if (
            target != source
            and target.exists()
            and target.name.casefold() not in source_names_casefolded
        ):
            raise PlanError(f"Target already exists outside the plan: {target.name}")

    return folder, items


def apply_plan(plan: Mapping[str, Any]) -> dict[str, Any]:
    """Apply one intact reviewed plan through a collision-safe two-phase rename."""

    # Complete every read-only safety check before moving the first source.
    folder, items = validate_plan(plan)
    ready = [item for item in items if item["status"] == "ready"]
    temporary: list[tuple[Path, Path, Path]] = []

    # Vacate every source name before assigning destinations that may overlap
    # the source set.
    try:
        for item in ready:
            source = folder / str(item["source_name"])
            target = folder / str(item["target_name"])
            temporary_path = folder / f".{TOOL_NAME}-{uuid.uuid4().hex}.tmp"
            source.rename(temporary_path)
            temporary.append((source, temporary_path, target))
    except OSError as error:
        for source, temporary_path, _ in reversed(temporary):
            if temporary_path.exists() and not source.exists():
                temporary_path.rename(source)
        raise PlanError(f"Could not stage rename operation: {error}") from error

    # Assign final names and make a best-effort rollback if the filesystem
    # rejects a destination.
    completed: list[tuple[Path, Path, Path]] = []
    try:
        for source, temporary_path, target in temporary:
            temporary_path.rename(target)
            completed.append((source, temporary_path, target))
    except OSError as error:
        for source, _, target in reversed(completed):
            if target.exists() and not source.exists():
                target.rename(source)
        for source, temporary_path, _ in reversed(temporary[len(completed) :]):
            if temporary_path.exists() and not source.exists():
                temporary_path.rename(source)
        raise PlanError(f"Could not complete rename operation: {error}") from error

    return {
        "status": "ok",
        "plan_id": plan["plan_id"],
        "renamed_count": len(ready),
        "unchanged_count": len(items) - len(ready),
    }


def load_json(path: Path) -> Any:
    """Load one JSON input file under the shared error contract."""

    # Convert both filesystem and syntax errors into concise command failures.
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PlanError(f"Could not read JSON file {path}: {error}") from error


def write_json(value: Any, output: Path | None) -> None:
    """Write stable readable JSON to a file or standard output."""

    # Keep command output directly inspectable and suitable for later apply
    # input.
    rendered = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if output is None:
        sys.stdout.write(rendered)
        return
    try:
        output.expanduser().write_text(rendered, encoding="utf-8")
    except OSError as error:
        raise PlanError(f"Could not write JSON file {output}: {error}") from error


def add_configuration_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the mutually exclusive configuration source flags."""

    # Keep discovery explicit in help while preserving the normal per-user
    # default.
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--config",
        type=Path,
        help="Use this TOML file instead of the discovered user configuration",
    )
    group.add_argument(
        "--no-config",
        action="store_true",
        help="Ignore personal configuration and locale files",
    )
    parser.add_argument(
        "--locale",
        action="append",
        dest="locales",
        help="Select a document locale; repeat to select more than one",
    )
    parser.add_argument(
        "--locale-file",
        action="append",
        default=[],
        type=Path,
        dest="locale_files",
        help="Use a complete locale file for its declared locale; repeat as needed",
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the complete user-invoked command interface."""

    # Expose only dependency checking, pure planning, and reviewed plan
    # application.
    parser = argparse.ArgumentParser(prog="rename_invoices.py", description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser(
        "check", help="Check Poppler and configuration"
    )
    add_configuration_arguments(check_parser)

    plan_parser = subparsers.add_parser(
        "plan", help="Create a non-mutating JSON rename plan"
    )
    plan_parser.add_argument(
        "--folder",
        default=Path("."),
        type=Path,
        help="Folder whose direct PDF children are planned; defaults to .",
    )
    plan_parser.add_argument(
        "--type",
        required=True,
        dest="document_type",
        help="Explicit configured document type",
    )
    add_configuration_arguments(plan_parser)
    plan_parser.add_argument("--prefix", help="Override the filename prefix")
    plan_parser.add_argument(
        "--template", help="Override the complete filename format template"
    )
    plan_parser.add_argument("--date-format", help="Override the strftime date format")
    plan_parser.add_argument(
        "--description-template",
        help="Override the optional description segment template",
    )
    plan_parser.add_argument(
        "--extension", help="Override the output filename extension"
    )
    plan_parser.add_argument(
        "--identifier-template",
        help="Override the optional identifier segment template",
    )
    plan_parser.add_argument(
        "--date-source",
        action="append",
        dest="date_sources",
        help="Override date source priority; repeat for more than one source",
    )
    plan_parser.add_argument("--counterparty-source", choices=("issuer", "recipient"))
    plan_parser.add_argument(
        "--identifier-policy", choices=("always", "collision", "never")
    )
    plan_parser.add_argument(
        "--overrides",
        type=Path,
        help="Load reviewed per-file semantic overrides from JSON",
    )
    plan_parser.add_argument(
        "--output", type=Path, help="Write the plan to this JSON file instead of stdout"
    )

    apply_parser = subparsers.add_parser(
        "apply", help="Apply one intact reviewed JSON plan"
    )
    apply_parser.add_argument(
        "plan", type=Path, help="Plan file created by the plan command"
    )
    apply_parser.add_argument(
        "--output",
        type=Path,
        help="Write the result to this JSON file instead of stdout",
    )

    return parser


def cli_overrides_from_arguments(arguments: argparse.Namespace) -> dict[str, Any]:
    """Collect only explicit plan flags for highest-precedence settings."""

    # Omitted argparse values must not erase configured behavior.
    fields = {
        "locales",
        "prefix",
        "template",
        "date_format",
        "description_template",
        "extension",
        "identifier_template",
        "date_sources",
        "counterparty_source",
        "identifier_policy",
    }

    return {
        field: getattr(arguments, field)
        for field in fields
        if getattr(arguments, field, None) is not None
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Run the user-invoked command and emit machine-readable JSON."""

    # Route every command through one concise error contract suitable for
    # low-cost agents.
    parser = build_parser()
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "check":
            result = check_environment(
                arguments.config,
                use_user_config=not arguments.no_config,
                locale_names=arguments.locales,
                locale_files=arguments.locale_files,
            )
            write_json(result, None)
            return 0
        if arguments.command == "plan":
            raw_overrides = (
                load_json(arguments.overrides) if arguments.overrides else None
            )
            if raw_overrides is not None and not isinstance(raw_overrides, Mapping):
                raise PlanError(
                    "Overrides JSON root must be an object keyed by source filename"
                )
            plan = build_plan(
                arguments.folder,
                arguments.document_type,
                config_path=arguments.config,
                use_user_config=not arguments.no_config,
                cli_overrides=cli_overrides_from_arguments(arguments),
                locale_files=arguments.locale_files,
                overrides=raw_overrides,
            )
            write_json(plan, arguments.output)
            return 0

        raw_plan = load_json(arguments.plan)
        if not isinstance(raw_plan, Mapping):
            raise PlanError("Plan JSON root must be an object")
        result = apply_plan(raw_plan)
        write_json(result, arguments.output)
        return 0
    except PlanError as error:
        parser.exit(2, f"error: {error}\n")


if __name__ == "__main__":
    # Execute the CLI only when the script is invoked directly.
    raise SystemExit(main())
