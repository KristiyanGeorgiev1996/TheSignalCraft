import pandas as pd

from scoring import calculate


def make_tf_data(
    bullish=True,
    atr=0.0020,
    adx=25.0,
    rsi=55.0,
    macd_hist=0.5,
    m15_rsi=55.0,
):
    if bullish:
        ema20, ema50, ema200 = 1.21, 1.20, 1.19
    else:
        ema20, ema50, ema200 = 1.19, 1.20, 1.21
        macd_hist = -abs(macd_hist)

    h1 = pd.DataFrame(
        [
            {
                "Open": 1.2000,
                "High": 1.2100,
                "Low": 1.1900,
                "Close": 1.2050,
                "ema20": ema20,
                "ema50": ema50,
                "ema200": ema200,
                "rsi": rsi,
                "atr": atr,
                "adx": adx,
                "macd_hist": macd_hist,
            }
        ]
        * 100
    )

    m15 = pd.DataFrame(
        [
            {
                "Open": 1.2040,
                "High": 1.2060,
                "Low": 1.2030,
                "Close": 1.2050,
                "ema20": 1.2050,
                "rsi": m15_rsi,
            }
        ]
        * 20
    )

    h4 = pd.DataFrame(
        [
            {
                "Open": 1.2000,
                "High": 1.2150,
                "Low": 1.1900,
                "Close": 1.2050,
                "ema20": ema20,
                "ema50": ema50,
                "ema200": ema200,
                "rsi": rsi,
                "atr": atr,
                "adx": adx,
                "macd_hist": macd_hist,
            }
        ]
        * 30
    )

    return {"1h": h1, "15m": m15, "4h": h4}


def test_calculate_rejects_invalid_buy_price_order():
    signal = {
        "pair": "GBPUSD",
        "direction": "BUY",
        "entry": 1.2000,
        "tp": 1.1900,
        "sl": 1.2100,
    }
    tf_data = make_tf_data()

    result = calculate(signal, tf_data)

    assert result["decision"] == "REJECT"
    assert result["score"] == 0
    assert any("BUY setup has invalid price order" in msg for msg in result["blockers"])


def test_calculate_rejects_invalid_sell_price_order():
    signal = {
        "pair": "GBPUSD",
        "direction": "SELL",
        "entry": 1.2000,
        "tp": 1.2100,
        "sl": 1.1900,
    }
    tf_data = make_tf_data(bullish=False)

    result = calculate(signal, tf_data)

    assert result["decision"] == "REJECT"
    assert result["score"] == 0
    assert any("SELL setup has invalid price order" in msg for msg in result["blockers"])


def test_calculate_returns_expected_result_shape():
    signal = {
        "pair": "GBPUSD",
        "direction": "BUY",
        "entry": 1.2040,
        "tp": 1.2080,
        "sl": 1.2010,
    }
    tf_data = make_tf_data()

    result = calculate(signal, tf_data)

    expected_keys = {
        "score",
        "decision",
        "notes",
        "blockers",
        "rr",
        "atr",
        "probability",
        "estimated_bars",
        "framework",
        "profile_name",
        "category",
    }

    assert expected_keys.issubset(result.keys())


def test_calculate_decision_is_valid():
    signal = {
        "pair": "GBPUSD",
        "direction": "BUY",
        "entry": 1.2040,
        "tp": 1.2080,
        "sl": 1.2010,
    }
    tf_data = make_tf_data()

    result = calculate(signal, tf_data)

    assert result["decision"] in {"REJECT", "RISKY", "ACCEPT", "STRONG TRADE"}


def test_calculate_returns_non_negative_score():
    signal = {
        "pair": "EURUSD",
        "direction": "BUY",
        "entry": 1.2040,
        "tp": 1.2080,
        "sl": 1.2010,
    }
    tf_data = make_tf_data()

    result = calculate(signal, tf_data)

    assert 0 <= result["score"] <= 100
