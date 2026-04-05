from __future__ import annotations

import pandas as pd
import yfinance as yf
from symbol_mapper import get_symbol


YF_KWARGS = dict(auto_adjust=False, progress=False, threads=False)


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    return df


def _download(symbol: str, interval: str, period: str) -> pd.DataFrame:
    df = yf.download(symbol, interval=interval, period=period, **YF_KWARGS)
    df = _normalize_columns(df)
    return df.dropna(how="all")


def get_data(pair: str) -> dict[str, pd.DataFrame]:
    """Return multi-timeframe market data.

    15m is used for entry timing, 1h for main analysis, and 4h is resampled
    from 1h to avoid unsupported broker/feed variations.
    """
    symbol = get_symbol(pair)
    m15 = _download(symbol, interval="15m", period="10d")
    h1 = _download(symbol, interval="1h", period="60d")

    if h1.empty:
        return {"15m": m15, "1h": h1, "4h": pd.DataFrame()}

    h4 = (
        h1[["Open", "High", "Low", "Close", "Volume"]]
        .resample("4h")
        .agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum",
        })
        .dropna()
    )

    return {"15m": m15, "1h": h1, "4h": h4}
