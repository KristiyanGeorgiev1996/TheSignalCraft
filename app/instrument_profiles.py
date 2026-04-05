from __future__ import annotations

from copy import deepcopy


INSTRUMENT_CATEGORIES = {
    # Forex majors
    "EURUSD": "forex_major",
    "GBPUSD": "forex_major",
    "AUDUSD": "forex_major",
    "NZDUSD": "forex_major",
    "USDCHF": "forex_major",
    "USDCAD": "forex_major",

    # Forex crosses
    "AUDJPY": "forex_cross",
    "CADJPY": "forex_cross",
    "GBPJPY": "forex_cross",
    "GBPCAD": "forex_cross",
    "GBPAUD": "forex_cross",
    "AUDCAD": "forex_cross",
    "EURAUD": "forex_cross",

    # Metals
    "XAUUSD": "metals",
    "XAGUSD": "metals",
    "COPPER": "metals",

    # Energy
    "NATURALGAS": "energy",

    # Indices
    "US500": "indices",
    "US30": "indices",
    "NAS100": "indices",
    "UK100": "indices",

    # Crypto
    "BTCUSD": "crypto",
    "ETHUSD": "crypto",
    "SOLUSD": "crypto",
    "AVAXUSD": "crypto",
    "XRPUSD": "crypto",
    "ATOMUSD": "crypto",
    "BCHUSD": "crypto",
}


DEFAULT_PROFILE = {
    "name": "default",

    "h4_trend_points": 14,
    "h1_trend_points_strong": 24,
    "h1_trend_points_weak": 10,

    "adx_good": 22,
    "adx_ok": 18,
    "adx_points_good": 12,
    "adx_points_ok": 7,

    "buy_rsi_good_min": 48,
    "buy_rsi_good_max": 67,
    "buy_rsi_overbought": 72,

    "sell_rsi_good_min": 33,
    "sell_rsi_good_max": 52,
    "sell_rsi_oversold": 28,

    "timing_gap_good_atr_mult": 0.55,
    "timing_gap_ok_atr_mult": 0.95,
    "timing_points_good": 6,
    "timing_points_ok": 3,
    "timing_no_exhaustion_points": 3,
    "m15_buy_exhaustion_rsi": 76,
    "m15_sell_exhaustion_rsi": 24,

    "sl_atr_good_min": 0.7,
    "sl_atr_good_max": 1.6,
    "sl_atr_ok_min": 0.5,
    "sl_atr_ok_max": 2.0,
    "sl_points_good": 8,
    "sl_points_ok": 4,

    "tp_atr_good_min": 0.9,
    "tp_atr_good_max": 2.4,
    "tp_atr_ok_max": 3.0,
    "tp_points_good": 7,
    "tp_points_ok": 3,

    "rr_good": 1.5,
    "rr_ok": 1.25,
    "rr_points_good": 8,
    "rr_points_ok": 4,

    "room_points_good": 5,
    "room_points_ok": 2,
    "room_ok_ratio": 0.75,

    "prob_good": 64,
    "prob_ok": 56,
    "prob_points_good": 8,
    "prob_points_ok": 4,

    "bars_good_max": 6,
    "bars_ok_max": 9,
    "bars_warn_max": 12,
    "bars_points_good": 6,
    "bars_points_ok": 3,

    "reject_score_below": 42,
    "risky_score_below": 58,
    "accept_score_below": 74,
    "hard_reject_blockers_count": 5,
}


