from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Any

import requests  # type: ignore

from .data_quality_checks import validate_candle


class OandaIngestor:
    """HTTP-based ingestor for Oanda candles (template)."""

    def __init__(self, api_key: str, account_id: str, base_url: str = "https://api-fxtrade.oanda.com/v3"):
        self.api_key = api_key
        self.account_id = account_id
        self.base_url = base_url

    def fetch_candles(self, instrument: str, granularity: str = "H1", count: int = 100) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/instruments/{instrument}/candles"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"granularity": granularity, "count": count, "price": "M"}
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        candles: List[Dict] = []
        prior = None
        for c in resp.json().get("candles", []):
            mid = c["mid"]
            candle = {
                "timestamp": datetime.fromisoformat(c["time"].replace("Z", "+00:00")).timestamp(),
                "open": float(mid["o"]),
                "high": float(mid["h"]),
                "low": float(mid["l"]),
                "close": float(mid["c"]),
                "volume": float(c.get("volume", 0)),
            }
            valid, reason = validate_candle(candle, prior)
            if not valid:
                print("Invalid Oanda candle skipped:", reason)
                continue
            candles.append(candle)
            prior = candle
        return candles
