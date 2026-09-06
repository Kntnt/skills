"""The one document both sides of the model-selector seam have to agree about."""

from __future__ import annotations

from typing import Any


def select_answer(
    model: str = "the-cheapest",
    deliberation: str | None = "medium",
    **fields: Any,
) -> dict[str, Any]:
    """Provide one complete answer to a `select` call, as the contract states it.

    Written out here rather than produced by running the real engine, so that a
    change to what that engine chooses cannot quietly change what the callers
    of this fixture are testing. What it pins is the shape a caller reads: the
    point, the channel that pays for it, the launch instruction, and the basis
    the answer rests on. A caller overrides any of it by keyword.

    A null *deliberation* is an answer rather than a gap: a model with no
    deliberation control at all comes back naming one point and no level.
    """

    return {
        "ok": True,
        "kind": "implement",
        "model": model,
        "deliberation": deliberation,
        "channel": {
            "provider": "anthropic",
            "pay": "subscription",
            "plan": "Claude Max 20x",
            "harness": "claude-code",
        },
        "launch": {
            "how": "claude-code-agent",
            "subagent_type": (
                f"kntnt-{model}-{deliberation}" if deliberation else f"kntnt-{model}"
            ),
            "command": None,
            "note": None,
        },
        "basis": "measured",
        "confidence": 0.71,
        "expected": {"cost_usd": 0.83, "p_success": 0.93, "tokens": 240000},
        "alternatives": [],
        "attempt_id": f"ms-{model}-{deliberation}" if deliberation else f"ms-{model}",
        "note": None,
    } | fields


def inherit_answer(
    model: str | None = "the-strongest",
    deliberation: str | None = "high",
    note: str = "no configured model is reachable from this harness",
    **fields: Any,
) -> dict[str, Any]:
    """Provide the answer a `select` call degrades to: the caller's own seat.

    The floor of the interface rather than a refusal — there is no status a
    caller may read as *start nothing* — so it names the seat the caller said
    it was calling from and says why nothing was chosen for it.
    """

    return select_answer(
        model=model or "",
        deliberation=deliberation or "",
        launch={"how": "inherit", "subagent_type": None, "command": None, "note": note},
        basis="inherit",
        confidence=0.0,
        expected={"cost_usd": None, "p_success": None, "tokens": None},
        note=note,
        **fields,
    ) | {"model": model, "deliberation": deliberation}
