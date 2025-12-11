import pytest

from services.dme_core_v5.backend.risk_guardrails import check_risk_guardrails, RiskBreach


def test_risk_guardrails_pass():
  metrics = {"max_drawdown": 0.1, "max_leverage": 2.0, "max_single_position_pct": 0.05}
  check_risk_guardrails(metrics)


def test_risk_guardrails_breach():
  metrics = {"max_drawdown": 0.3, "max_leverage": 6.0, "max_single_position_pct": 0.2}
  with pytest.raises(RiskBreach):
    check_risk_guardrails(metrics)
