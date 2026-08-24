# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Select one Language Resource and hand back only the scopes a caller can use.

A Language Resource is one Markdown source for one language or locale: its
frontmatter carries everything needed to choose it, and its body carries four
separately addressable scopes. Several editorial Skills need the same language
identity and different parts of the same guidance, so the choosing happens here
once rather than in each of their instructions.

Two properties are the whole reason this is a script and not prose. It is
deterministic — a selector either reaches exactly one installed resource or is
refused with a diagnostic saying which of the four ways it failed — and it is
frugal: inventorying reads frontmatter and stops at its closing delimiter, and a
body is opened only to extract a scope somebody asked for. A caller wanting
mechanics never pays for composition guidance it cannot use.

Interpreting an unlisted human description of a language is the agent's work,
not this script's. Where nothing matches, the refusal names the installed
inventory so the agent can propose a candidate and verify it through this same
interface, rather than being handed a guess it cannot tell from a match.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

import yaml

# The four scopes, each named for the guidance it holds rather than for the
# Skill that reads it: a scope two Skills consume must not read as one Skill's
# property. The heading is the address inside the body; the key is the address
# on the command line.
SCOPE_HEADINGS: dict[str, str] = {
    "composition": "Composition",
    "review": "Review",
    "anti-slop": "Anti-slop",
    "mechanics": "Mechanics",
}
SCOPES: tuple[str, ...] = tuple(SCOPE_HEADINGS)
HEADINGS: dict[str, str] = {heading: scope for scope, heading in SCOPE_HEADINGS.items()}

# The complete frontmatter vocabulary. A key outside it is a misspelling, and a
# misspelled selector field is a resource nobody can reach.
FIELDS = frozenset(
    {
        "code",
        "language",
        "territory",
        "territory-name",
        "aliases",
        "default-for",
        "inherits",
    }
)

# The canonical spelling a resource declares itself with: a lowercase language
# subtag, optionally an uppercase territory subtag after an underscore. Selectors
# are normalised into this space; the file itself is held to the canonical form.
CODE = re.compile(r"^[a-z]{2,3}(?:_[A-Z]{2})?$")
TERRITORY = re.compile(r"^[A-Z]{2}$")

# Aliases are curated human names and abbreviations, not an exhaustive registry;
# the cap is what keeps that a rule rather than an intention.
MAX_ALIASES = 12

# Case and separators carry no meaning in a selector, so `en-GB`, `EN_GB`, and
# `en gb` are normalised into one key before anything is compared.
SEPARATORS = re.compile(r"[\s_-]+")

# A `##` heading and nothing deeper: a `###` inside a scope is that scope's own
# content, not the start of another one.
HEADING = re.compile(r"^## (.+?)\s*$")

# The file beside the resources that documents their format, rather than a
# resource of its own.
FORMAT_PAGE = "README.md"

# One exit code per way a selector can fail, because a caller that has to parse
# prose to tell an absent language from an ambiguous one is a caller that
# guesses.
ABSENT = 3
AMBIGUOUS = 4
MALFORMED = 5
INHERITANCE = 6


class ResolverError(RuntimeError):
    """A refusal carrying the kind and the exit code that distinguish it."""

    kind: ClassVar[str] = "error"
    status: ClassVar[int] = 1


class MalformedResource(ResolverError):
    """A resource's metadata or structure is not well formed."""

    kind: ClassVar[str] = "malformed-resource"
    status: ClassVar[int] = MALFORMED


class AbsentLanguage(ResolverError):
    """No installed resource answers to this selector."""

    kind: ClassVar[str] = "no-such-language"
    status: ClassVar[int] = ABSENT


class AmbiguousSelector(ResolverError):
    """Several installed resources answer to this selector."""

    kind: ClassVar[str] = "ambiguous-selector"
    status: ClassVar[int] = AMBIGUOUS


class InheritanceError(ResolverError):
    """A resource's declared base cannot be resolved in exactly one step."""

    kind: ClassVar[str] = "inheritance-error"
    status: ClassVar[int] = INHERITANCE


