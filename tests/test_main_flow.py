import pandas as pd
import pytest

import main


class DummyMessage:
    def __init__(self, text):
        self.text = text
        self.sent_messages = []

    async def reply_text(self, text):
        self.sent_messages.append(text)


class DummyUpdate:
    def __init__(self, text):
        self.message = DummyMessage(text)


class DummyContext:
    pass


def make_df():
    return pd.DataFrame(
        [
            {
                "Open": 1.2000,
                "High": 1.2100,
                "Low": 1.1900,
                "Close": 1.2050,
                "Volume": 1000,
                "ema20": 1.2040,
                "ema50": 1.2030,
                "ema200": 1.2000,
                "rsi": 55.0,
                "atr": 0.0020,
                "adx": 25.0,
                "macd": 0.1,
                "macd_signal": 0.05,
                "macd_hist": 0.05,
                "bb_high": 1.2100,
                "bb_low": 1.1900,
                "bb_width": 0.0200,
                "vol_sma20": 1000,
            }
        ]
    )


@pytest.mark.asyncio
async def test_signal_handler_success(monkeypatch):
    update = DummyUpdate("/signal GBPUSD BUY 1.2750 1.2820 1.2700")
    context = DummyContext()

    monkeypatch.setattr(
        main,
        "parse_signal",
        lambda text: {
            "pair": "GBPUSD",
            "direction": "BUY",
            "entry": 1.2750,
            "tp": 1.2820,
            "sl": 1.2700,
        },
    )

    monkeypatch.setattr(
        main,
        "get_data",
        lambda pair: {"1h": make_df(), "15m": make_df(), "4h": make_df()},
    )

    monkeypatch.setattr(main, "_decorate_timeframes", lambda raw: raw)

    monkeypatch.setattr(
        main,
        "calculate",
        lambda signal_data, tf_data: {
            "framework": "1H master / 4H filter / 15m timing / profile=forex_major",
            "profile_name": "forex_major",
            "category": "forex_major",
            "atr": 0.002,
            "rr": 1.4,
            "probability": 61.5,
            "estimated_bars": 5,
            "score": 72,
            "decision": "ACCEPT",
            "notes": ["1H trend structure aligns with the signal"],
            "blockers": ["15m timing is acceptable"],
        },
    )

    monkeypatch.setattr(main, "log_signal", lambda signal_data, result: None)

    await main.signal(update, context)

    assert len(update.message.sent_messages) == 1
    response = update.message.sent_messages[0]
    assert "Signal Analysis" in response
    assert "Pair: GBPUSD" in response
    assert "Decision: ACCEPT" in response


@pytest.mark.asyncio
async def test_signal_handler_handles_parser_error(monkeypatch):
    update = DummyUpdate("/signal BAD")
    context = DummyContext()

    def fake_parse(_):
        raise ValueError("Expected format: /signal PAIR DIRECTION ENTRY TP SL")

    monkeypatch.setattr(main, "parse_signal", fake_parse)

    await main.signal(update, context)

    assert len(update.message.sent_messages) == 1
    assert "Signal format error" in update.message.sent_messages[0]


@pytest.mark.asyncio
async def test_signal_handler_handles_missing_market_data(monkeypatch):
    update = DummyUpdate("/signal GBPUSD BUY 1.2750 1.2820 1.2700")
    context = DummyContext()

    monkeypatch.setattr(
        main,
        "parse_signal",
        lambda text: {
            "pair": "GBPUSD",
            "direction": "BUY",
            "entry": 1.2750,
            "tp": 1.2820,
            "sl": 1.2700,
        },
    )

    monkeypatch.setattr(
        main,
        "get_data",
        lambda pair: {"1h": pd.DataFrame(), "15m": pd.DataFrame(), "4h": pd.DataFrame()},
    )

    await main.signal(update, context)

    assert len(update.message.sent_messages) == 1
    assert "No market data found" in update.message.sent_messages[0]
