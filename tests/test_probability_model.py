import pandas as pd

from probability_model import estimate_bars_to_target, estimate_tp_probability


def make_probability_df(rows=120):
    data = []
    base = 100.0

    for i in range(rows):
        close = base + i * 0.1
        data.append(
            {
                "Close": close,
                "High": close + 0.3,
                "Low": close - 0.3,
                "rsi": 55.0,
                "adx": 25.0,
                "ema20": close - 0.1,
                "ema50": close - 0.2,
                "ema200": close - 0.5,
                "atr": 1.0,
            }
        )

    return pd.DataFrame(data)


def test_estimate_tp_probability_returns_50_for_empty_data():
    df = pd.DataFrame()
    result = estimate_tp_probability(df, entry=100, tp=102, sl=99, direction="BUY")

    assert result == 50.0


def test_estimate_tp_probability_returns_50_for_short_data():
    df = make_probability_df(rows=40)
    result = estimate_tp_probability(df, entry=100, tp=102, sl=99, direction="BUY")

    assert result == 50.0


def test_estimate_tp_probability_returns_zero_for_invalid_distances():
    df = make_probability_df()
    result = estimate_tp_probability(df, entry=100, tp=100, sl=99, direction="BUY")

    assert result == 0.0


def test_estimate_tp_probability_returns_percentage():
    df = make_probability_df()
    result = estimate_tp_probability(df, entry=100, tp=101, sl=99, direction="BUY")

    assert isinstance(result, float)
    assert 0.0 <= result <= 100.0


def test_estimate_bars_to_target_returns_999_when_atr_is_zero():
    assert estimate_bars_to_target(atr=0, reward_distance=2, trend_strength=25) == 999


def test_estimate_bars_to_target_returns_positive_integer():
    result = estimate_bars_to_target(atr=1.0, reward_distance=2.0, trend_strength=25)

    assert isinstance(result, int)
    assert result >= 1