def key(value: str) -> str:
    """Return the comparison key of a selector, code, alias, or default.

    Case and the three separators a language tag is written with carry no
    meaning, so they are removed before anything is matched. This is the whole
    of normalisation: nothing here guesses at a language, it only stops two
    spellings of one from being two things.
    """

    return SEPARATORS.sub(" ", value.strip().casefold())


@dataclass(frozen=True)
class Resource:
    """One Language Resource, as its frontmatter alone describes it."""

    path: Path
    code: str
    language: str
    territory: str | None
    territory_name: str | None
    aliases: tuple[str, ...]
    default_for: tuple[str, ...]
    inherits: str | None

    def entry(self) -> dict[str, Any]:
        """Return the resource as the inventory reports it."""

        return {
            "code": self.code,
            "language": self.language,
            "territory": self.territory,
            "territory_name": self.territory_name,
            "aliases": list(self.aliases),
            "default_for": list(self.default_for),
            "inherits": self.inherits,
            "path": str(self.path),
        }


def read_frontmatter(path: Path) -> str:
    """Return the frontmatter of *path*, having read no further into the file.

    The file is opened in binary and abandoned at the closing delimiter, so the
    body is never decoded and its size never paid for. That is what makes an
    inventory of every installed language cheap enough to run before knowing
    which one is wanted.
    """

    lines: list[bytes] = []
    try:
        with path.open("rb") as handle:
            opening = handle.readline()
            if opening.strip() != b"---":
                raise MalformedResource(
                    f"{path}: a Language Resource opens with a `---` frontmatter"
                    f" delimiter."
                )
            for line in handle:
                if line.strip() == b"---":
                    break
                lines.append(line)
            else:
                raise MalformedResource(f"{path}: the frontmatter is never closed.")
    except OSError as exc:
        raise MalformedResource(f"{path}: could not be read: {exc}") from exc

    try:
        return b"".join(lines).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MalformedResource(f"{path}: frontmatter is not UTF-8: {exc}") from exc


def _string(path: Path, document: dict[str, Any], field: str) -> str | None:
    """Return one optional string field, refusing any other shape."""

    value = document.get(field)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise MalformedResource(f"{path}: `{field}` is a non-empty string.")
    return value.strip()


def _strings(path: Path, document: dict[str, Any], field: str) -> tuple[str, ...]:
    """Return one optional list-of-strings field, refusing any other shape."""

    value = document.get(field)
    if value is None:
        return ()
    if not isinstance(value, list) or not value:
        raise MalformedResource(f"{path}: `{field}` is a non-empty list of strings.")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise MalformedResource(
                f"{path}: `{field}` holds non-empty strings; found {item!r}."
            )
    return tuple(item.strip() for item in value)


