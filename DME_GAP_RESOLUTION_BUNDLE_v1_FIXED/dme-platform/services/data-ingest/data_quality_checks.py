from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple


def validate_candle(candle: Dict, prior_candle: Optional[Dict] = None) -> Tuple[bool, str]:
    if not is_timestamp_sane(candle.get("timestamp")):
        return False, "Timestamp out of acceptable range"

    if prior_candle is not None:
        if not is_price_sane(float(candle["close"]), float(prior_candle["close"])):
            return False, "Price deviation exceeds threshold"

    if float(candle.get("volume", 0)) < 0:
        return False, "Negative volume"

    return True, ""


def is_timestamp_sane(ts: int | float | None) -> bool:
    if ts is None:
        return False
    now = datetime.utcnow()
    ts_dt = datetime.utcfromtimestamp(ts)
    return abs((now - ts_dt).total_seconds()) <= 5.0


def is_price_sane(current: float, prior: float, threshold: float = 0.20) -> bool:
    if prior <= 0:
        return True
    change = abs(current - prior) / prior
    return change <= threshold
