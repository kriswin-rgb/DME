from services.dme_core_v5.backend.backtest_service import simple_moving_average_strategy


def test_backtest_returns_reasonable_result():
    prices = [100 + i for i in range(50)]
    result = simple_moving_average_strategy(prices)
    assert result.trades >= 0
    assert -1.0 <= result.max_drawdown <= 1.0