def load(path: Path) -> Resource:
    """Read and validate one resource's frontmatter into a `Resource`."""

    # A resource declares itself in YAML, so YAML is what reads it: anything a
    # real parser accepts is what the field means.
    try:
        document = yaml.safe_load(read_frontmatter(path))
    except yaml.YAMLError as exc:
        raise MalformedResource(
            f"{path}: frontmatter is not valid YAML: {exc}"
        ) from exc
    if not isinstance(document, dict):
        raise MalformedResource(f"{path}: frontmatter is a mapping of fields.")

    # A key outside the vocabulary is a misspelling, and a misspelled selector
    # field is guidance nothing can ever select.
    unknown = sorted(set(document) - FIELDS)
    if unknown:
        raise MalformedResource(
            f"{path}: `{'`, `'.join(unknown)}` is not a Language Resource field;"
            f" the fields are `{'`, `'.join(sorted(FIELDS))}`."
        )

    # Identity first: the canonical code and the one English language name are
    # what every other field hangs off.
    code = _string(path, document, "code")
    language = _string(path, document, "language")
    if code is None or language is None:
        raise MalformedResource(f"{path}: `code` and `language` are both required.")
    if not CODE.match(code):
        raise MalformedResource(
            f"{path}: `code` is written canonically as `xx` or `xx_YY`; found `{code}`."
        )

    # The territory is optional, and where it is written it is written the one
    # way a reader outside this collection expects to meet it.
    territory = _string(path, document, "territory")
    if territory is not None and not TERRITORY.match(territory):
        raise MalformedResource(
            f"{path}: `territory` is a two-letter uppercase code; found `{territory}`."
        )

    aliases = _strings(path, document, "aliases")
    if len(aliases) > MAX_ALIASES:
        raise MalformedResource(
            f"{path}: `aliases` is a curated set of at most {MAX_ALIASES} human"
            f" names and abbreviations; found {len(aliases)}."
        )
    if len({key(alias) for alias in aliases}) != len(aliases):
        raise MalformedResource(f"{path}: two aliases normalise to one selector.")

    # Inheritance is declared in the same canonical spelling as a code, so a
    # base named in some other form is caught before anything tries to find it.
    inherits = _string(path, document, "inherits")
    if inherits is not None and not CODE.match(inherits):
        raise MalformedResource(
            f"{path}: `inherits` names a canonical code; found `{inherits}`."
        )

    return Resource(
        path=path,
        code=code,
        language=language,
        territory=territory,
        territory_name=_string(path, document, "territory-name"),
        aliases=aliases,
        default_for=_strings(path, document, "default-for"),
        inherits=inherits,
    )


@dataclass(frozen=True)
class Inventory:
    """Every installed Language Resource, described by frontmatter alone."""

    directory: Path
    resources: tuple[Resource, ...]

    def by_code(self, selector: str) -> Resource | None:
        """Return the resource whose canonical code *selector* spells."""

        wanted = key(selector)
        return next((r for r in self.resources if key(r.code) == wanted), None)

    def codes(self) -> str:
        """Return the installed codes, for a refusal the agent can act on."""

        return ", ".join(sorted(resource.code for resource in self.resources))


def read_inventory(directory: Path) -> Inventory:
    """Inventory every resource in *directory*, reading frontmatter only."""

    if not directory.is_dir():
        raise MalformedResource(
            f"{directory}: no Language Resource inventory at this path."
        )

    # The format page sits beside the resources it documents and is not one of
    # them; everything else in the directory has to be a resource.
    paths = [
        path for path in sorted(directory.glob("*.md")) if path.name != FORMAT_PAGE
    ]
    if not paths:
        raise MalformedResource(f"{directory}: the inventory holds no resources.")

    resources = tuple(load(path) for path in paths)

    # A canonical code names one resource, or a citation of it cannot say which
    # resource it means.
    seen: dict[str, Path] = {}
    for resource in resources:
        collision = seen.get(key(resource.code))
        if collision is not None:
            raise MalformedResource(
                f"{resource.path}: the canonical code `{resource.code}` is already"
                f" claimed by {collision}."
            )
        seen[key(resource.code)] = resource.path

    # An alias spelling a canonical code is an alias nothing can ever reach,
    # because a code is matched before any alias is looked at.
    for resource in resources:
        for alias in resource.aliases:
            owner = seen.get(key(alias))
            if owner is not None:
                raise MalformedResource(
                    f"{resource.path}: the alias `{alias}` spells the canonical"
                    f" code a resource already carries ({owner}); aliases carry"
                    f" human names and abbreviations."
                )

    return Inventory(directory=directory, resources=resources)