CATEGORY_PROFILES = {
    "forex_major": {
        "name": "forex_major",
        "adx_good": 21,
        "adx_ok": 17,
        "tp_atr_good_max": 2.3,
        "tp_atr_ok_max": 2.8,
        "bars_good_max": 6,
        "bars_ok_max": 9,
        "bars_warn_max": 11,
        "reject_score_below": 42,
        "risky_score_below": 58,
        "accept_score_below": 74,
    },
    "forex_cross": {
        "name": "forex_cross",
        "adx_good": 23,
        "adx_ok": 18,
        "sl_atr_good_max": 1.8,
        "sl_atr_ok_max": 2.2,
        "tp_atr_good_max": 2.6,
        "tp_atr_ok_max": 3.1,
        "timing_gap_good_atr_mult": 0.60,
        "timing_gap_ok_atr_mult": 1.00,
        "bars_good_max": 7,
        "bars_ok_max": 10,
        "bars_warn_max": 12,
    },
    "metals": {
        "name": "metals",
        "adx_good": 24,
        "adx_ok": 19,
        "buy_rsi_good_min": 50,
        "buy_rsi_good_max": 70,
        "buy_rsi_overbought": 76,
        "sell_rsi_good_min": 30,
        "sell_rsi_good_max": 50,
        "sell_rsi_oversold": 24,
        "timing_gap_good_atr_mult": 0.70,
        "timing_gap_ok_atr_mult": 1.10,
        "m15_buy_exhaustion_rsi": 80,
        "m15_sell_exhaustion_rsi": 20,
        "sl_atr_good_max": 1.9,
        "sl_atr_ok_max": 2.4,
        "tp_atr_good_max": 3.0,
        "tp_atr_ok_max": 3.6,
        "rr_good": 1.4,
        "rr_ok": 1.2,
        "bars_good_max": 7,
        "bars_ok_max": 10,
        "bars_warn_max": 13,
        "reject_score_below": 40,
        "risky_score_below": 56,
        "accept_score_below": 72,
    },
    "indices": {
        "name": "indices",
        "adx_good": 20,
        "adx_ok": 16,
        "buy_rsi_good_min": 50,
        "buy_rsi_good_max": 69,
        "buy_rsi_overbought": 77,
        "sell_rsi_good_min": 31,
        "sell_rsi_good_max": 50,
        "sell_rsi_oversold": 23,
        "timing_gap_good_atr_mult": 0.75,
        "timing_gap_ok_atr_mult": 1.20,
        "m15_buy_exhaustion_rsi": 81,
        "m15_sell_exhaustion_rsi": 19,
        "sl_atr_good_max": 2.0,
        "sl_atr_ok_max": 2.6,
        "tp_atr_good_max": 3.2,
        "tp_atr_ok_max": 4.0,
        "rr_good": 1.35,
        "rr_ok": 1.15,
        "bars_good_max": 6,
        "bars_ok_max": 9,
        "bars_warn_max": 11,
        "reject_score_below": 39,
        "risky_score_below": 55,
        "accept_score_below": 71,
    },
    "crypto": {
        "name": "crypto",
        "adx_good": 19,
        "adx_ok": 15,
        "buy_rsi_good_min": 47,
        "buy_rsi_good_max": 72,
        "buy_rsi_overbought": 80,
        "sell_rsi_good_min": 28,
        "sell_rsi_good_max": 53,
        "sell_rsi_oversold": 20,
        "timing_gap_good_atr_mult": 0.85,
        "timing_gap_ok_atr_mult": 1.30,
        "m15_buy_exhaustion_rsi": 83,
        "m15_sell_exhaustion_rsi": 17,
        "sl_atr_good_max": 2.2,
        "sl_atr_ok_max": 2.8,
        "tp_atr_good_max": 3.8,
        "tp_atr_ok_max": 4.8,
        "rr_good": 1.3,
        "rr_ok": 1.1,
        "bars_good_max": 8,
        "bars_ok_max": 11,
        "bars_warn_max": 14,
        "reject_score_below": 38,
        "risky_score_below": 54,
        "accept_score_below": 70,
    },
    "energy": {
        "name": "energy",
        "adx_good": 24,
        "adx_ok": 19,
        "timing_gap_good_atr_mult": 0.75,
        "timing_gap_ok_atr_mult": 1.20,
        "m15_buy_exhaustion_rsi": 80,
        "m15_sell_exhaustion_rsi": 20,
        "sl_atr_good_max": 2.1,
        "sl_atr_ok_max": 2.7,
        "tp_atr_good_max": 3.4,
        "tp_atr_ok_max": 4.2,
        "rr_good": 1.35,
        "rr_ok": 1.15,
        "bars_good_max": 7,
        "bars_ok_max": 10,
        "bars_warn_max": 13,
        "reject_score_below": 39,
        "risky_score_below": 55,
        "accept_score_below": 71,
    },
}


