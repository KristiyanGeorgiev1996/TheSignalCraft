import pytest

from signal_parser import parse_signal


def test_parse_valid_buy_signal():
    result = parse_signal("/signal GBPUSD BUY 1.2750 1.2820 1.2700")

    assert result["pair"] == "GBPUSD"
    assert result["direction"] == "BUY"
    assert result["entry"] == 1.2750
    assert result["tp"] == 1.2820
    assert result["sl"] == 1.2700


def test_parse_valid_sell_signal():
    result = parse_signal("/signal EURCHF SELL 0.9206 0.9146 0.9226")

    assert result["pair"] == "EURCHF"
    assert result["direction"] == "SELL"
    assert result["entry"] == 0.9206
    assert result["tp"] == 0.9146
    assert result["sl"] == 0.9226


def test_parse_signal_accepts_comma_decimal_separator():
    result = parse_signal("/signal GBPUSD BUY 1,2750 1,2820 1,2700")

    assert result["entry"] == 1.2750
    assert result["tp"] == 1.2820
    assert result["sl"] == 1.2700


def test_parse_signal_rejects_wrong_command():
    with pytest.raises(ValueError, match="Command must start with /signal"):
        parse_signal("/start GBPUSD BUY 1.2750 1.2820 1.2700")


def test_parse_signal_rejects_invalid_direction():
    with pytest.raises(ValueError, match="Direction must be BUY or SELL"):
        parse_signal("/signal GBPUSD LONG 1.2750 1.2820 1.2700")


def test_parse_signal_rejects_missing_parts():
    with pytest.raises(ValueError, match="Expected format"):
        parse_signal("/signal GBPUSD BUY 1.2750 1.2820")


def test_parse_signal_rejects_non_numeric_prices():
    with pytest.raises(ValueError):
        parse_signal("/signal GBPUSD BUY entry 1.2820 1.2700")
