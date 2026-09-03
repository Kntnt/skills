"""The command line the Library's hand-rolling engines parse, and what parses it."""

from __future__ import annotations

import importlib.util
import inspect
import json
from pathlib import Path
from typing import Any, get_args, get_type_hints

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBRARY = REPO_ROOT / "skills" / "kntnt" / "library" / "scripts"

# The one implementation of this collection's argument grammar, which the two
# engines that read their own command lines reach from beside themselves.
GRAMMAR = "argument_grammar.py"


def _load(name: str, filename: str) -> Any:
    """Load one Library module from its shipped path, the way its callers do.

    Nothing here amends `sys.path` and nothing imports a Library module by bare
    name: a directory that is not this suite's to own is not made importable
    just because a test wants a module out of it (ADR-0149).
    """

    spec = importlib.util.spec_from_file_location(name, LIBRARY / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _declared(module: Any, name: str) -> Any:
    """Resolve one module-level annotation, deferred to a string or not."""

    annotation = module.__annotations__[name]
    if isinstance(annotation, str):
        return eval(annotation, vars(module))
    return annotation


def _policy(argv: list[str], capsys: pytest.CaptureFixture[str]) -> Any:
    """Run one Standing Policy command line and return its JSON and status."""

    status = _load("kntnt_standing_policy", "standing_policy.py").main(argv)
    return json.loads(capsys.readouterr().out), status


def _observations(argv: list[str], capsys: pytest.CaptureFixture[str]) -> Any:
    """Run one routed-observation command line and return its JSON and status."""

    status = _load("kntnt_routed_observations", "routed_observations.py").main(argv)
    return json.loads(capsys.readouterr().out), status


def _attempts(directory: Path) -> Path:
    """Write one readable attempt envelope `observe` accepts and reads."""

    path = directory / "attempts.json"
    path.write_text(
        json.dumps({"schema_version": 1, "attempts": [{"attempt_id": "a1"}]}),
        encoding="utf-8",
    )
    return path


def _observations_artifact(directory: Path) -> Path:
    """Write one readable observation envelope `record` reads and refuses."""

    path = directory / "observations.json"
    path.write_text(
        json.dumps({"schema_version": 1, "observations": []}), encoding="utf-8"
    )
    return path


def test_the_policy_engine_reads_one_cohort_in_either_invocation_order(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Flags before operands and operands before flags parse to one result.

    The Skills write the flags first (ADR-0097) and this engine reads its
    Cohort first, so both orders are accepted and neither is a special case
    downstream. The attached spelling of a value is one token (ADR-0096) and
    the separated one is two, which is the other half of what the normalisation
    has to see.
    """

    attached, status = _policy(
        ["policy", "show", f"--data={tmp_path}", "python-refactor"], capsys
    )
    operand_first = _policy(
        ["policy", "show", "python-refactor", f"--data={tmp_path}"], capsys
    )[0]
    separated = _policy(
        ["policy", "show", "--data", str(tmp_path), "python-refactor"], capsys
    )[0]

    assert status == 0
    assert attached["workload_cohort"] == "python-refactor"
    assert attached["data"] == str(tmp_path)
    assert operand_first == attached
    assert separated == attached


def test_the_policy_engine_reads_the_home_store_where_no_directory_is_given(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The flagless form is the one a user types, and it reads without writing."""

    response, status = _policy(["policy", "show"], capsys)

    assert status == 0
    assert response["data"] == str(Path.home() / ".kntnt" / "model-selector")
    assert response["workload_cohort"] is None


def test_the_policy_engine_takes_its_confirmation_flag_anywhere_in_the_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`--yes` carries no value, so the token behind it stays an operand.

    This is the case the collection's one valueless flag already exercises: a
    reset naming a Cohort behind the confirmation is a reset of that Cohort,
    not of the whole store with an operand eaten.
    """

    behind, status = _policy(
        ["policy", "reset", "--yes", f"--data={tmp_path}", "python-refactor"], capsys
    )
    ahead = _policy(
        ["policy", "reset", "python-refactor", "--yes", f"--data={tmp_path}"], capsys
    )[0]

    assert status == 0
    assert behind["workload_cohort"] == "python-refactor"
    assert ahead == behind


def test_the_policy_engine_keeps_every_refusal_it_answers_with(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Each refused line, by the code and the exit status it comes back with."""

    top_level_usage = (
        "invalid_arguments",
        "Use policy show [<cohort>], policy reset [<cohort>], or purge.",
    )
    policy_usage = (
        "invalid_arguments",
        "Use policy show [<cohort>] or policy reset [<cohort>].",
    )
    refused = {
        (): top_level_usage,
        ("policy",): policy_usage,
        ("policy", "audit"): policy_usage,
        ("policy", "show", "one", "two"): (
            "invalid_arguments",
            "At most one Cohort is addressed.",
        ),
        ("policy", "show", "--unknown=1"): (
            "invalid_arguments",
            "Unsupported options.",
        ),
        ("policy", "reset", f"--data={tmp_path}"): (
            "unconfirmed_reset",
            "A reset restores the shipped default; re-run it with --yes.",
        ),
        ("purge", "operand"): ("invalid_arguments", "purge takes no operand."),
        ("purge", "--unknown=1"): ("invalid_arguments", "Unsupported options."),
    }

    for argv, expected in refused.items():
        response, status = _policy(list(argv), capsys)
        assert status == 2, argv
        assert (response["refusal"]["code"], response["refusal"]["detail"]) == expected


def test_the_observation_engine_reads_one_path_in_either_invocation_order(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`observe` accepts its artifact flag before or after the path it reads."""

    attempts = _attempts(tmp_path)
    destination = tmp_path / "artifact.json"

    attached, status = _observations(
        ["observe", str(attempts), f"--artifact={destination}"], capsys
    )
    flags_first = _observations(
        ["observe", f"--artifact={destination}", str(attempts)], capsys
    )[0]
    separated = _observations(
        ["observe", str(attempts), "--artifact", str(destination)], capsys
    )[0]

    assert status == 0
    assert attached["artifact"] == str(destination)
    assert flags_first == attached
    assert separated == attached
    assert destination.exists()


def test_the_observation_engine_records_into_the_directory_either_order_names(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`record` reaches its artifact whichever side of it the flag is written."""

    artifact = _observations_artifact(tmp_path)
    data = tmp_path / "ledger"

    attached, status = _observations(
        ["record", str(artifact), f"--data={data}"], capsys
    )
    flags_first = _observations(["record", f"--data={data}", str(artifact)], capsys)[0]
    separated = _observations(["record", str(artifact), "--data", str(data)], capsys)[0]

    assert status == 2
    assert attached["artifact_refusal"] == {
        "code": "invalid_artifact",
        "detail": "observations must be a non-empty ordered array.",
    }
    assert flags_first == attached
    assert separated == attached


def test_the_observation_engine_keeps_every_refusal_it_answers_with(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Each refused line, by the code and the exit status it comes back with."""

    attempts = _attempts(tmp_path)
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{not json", encoding="utf-8")
    usage = ("invalid_arguments", "Use observe <path>, record <path>, or purge.")
    refused: dict[tuple[str, ...], tuple[str, str]] = {
        (): usage,
        ("import",): usage,
        ("observe",): ("invalid_arguments", "Observe needs one path."),
        ("observe", "--artifact=out.json"): (
            "invalid_arguments",
            "Observe needs one path.",
        ),
        ("observe", str(attempts), "second"): (
            "invalid_arguments",
            "Unsupported options.",
        ),
        ("observe", str(attempts), "--import", "--import"): (
            "invalid_arguments",
            "Unsupported options.",
        ),
        ("observe", str(attempts), f"--data={tmp_path}"): (
            "invalid_arguments",
            "Unsupported options.",
        ),
        ("record",): ("invalid_arguments", "Record needs one path."),
        ("record", str(tmp_path / "absent.json")): ("unreadable_artifact", ""),
        ("record", str(malformed)): ("malformed_json", ""),
        ("record", str(attempts)): (
            "invalid_artifact",
            "The artifact contains an unsupported top-level field.",
        ),
        ("purge", "operand"): ("invalid_arguments", "purge takes no operand."),
        ("purge", "--unknown=1"): ("invalid_arguments", "Unsupported options."),
        ("purge", "--yes", "--yes"): ("invalid_arguments", "Unsupported options."),
    }

    for argv, (code, detail) in refused.items():
        response, status = _observations(list(argv), capsys)
        assert status == 2, argv
        assert response["artifact_refusal"]["code"] == code, argv

        # Two of these carry the operating system's or the decoder's own words,
        # which are the one part of a refusal this collection does not write.
        if detail:
            assert response["artifact_refusal"]["detail"] == detail, argv


def test_a_flag_declared_valueless_leaves_the_operand_behind_it_alone() -> None:
    """The one thing a hand-rolled parser cannot know by looking at a token.

    A flag that carries no value takes nothing from behind it, so the operand
    written there survives the normalisation. Which flags those are is not a
    property of the grammar but of the engine, so the engine names them and the
    grammar is told; the fork this replaced knew one engine's `--yes` as a
    literal and swallowed the operand behind every valueless flag the other
    engine could ever grow (issue #220).
    """

    grammar = _load("kntnt_argument_grammar", GRAMMAR)

    assert grammar.split(["--yes", "python-refactor"], {"--yes"}) == (
        ["python-refactor"],
        ["--yes"],
    )

    # An engine that declares none is parsed as a permissive command line
    # always was: the token behind a separated flag is that flag's value.
    assert grammar.split(["--data", "/tmp/store", "python-refactor"], ()) == (
        ["python-refactor"],
        ["--data", "/tmp/store"],
    )

    # An attached value is one token whatever the flag is, and the operands
    # come back in the order they were written, from either region of the line.
    assert grammar.split(["python-refactor", "--data=/tmp/store"], {"--yes"}) == (
        ["python-refactor"],
        ["--data=/tmp/store"],
    )


def test_the_option_reader_takes_a_value_in_either_spelling() -> None:
    """The engines stay permissive about the spelling they accept (ADR-0096)."""

    grammar = _load("kntnt_argument_grammar", GRAMMAR)

    assert grammar.option(["--data=/tmp/store"], "--data") == "/tmp/store"
    assert grammar.option(["--data", "/tmp/store"], "--data") == "/tmp/store"

    # Anything that is not this one flag and its value is not this flag's
    # value, which is how an engine tells an unsupported option from its own.
    assert grammar.option([], "--data") is None
    assert grammar.option(["--other=1"], "--data") is None
    assert grammar.option(["--data=/tmp/store", "--other"], "--data") is None


def test_no_library_engine_carries_its_own_copy_of_the_shared_grammar() -> None:
    """The normalising loop is written once and reached by path (ADR-0152)."""

    engines = sorted(LIBRARY.glob("*.py"))

    # A glob that matched nothing would leave the check below judging nothing.
    assert engines

    carrying = [
        path.name
        for path in engines
        if path.name != GRAMMAR
        and 'startswith("--")' in path.read_text(encoding="utf-8")
    ]
    assert carrying == [], (
        f"{carrying}: an engine that separates operands from options by hand"
        f" carries a second answer to how this collection's command lines are"
        f" read, and the two drift apart a token at a time. See {GRAMMAR}."
    )


def test_both_engines_bind_the_grammar_the_library_itself_declares() -> None:
    """One declared shape, checked against the code mypy cannot reach.

    Each engine loads this grammar by path and restates its two functions'
    signatures in its own annotations. mypy checks every call site against
    those restatements and can never compare them with the implementation,
    which arrives through a dynamic load it does not follow. A signature
    changed here would therefore leave both engines type-checking their
    callers against a shape nothing has any more, in silence.
    """

    grammar = _load("kntnt_argument_grammar", GRAMMAR)

    # Assert the declared shape describes the functions this module ships.
    for alias, function in (
        (grammar.OptionReader, grammar.option),
        (grammar.SplitReader, grammar.split),
    ):
        parameters, returns = get_args(alias.__value__)
        hints = get_type_hints(function)
        named = list(inspect.signature(function).parameters)
        assert [hints[name] for name in named] == list(parameters)
        assert hints["return"] == returns

    # Assert both engines bind those functions and declare that same shape.
    for name, filename in (
        ("kntnt_standing_policy", "standing_policy.py"),
        ("kntnt_routed_observations", "routed_observations.py"),
    ):
        engine = _load(name, filename)
        assert inspect.signature(engine._option) == inspect.signature(grammar.option)
        assert inspect.signature(engine._split) == inspect.signature(grammar.split)
        assert _declared(engine, "_option") == grammar.OptionReader.__value__
        assert _declared(engine, "_split") == grammar.SplitReader.__value__
