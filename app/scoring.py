from __future__ import annotations

from instrument_profiles import get_instrument_profile
from probability_model import estimate_tp_probability, estimate_bars_to_target


MAX_SCORE = 100


def _is_bullish(last) -> bool:
    return bool(last["ema20"] > last["ema50"] > last["ema200"])


def _is_bearish(last) -> bool:
    return bool(last["ema20"] < last["ema50"] < last["ema200"])


def _aligned(direction: str, bullish: bool, bearish: bool) -> bool:
    return (direction == "BUY" and bullish) or (direction == "SELL" and bearish)


def _trend_points(last, direction: str, label: str, strong_points: int, weak_points: int):
    bullish = _is_bullish(last)
    bearish = _is_bearish(last)

    if _aligned(direction, bullish, bearish):
        return strong_points, f"{label} trend structure aligns with the signal"

    if (direction == "BUY" and last["ema50"] > last["ema200"]) or (
        direction == "SELL" and last["ema50"] < last["ema200"]
    ):
        return weak_points, f"{label} trend is supportive but not fully stacked"

    return 0, f"{label} trend is not aligned"


def calculate(signal: dict, tf_data: dict):
    h1 = tf_data["1h"]
    m15 = tf_data["15m"]
    h4 = tf_data["4h"]

    instrument = signal["pair"]
    profile = get_instrument_profile(instrument)

    last_h1 = h1.iloc[-1]
    last_m15 = m15.iloc[-1] if not m15.empty else last_h1
    last_h4 = h4.iloc[-1] if not h4.empty else last_h1

    entry = signal["entry"]
    tp = signal["tp"]
    sl = signal["sl"]
    direction = signal["direction"]

    risk = abs(entry - sl)
    reward = abs(tp - entry)
    rr = reward / risk if risk else 0.0
    atr = float(last_h1["atr"])

    score = 0
    notes: list[str] = []
    blockers: list[str] = []
    hard_reject_reasons: list[str] = []

    if direction == "BUY" and not (sl < entry < tp):
        hard_reject_reasons.append("BUY setup has invalid price order: SL < Entry < TP is required")
    if direction == "SELL" and not (tp < entry < sl):
        hard_reject_reasons.append("SELL setup has invalid price order: TP < Entry < SL is required")
    if risk <= 0 or reward <= 0:
        hard_reject_reasons.append("Risk and reward distances must both be positive")

    if hard_reject_reasons:
        return {
            "score": 0,
            "decision": "REJECT",
            "notes": notes,
            "blockers": hard_reject_reasons,
            "rr": rr,
            "atr": atr,
            "probability": 0.0,
            "estimated_bars": 999,
            "framework": f"1H master / 4H filter / 15m timing / profile={profile['category']}",
            "profile_name": profile["name"],
            "category": profile["category"],
        }

    h4_bull = bool(last_h4["ema50"] > last_h4["ema200"])
    h4_bear = bool(last_h4["ema50"] < last_h4["ema200"])
    h1_bull = _is_bullish(last_h1)
    h1_bear = _is_bearish(last_h1)

    if _aligned(direction, h4_bull, h4_bear):
        score += profile["h4_trend_points"]
        notes.append("4H context confirms the signal direction")
    elif _aligned(direction, h1_bull, h1_bear):
        blockers.append("4H context is not ideal, but 1H still has local alignment")
    else:
        hard_reject_reasons.append("Both 4H context and 1H structure are against the signal")

    pts, note = _trend_points(
        last_h1,
        direction,
        "1H",
        profile["h1_trend_points_strong"],
        profile["h1_trend_points_weak"],
    )
    score += pts
    (notes if pts else blockers).append(note)

    adx = float(last_h1["adx"])
    if adx >= profile["adx_good"]:
        score += profile["adx_points_good"]
        notes.append(f"1H trend strength is good (ADX {adx:.1f})")
    elif adx >= profile["adx_ok"]:
        score += profile["adx_points_ok"]
        notes.append(f"1H trend strength is usable (ADX {adx:.1f})")
    else:
        blockers.append(f"1H trend is weak for {profile['category']} (ADX {adx:.1f})")

    rsi = float(last_h1["rsi"])
    if direction == "BUY" and profile["buy_rsi_good_min"] <= rsi <= profile["buy_rsi_good_max"]:
        score += 10
        notes.append(f"1H RSI is supportive for BUY ({rsi:.1f})")
    elif direction == "SELL" and profile["sell_rsi_good_min"] <= rsi <= profile["sell_rsi_good_max"]:
        score += 10
        notes.append(f"1H RSI is supportive for SELL ({rsi:.1f})")
    elif direction == "BUY" and rsi > profile["buy_rsi_overbought"]:
        blockers.append(f"1H RSI looks overbought for {profile['category']} ({rsi:.1f})")
    elif direction == "SELL" and rsi < profile["sell_rsi_oversold"]:
        blockers.append(f"1H RSI looks oversold for {profile['category']} ({rsi:.1f})")
    else:
        blockers.append(f"1H RSI regime is not ideal ({rsi:.1f})")

    macd_hist = float(last_h1["macd_hist"])
    if direction == "BUY" and macd_hist > 0:
        score += 9
        notes.append("1H MACD momentum supports BUY")
    elif direction == "SELL" and macd_hist < 0:
        score += 9
        notes.append("1H MACD momentum supports SELL")
    else:
        blockers.append("1H MACD momentum is not aligned")

    m15_rsi = float(last_m15["rsi"])
    entry_gap = abs(entry - float(last_m15["ema20"]))

    if entry_gap <= atr * profile["timing_gap_good_atr_mult"]:
        score += profile["timing_points_good"]
        notes.append("15m timing is tight, entry is near the short-term mean")
    elif entry_gap <= atr * profile["timing_gap_ok_atr_mult"]:
        score += profile["timing_points_ok"]
        notes.append("15m timing is acceptable")
    else:
        blockers.append("15m timing looks late / stretched")

    if direction == "BUY" and m15_rsi >= profile["m15_buy_exhaustion_rsi"]:
        blockers.append(f"15m shows short-term exhaustion on BUY ({m15_rsi:.1f})")
    elif direction == "SELL" and m15_rsi <= profile["m15_sell_exhaustion_rsi"]:
        blockers.append(f"15m shows short-term exhaustion on SELL ({m15_rsi:.1f})")
    else:
        score += profile["timing_no_exhaustion_points"]
        notes.append("15m does not show extreme exhaustion")

    sl_atr = risk / atr if atr else 999
    if profile["sl_atr_good_min"] <= sl_atr <= profile["sl_atr_good_max"]:
        score += profile["sl_points_good"]
        notes.append(f"SL distance is realistic ({sl_atr:.2f} ATR)")
    elif profile["sl_atr_ok_min"] <= sl_atr <= profile["sl_atr_ok_max"]:
        score += profile["sl_points_ok"]
        notes.append(f"SL distance is usable ({sl_atr:.2f} ATR)")
    else:
        blockers.append(f"SL distance is poor relative to 1H ATR ({sl_atr:.2f} ATR)")

    tp_atr = reward / atr if atr else 999
    if profile["tp_atr_good_min"] <= tp_atr <= profile["tp_atr_good_max"]:
        score += profile["tp_points_good"]
        notes.append(f"TP distance is realistic ({tp_atr:.2f} ATR)")
    elif tp_atr <= profile["tp_atr_ok_max"]:
        score += profile["tp_points_ok"]
        notes.append(f"TP distance is borderline but possible ({tp_atr:.2f} ATR)")
    else:
        blockers.append(f"TP is too ambitious for {profile['category']} ({tp_atr:.2f} ATR)")

    if rr >= profile["rr_good"]:
        score += profile["rr_points_good"]
        notes.append(f"Risk/reward is solid ({rr:.2f})")
    elif rr >= profile["rr_ok"]:
        score += profile["rr_points_ok"]
        notes.append(f"Risk/reward is acceptable ({rr:.2f})")
    else:
        blockers.append(f"Risk/reward is too weak ({rr:.2f})")

    recent_high = float(h1["High"].tail(72).max())
    recent_low = float(h1["Low"].tail(72).min())
    room = (recent_high - entry) if direction == "BUY" else (entry - recent_low)

    if room >= reward:
        score += profile["room_points_good"]
        notes.append("1H structure leaves enough room to target")
    elif room >= reward * profile["room_ok_ratio"]:
        score += profile["room_points_ok"]
        notes.append("1H structure room is borderline")
    else:
        blockers.append("Nearby 1H structure may block the target")

    probability = estimate_tp_probability(h1, entry, tp, sl, direction, max_bars=10)
    if probability >= profile["prob_good"]:
        score += profile["prob_points_good"]
        notes.append(f"H1 historical analogs support the trade ({probability:.1f}%)")
    elif probability >= profile["prob_ok"]:
        score += profile["prob_points_ok"]
        notes.append(f"H1 analog probability is neutral ({probability:.1f}%)")
    else:
        blockers.append(f"H1 analog probability is weak ({probability:.1f}%)")

    estimated_bars = estimate_bars_to_target(atr, reward, adx)
    if estimated_bars <= profile["bars_good_max"]:
        score += profile["bars_points_good"]
        notes.append(f"Expected duration is good (~{estimated_bars} H1 bars)")
    elif estimated_bars <= profile["bars_ok_max"]:
        score += profile["bars_points_ok"]
        notes.append(f"Expected duration is acceptable (~{estimated_bars} H1 bars)")
    elif estimated_bars <= profile["bars_warn_max"]:
        blockers.append(f"Trade may take a while (~{estimated_bars} H1 bars)")
    else:
        hard_reject_reasons.append(
            f"Trade is likely too slow for {profile['category']} (~{estimated_bars} H1 bars)"
        )

    if hard_reject_reasons:
        return {
            "score": min(score, MAX_SCORE),
            "decision": "REJECT",
            "notes": notes,
            "blockers": blockers + hard_reject_reasons,
            "rr": rr,
            "atr": atr,
            "probability": probability,
            "estimated_bars": estimated_bars,
            "framework": f"1H master / 4H filter / 15m timing / profile={profile['category']}",
            "profile_name": profile["name"],
            "category": profile["category"],
        }

    if len(blockers) >= profile["hard_reject_blockers_count"] or score < profile["reject_score_below"]:
        decision = "REJECT"
    elif score < profile["risky_score_below"]:
        decision = "RISKY"
    elif score < profile["accept_score_below"]:
        decision = "ACCEPT"
    else:
        decision = "STRONG TRADE"

    return {
        "score": min(score, MAX_SCORE),
        "decision": decision,
        "notes": notes,
        "blockers": blockers,
        "rr": rr,
        "atr": atr,
        "probability": probability,
        "estimated_bars": estimated_bars,
        "framework": f"1H master / 4H filter / 15m timing / profile={profile['category']}",
        "profile_name": profile["name"],
        "category": profile["category"],
    }