def select(inventory: Inventory, selector: str) -> Resource:
    """Return the one resource *selector* reaches, or refuse with the reason.

    Three matchers, tried in a fixed order and never blended: the canonical code
    a resource declares, a default another selector was declared to stand for,
    and a curated alias. Where two resources answer the same way the selector is
    ambiguous, and where none does the language is absent — neither is a case
    this returns a best guess for.
    """

    wanted = key(selector)

    # The canonical code a resource declares, whatever case and separator the
    # selector spelled it with.
    exact = inventory.by_code(wanted)
    if exact is not None:
        return exact

    # A bare selector the resource itself declared it stands for, which is how
    # bare English becomes British English without a table anywhere else.
    declared = [
        resource
        for resource in inventory.resources
        if wanted in {key(value) for value in resource.default_for}
    ]
    if len(declared) > 1:
        raise AmbiguousSelector(
            f"`{selector}` is declared the default of"
            f" {', '.join(sorted(r.code for r in declared))}; name one canonical"
            f" code."
        )
    if declared:
        return declared[0]

    # A curated human name or abbreviation, last because a code and a declared
    # default are both stronger claims on the same spelling.
    aliased = [
        resource
        for resource in inventory.resources
        if wanted in {key(alias) for alias in resource.aliases}
    ]
    if len(aliased) > 1:
        raise AmbiguousSelector(
            f"`{selector}` is an alias of"
            f" {', '.join(sorted(r.code for r in aliased))}; name one canonical"
            f" code."
        )
    if aliased:
        return aliased[0]

    raise AbsentLanguage(
        f"`{selector}` reaches no installed Language Resource; installed:"
        f" {inventory.codes()}."
    )


def base_of(inventory: Inventory, resource: Resource) -> Resource | None:
    """Return the resource *resource* inherits from, refusing anything longer.

    Inheritance is one step by contract, so a chain, a cycle, and a base nothing
    installs are all reported here rather than flattened into a resource that
    silently answers with less than it claims.
    """

    if resource.inherits is None:
        return None

    if key(resource.inherits) == key(resource.code):
        raise InheritanceError(
            f"{resource.path}: `{resource.code}` inherits from itself."
        )

    base = inventory.by_code(resource.inherits)
    if base is None:
        raise InheritanceError(
            f"{resource.path}: `{resource.code}` inherits from"
            f" `{resource.inherits}`, which no installed resource carries;"
            f" installed: {inventory.codes()}."
        )
    if base.inherits is not None:
        raise InheritanceError(
            f"{resource.path}: `{resource.code}` inherits from `{base.code}`,"
            f" which inherits in turn; inheritance is one step."
        )
    return base


def sections(path: Path) -> dict[str, str]:
    """Return the scopes *path*'s body carries, keyed by their scope name.

    This is the only place a body is read, and it is reached only once a caller
    has asked for a scope. Anything above the first heading is the resource's
    own introduction; a heading the format does not define is refused, because
    guidance nothing can request is guidance nobody will read.
    """

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise MalformedResource(f"{path}: the body could not be read: {exc}") from exc

    # Walk the body once, attributing every line to the scope heading above it.
    found: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        heading = HEADING.match(line)
        if heading is None:
            if current is not None:
                found[current].append(line)
            continue
        title = heading.group(1)
        scope = HEADINGS.get(title)
        if scope is None:
            raise MalformedResource(
                f"{path}: `## {title}` is not a Language Resource scope; the"
                f" scopes are `{'`, `'.join(SCOPE_HEADINGS.values())}`."
            )
        if scope in found:
            raise MalformedResource(f"{path}: the scope `{scope}` is written twice.")
        current = scope
        found[scope] = []

    return {scope: "\n".join(lines).strip() for scope, lines in found.items()}


def scope_of(
    inventory: Inventory,
    resource: Resource,
    wanted: str,
    bodies: dict[Path, dict[str, str]],
) -> dict[str, str]:
    """Return one scope's text and the resource it actually came from."""

    # One caller may ask for several scopes out of the same two files, so each
    # body is parsed once per invocation rather than once per scope.
    def body(of: Resource) -> dict[str, str]:
        if of.path not in bodies:
            bodies[of.path] = sections(of.path)
        return bodies[of.path]

    # The resource answers for itself where it wrote the scope, and falls back to
    # the one base it may inherit from where it did not.
    own = body(resource).get(wanted, "")
    if own:
        return {"source": resource.code, "content": own}

    base = base_of(inventory, resource)
    if base is not None:
        inherited = body(base).get(wanted, "")
        if inherited:
            return {"source": base.code, "content": inherited}

    raise MalformedResource(
        f"{resource.path}: the scope `{wanted}` is carried neither by"
        f" `{resource.code}` nor by a base it inherits from."
    )


