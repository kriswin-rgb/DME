from __future__ import annotations

from typing import Mapping


class RiskBreach(Exception):
    """Raised when portfolio risk metrics breach configured guardrails."""


DEFAULT_LIMITS = {
    "max_drawdown": 0.25,
    "max_leverage": 5.0,
    "max_single_position_pct": 0.1,
}


def check_risk_guardrails(metrics: Mapping[str, float], limits: Mapping[str, float] | None = None) -> None:
    limits = limits or DEFAULT_LIMITS
    breaches: list[str] = []

    if metrics.get("max_drawdown", 0.0) > limits["max_drawdown"]:
        breaches.append("max_drawdown")
    if metrics.get("max_leverage", 0.0) > limits["max_leverage"]:
        breaches.append("max_leverage")
    if metrics.get("max_single_position_pct", 0.0) > limits["max_single_position_pct"]:
        breaches.append("max_single_position_pct")

    if breaches:
        raise RiskBreach(", ".join(breaches))
