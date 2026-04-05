from __future__ import annotations

import math
import pandas as pd


def estimate_tp_probability(
    data: pd.DataFrame,
    entry: float,
    tp: float,
    sl: float,
    direction: str,
    max_bars: int = 12,
) -> float:
    """Estimate whether TP is hit before SL using historical analog candles.

    This is still heuristic, not a real predictive model. It compares the current
    setup to past bars with similar trend, RSI and ATR conditions and checks what
    happened in the next `max_bars` candles.
    """
    if data.empty or len(data) < 80:
        return 50.0

    df = data.copy().dropna().reset_index(drop=True)
    last = df.iloc[-1]
    risk = abs(entry - sl)
    reward = abs(tp - entry)
    if risk <= 0 or reward <= 0:
        return 0.0

    outcomes: list[int] = []
    direction = direction.upper()

    for i in range(50, len(df) - max_bars - 1):
        row = df.iloc[i]
        # Similarity gates around the current setup
        rsi_ok = abs(row["rsi"] - last["rsi"]) <= 8
        adx_ok = abs(row["adx"] - last["adx"]) <= 7
        trend_now = row["ema50"] > row["ema200"]
        trend_last = last["ema50"] > last["ema200"]
        trend_ok = trend_now == trend_last
        stretch_ok = abs((row["Close"] - row["ema20"])) <= max(last["atr"] * 1.2, 1e-9)

        if not (rsi_ok and adx_ok and trend_ok and stretch_ok):
            continue

        simulated_entry = float(row["Close"])
        if direction == "BUY":
            sim_tp = simulated_entry + reward
            sim_sl = simulated_entry - risk
        else:
            sim_tp = simulated_entry - reward
            sim_sl = simulated_entry + risk

        result = 0
        for j in range(1, max_bars + 1):
            future = df.iloc[i + j]
            hi = float(future["High"])
            lo = float(future["Low"])
            if direction == "BUY":
                if hi >= sim_tp:
                    result = 1
                    break
                if lo <= sim_sl:
                    result = -1
                    break
            else:
                if lo <= sim_tp:
                    result = 1
                    break
                if hi >= sim_sl:
                    result = -1
                    break
        if result != 0:
            outcomes.append(result)

    if len(outcomes) < 8:
        return 50.0

    wins = sum(1 for x in outcomes if x == 1)
    probability = wins / len(outcomes) * 100
    return round(probability, 2)


def estimate_bars_to_target(atr: float, reward_distance: float, trend_strength: float) -> int:
    if atr <= 0:
        return 999
    speed_factor = max(0.7, min(1.8, trend_strength / 20 if trend_strength else 1.0))
    bars = math.ceil(reward_distance / max(atr * 0.55 * speed_factor, 1e-9))
    return max(1, bars)