def cmd_list(directory: Path) -> int:
    """Report every installed resource, from frontmatter alone."""

    inventory = read_inventory(directory)
    payload = {"resources": [resource.entry() for resource in inventory.resources]}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def cmd_resolve(directory: Path, selector: str, wanted: list[str]) -> int:
    """Resolve *selector* and return only the scopes *wanted* asked for."""

    inventory = read_inventory(directory)
    resource = select(inventory, selector)

    # Verify the declared inheritance before any scope is extracted, so a broken
    # base is reported even by a caller that only wanted the canonical code.
    base_of(inventory, resource)

    bodies: dict[Path, dict[str, str]] = {}
    payload: dict[str, Any] = {
        "selector": selector,
        "code": resource.code,
        "language": resource.language,
        "territory": resource.territory,
        "territory_name": resource.territory_name,
        "inherits": resource.inherits,
        "path": str(resource.path),
        "scopes": {
            scope: scope_of(inventory, resource, scope, bodies) for scope in wanted
        },
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def _problems(inventory: Inventory) -> list[dict[str, str]]:
    """Collect everything wrong with an inventory whose metadata already parsed."""

    problems: list[dict[str, str]] = []

    # Two resources answering to one selector is a question with two answers,
    # which is the one thing a deterministic resolver may not have.
    claimed: dict[str, list[str]] = {}
    for resource in inventory.resources:
        for selector in (*resource.aliases, *resource.default_for):
            claimed.setdefault(key(selector), []).append(resource.code)
    for selector, owners in sorted(claimed.items()):
        if len(owners) > 1:
            problems.append(
                {
                    "resource": ", ".join(sorted(owners)),
                    "kind": AmbiguousSelector.kind,
                    "message": f"`{selector}` reaches {len(owners)} resources.",
                }
            )

    # Every resource has to answer all four scopes, itself or through the one
    # base it is allowed to inherit from.
    bodies: dict[Path, dict[str, str]] = {}
    for resource in inventory.resources:
        for scope in SCOPES:
            try:
                scope_of(inventory, resource, scope, bodies)
            except ResolverError as exc:
                problems.append(
                    {
                        "resource": resource.code,
                        "kind": type(exc).kind,
                        "message": str(exc),
                    }
                )

    return problems


def cmd_validate(directory: Path) -> int:
    """Report whether every installed resource is well formed."""

    inventory = read_inventory(directory)
    problems = _problems(inventory)
    payload = {"resources": len(inventory.resources), "problems": problems}
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    kinds = {problem["kind"] for problem in problems}
    if MalformedResource.kind in kinds:
        return MALFORMED
    if InheritanceError.kind in kinds:
        return INHERITANCE
    if kinds:
        return AMBIGUOUS
    return 0


def default_directory() -> Path:
    """Return the inventory shipped beside this script in the Library."""

    return Path(__file__).resolve().parent.parent / "references" / "languages"


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the resolver's command line."""

    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    def with_resources(sub: argparse.ArgumentParser) -> argparse.ArgumentParser:
        sub.add_argument("--resources", default=None)
        return sub

    with_resources(commands.add_parser("list", help="Report every installed resource."))

    resolve = with_resources(
        commands.add_parser("resolve", help="Resolve one selector to one resource.")
    )
    resolve.add_argument("selector")
    resolve.add_argument("--scope", action="append", default=[], choices=SCOPES)

    with_resources(
        commands.add_parser("validate", help="Report what is wrong with the inventory.")
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run one resolver command and return its exit code."""

    args = parse_args(sys.argv[1:] if argv is None else argv)
    directory = Path(args.resources) if args.resources else default_directory()

    try:
        if args.command == "list":
            return cmd_list(directory)
        if args.command == "resolve":
            return cmd_resolve(directory, args.selector, args.scope)
        return cmd_validate(directory)
    except ResolverError as exc:
        print(f"{type(exc).kind}: {exc}", file=sys.stderr)
        return type(exc).status


if __name__ == "__main__":
    raise SystemExit(main())