INSTRUMENT_OVERRIDES = {
    "XAUUSD": {
        "name": "xauusd",
        "adx_good": 25,
        "adx_ok": 20,
        "tp_atr_good_max": 3.2,
        "tp_atr_ok_max": 3.9,
        "sl_atr_good_max": 2.0,
        "sl_atr_ok_max": 2.5,
        "bars_good_max": 7,
        "bars_ok_max": 10,
        "bars_warn_max": 13,
    },
    "XAGUSD": {
        "name": "xagusd",
        "adx_good": 24,
        "adx_ok": 19,
        "tp_atr_good_max": 3.4,
        "tp_atr_ok_max": 4.2,
        "sl_atr_good_max": 2.1,
        "sl_atr_ok_max": 2.7,
    },
    "US30": {
        "name": "us30",
        "adx_good": 20,
        "adx_ok": 16,
        "timing_gap_good_atr_mult": 0.85,
        "timing_gap_ok_atr_mult": 1.30,
        "tp_atr_good_max": 3.5,
        "tp_atr_ok_max": 4.3,
        "rr_good": 1.3,
        "rr_ok": 1.1,
        "reject_score_below": 38,
    },
    "NAS100": {
        "name": "nas100",
        "adx_good": 19,
        "adx_ok": 15,
        "timing_gap_good_atr_mult": 0.90,
        "timing_gap_ok_atr_mult": 1.35,
        "tp_atr_good_max": 3.6,
        "tp_atr_ok_max": 4.5,
        "rr_good": 1.3,
        "rr_ok": 1.1,
    },
    "BTCUSD": {
        "name": "btcusd",
        "adx_good": 18,
        "adx_ok": 14,
        "buy_rsi_overbought": 82,
        "sell_rsi_oversold": 18,
        "m15_buy_exhaustion_rsi": 84,
        "m15_sell_exhaustion_rsi": 16,
        "tp_atr_good_max": 4.2,
        "tp_atr_ok_max": 5.2,
        "sl_atr_good_max": 2.4,
        "sl_atr_ok_max": 3.0,
        "bars_good_max": 8,
        "bars_ok_max": 12,
        "bars_warn_max": 15,
        "reject_score_below": 37,
        "risky_score_below": 53,
        "accept_score_below": 69,
    },
    "ETHUSD": {
        "name": "ethusd",
        "adx_good": 18,
        "adx_ok": 14,
        "tp_atr_good_max": 4.0,
        "tp_atr_ok_max": 5.0,
        "sl_atr_good_max": 2.3,
        "sl_atr_ok_max": 2.9,
    },
    "SOLUSD": {
        "name": "solusd",
        "adx_good": 17,
        "adx_ok": 13,
        "tp_atr_good_max": 4.4,
        "tp_atr_ok_max": 5.4,
        "sl_atr_good_max": 2.5,
        "sl_atr_ok_max": 3.2,
    },
    "NATURALGAS": {
        "name": "naturalgas",
        "adx_good": 25,
        "adx_ok": 20,
        "tp_atr_good_max": 3.6,
        "tp_atr_ok_max": 4.5,
        "sl_atr_good_max": 2.2,
        "sl_atr_ok_max": 2.9,
        "bars_good_max": 7,
        "bars_ok_max": 10,
        "bars_warn_max": 13,
    },
}


ALIASES = {
    "EUR/USD": "EURUSD",
    "GBP/USD": "GBPUSD",
    "AUD/USD": "AUDUSD",
    "NZD/USD": "NZDUSD",
    "USD/CHF": "USDCHF",
    "USD/CAD": "USDCAD",
    "AUD/JPY": "AUDJPY",
    "CAD/JPY": "CADJPY",
    "GBP/JPY": "GBPJPY",
    "GBP/CAD": "GBPCAD",
    "GBP/AUD": "GBPAUD",
    "AUD/CAD": "AUDCAD",
    "EUR/AUD": "EURAUD",
    "XAU/USD": "XAUUSD",
    "XAG/USD": "XAGUSD",
    "BTC/USD": "BTCUSD",
    "ETH/USD": "ETHUSD",
    "SOL/USD": "SOLUSD",
    "AVAX/USD": "AVAXUSD",
    "XRP/USD": "XRPUSD",
    "ATOM/USD": "ATOMUSD",
    "BCH/USD": "BCHUSD",
    "GOLD": "XAUUSD",
    "SILVER": "XAGUSD",
    "SP500": "US500",
    "SPX500": "US500",
    "S&P500": "US500",
    "DJ30": "US30",
    "DOWJONES": "US30",
    "NASDAQ100": "NAS100",
    "USTEC": "NAS100",
    "FTSE100": "UK100",
    "NATGAS": "NATURALGAS",
    "NG": "NATURALGAS",
}


def normalize_instrument(instrument: str) -> str:
    raw = instrument.strip().upper()
    normalized = ALIASES.get(raw, raw)
    normalized = normalized.replace(" ", "").replace("/", "")
    normalized = ALIASES.get(normalized, normalized)
    return normalized


def get_instrument_category(instrument: str) -> str:
    normalized = normalize_instrument(instrument)
    return INSTRUMENT_CATEGORIES.get(normalized, "default")


def get_instrument_profile(instrument: str) -> dict:
    normalized = normalize_instrument(instrument)
    category = get_instrument_category(normalized)

    profile = deepcopy(DEFAULT_PROFILE)
    profile.update(CATEGORY_PROFILES.get(category, {}))
    profile.update(INSTRUMENT_OVERRIDES.get(normalized, {}))

    profile["instrument"] = normalized
    profile["category"] = category
    return profile
