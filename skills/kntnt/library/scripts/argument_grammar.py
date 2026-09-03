# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Read this collection's argument grammar for an engine that answers in JSON.

The Library's other engines declare their command lines to `argparse`, which
answers a malformed one with a usage dump on stderr and its own exit status.
The two that reach this module cannot: their contract is one machine-readable
refusal carrying a stable code, on exit 2, for every line they will not run. So
they read their own arguments — and this module is the whole of how, rather
than a habit each of them keeps privately (ADR-0152).

Two things are normalised here. A value written apart from its flag is joined
to it, because the engines stay permissive about the attached spelling the
collection writes everywhere else (ADR-0096); and the operands are separated
from the options whichever order the caller wrote them in, because the Skills
write the flags first (ADR-0097) while these parsers read their own operand
first. What a flag is, an engine knows and this module does not: the flags that
carry no value are named by the engine that has them, so a valueless flag never
takes the operand written behind it.

The module is loaded by path from beside the engine that reads it, the way the
Library's own cross-module load already is: a peer Skill's `scripts/` is not an
interface to reach into, and neither is a `sys.path` a module does not own
(ADR-0149).
"""

from __future__ import annotations

from collections.abc import Collection


def option(rest: list[str], name: str) -> str | None:
    """Return the sole option's value in either spelling, or None where it is not one.

    *rest* is everything one command's operands left over. Anything but this
    flag and its value — a second flag, a stray operand, a different flag — is
    None, which is how an engine tells an unsupported option from its own.
    """

    if len(rest) == 1 and rest[0].startswith(f"{name}="):
        return rest[0].split("=", 1)[1]
    if len(rest) == 2 and rest[0] == name:
        return rest[1]
    return None


def split(
    arguments: list[str], valueless: Collection[str] = ()
) -> tuple[list[str], list[str]]:
    """Separate operands from options whichever order the caller wrote them in.

    Each list keeps the order it was written in, and a separated value stays
    behind the flag it belongs to, so an engine reads the result as though the
    caller had written the one order it prefers.

    Args:
        arguments: One command's arguments, its command path already consumed.
        valueless: The engine's own flags that carry no value. A flag named
            here takes nothing from behind it, so the operand written there is
            still an operand; an engine that has none declares none.
    """

    operands: list[str] = []
    options: list[str] = []
    index = 0
    while index < len(arguments):
        token = arguments[index]
        index += 1
        if not token.startswith("--"):
            operands.append(token)
            continue

        # A separated value belongs to the flag before it and travels with it,
        # unless the engine has declared that this flag carries none.
        options.append(token)
        if "=" not in token and token not in valueless and index < len(arguments):
            options.append(arguments[index])
            index += 1
    return operands, options
