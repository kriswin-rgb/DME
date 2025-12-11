from __future__ import annotations

import asyncio
import json
from typing import Dict, List

import websockets  # type: ignore

from .data_quality_checks import validate_candle


class BinanceIngestor:
    """Real-time Binance OHLCV WebSocket ingestor (template)."""

    def __init__(self, symbols: List[str], db_conn):
        self.symbols = symbols
        self.db = db_conn
        self.ws_url = "wss://stream.binance.com:9443/ws"

    async def connect(self) -> None:
        stream = "/".join(f"{s.lower()}@kline_1h" for s in self.symbols)
        url = f"{self.ws_url}/{stream}"
        while True:
            try:
                async with websockets.connect(url) as ws:
                    async for message in ws:
                        await self.process_message(json.loads(message))
            except Exception as exc:  # pragma: no cover - network errors
                print("BinanceIngestor error, reconnecting:", exc)
                await asyncio.sleep(5)

    async def process_message(self, msg: Dict) -> None:
        k = msg.get("k", {})
        candle = {
            "timestamp": k.get("T", 0) / 1000,
            "open": float(k.get("o", 0)),
            "high": float(k.get("h", 0)),
            "low": float(k.get("l", 0)),
            "close": float(k.get("c", 0)),
            "volume": float(k.get("v", 0)),
        }
        ok, reason = validate_candle(candle)
        if not ok:
            print("Invalid candle, sending to DLQ:", reason)
            return
        # Persist to DB here using self.db
        # self.db.write_candle('BINANCE', candle)
        print("Valid candle received for Binance symbol", k.get("s"))
