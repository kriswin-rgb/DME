from services.data_ingest.data_quality_checks import is_timestamp_sane, is_price_sane, validate_candle
from datetime import datetime, timedelta


def test_is_price_sane_basic():
    assert is_price_sane(110, 100)
    assert not is_price_sane(150, 100, threshold=0.2)


def test_is_timestamp_sane_near_now():
    now_ts = datetime.utcnow().timestamp()
    assert is_timestamp_sane(now_ts)


def test_validate_candle_negative_volume():
    ok, reason = validate_candle({"timestamp": datetime.utcnow().timestamp(), "close": 100, "volume": -1})
    assert not ok
    assert "Negative volume" in reason
