import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Tuple

from sqlalchemy import func

from .db import SessionLocal
from .models import PortfolioSnapshot, StrategyTradeLog

logger = logging.getLogger("dme_portfolio_analytics")


def _compute_equity_curve(points: Iterable[float]) -> Tuple[float, List[float]]:
    """Return (max_drawdown, equity_curve) for a sequence of PnL values."""
    equity_curve: List[float] = []
    peak = None
    cumulative = 0.0
    max_dd = 0.0

    for pnl in points:
        cumulative += pnl
        equity_curve.append(cumulative)
        if peak is None or cumulative > peak:
            peak = cumulative
        if peak and peak != 0:
            dd = (cumulative - peak) / peak
            if dd < max_dd:
                max_dd = dd

    return max_dd, equity_curve


def compute_portfolio_snapshot(lookback_days: int = 30) -> Dict[str, Any]:
    """Compute and persist a portfolio-level snapshot from strategy_trade_log.

    Designed to be run periodically (e.g. hourly or daily) via a scheduler or n8n.
    """
    session = SessionLocal()
    try:
        since = datetime.utcnow() - timedelta(days=lookback_days)

        results = (
            session.query(
                StrategyTradeLog.strategy_id,
                StrategyTradeLog.strategy_version,
                func.count(StrategyTradeLog.id).label("trades"),
                func.sum(StrategyTradeLog.realized_pnl).label("realized_pnl"),
            )
            .filter(StrategyTradeLog.filled_at >= since)
            .group_by(StrategyTradeLog.strategy_id, StrategyTradeLog.strategy_version)
            .all()
        )

        per_strategy: List[Dict[str, Any]] = []
        pnl_points: List[float] = []

        for strategy_id, version, trades, pnl in results:
            pnl_val = float(pnl or 0.0)
            pnl_points.append(pnl_val)
            per_strategy.append(
                {
                    "strategy_id": strategy_id,
                    "strategy_version": version,
                    "trades": int(trades or 0),
                    "realized_pnl": pnl_val,
                }
            )

        max_dd, equity_curve = _compute_equity_curve(pnl_points)
        total_pnl = float(sum(pnl_points))

        payload: Dict[str, Any] = {
            "as_of": datetime.utcnow().isoformat(),
            "lookback_days": lookback_days,
            "total_realized_pnl": total_pnl,
            "max_drawdown": max_dd,
            "per_strategy": per_strategy,
            "equity_curve": equity_curve,
        }

        snapshot = PortfolioSnapshot(
            as_of=datetime.utcnow(),
            lookback_days=lookback_days,
            total_realized_pnl=total_pnl,
            max_drawdown=max_dd,
            num_strategies=len(per_strategy),
            json_payload=json.dumps(payload),
        )
        session.add(snapshot)
        session.commit()
        logger.info(
            "Portfolio snapshot created: %d strategies, PnL=%f, DD=%f",
            snapshot.num_strategies,
            snapshot.total_realized_pnl,
            snapshot.max_drawdown,
        )
        return payload
    finally:
        session.close()


if __name__ == "__main__":
    compute_portfolio_snapshot()
