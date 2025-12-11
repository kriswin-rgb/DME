from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass
class BacktestResult:
    total_return: float
    max_drawdown: float
    trades: int


def simple_moving_average_strategy(prices: Sequence[float], fast: int = 5, slow: int = 20) -> BacktestResult:
    if len(prices) < slow:
        return BacktestResult(total_return=0.0, max_drawdown=0.0, trades=0)

    equity = 1.0
    peak_equity = 1.0
    max_drawdown = 0.0
    position = 0
    trades = 0

    for i in range(slow, len(prices)):
        window_fast = prices[i - fast : i]
        window_slow = prices[i - slow : i]
        ma_fast = sum(window_fast) / len(window_fast)
        ma_slow = sum(window_slow) / len(window_slow)

        if ma_fast > ma_slow and position == 0:
            position = 1
            trades += 1
        elif ma_fast < ma_slow and position == 1:
            position = 0
            trades += 1

        if position == 1:
            equity *= prices[i] / prices[i - 1]

        peak_equity = max(peak_equity, equity)
        drawdown = (peak_equity - equity) / peak_equity
        max_drawdown = max(max_drawdown, drawdown)

    total_return = equity - 1.0
    return BacktestResult(total_return=total_return, max_drawdown=max_drawdown, trades=trades)
