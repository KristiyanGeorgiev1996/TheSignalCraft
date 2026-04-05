import pandas as pd
import ta


def add_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Add a compact but useful set of indicators for signal filtering."""
    if data.empty:
        return data

    df = data.copy()
    close = df["Close"].astype(float).squeeze()
    high = df["High"].astype(float).squeeze()
    low = df["Low"].astype(float).squeeze()
    volume = df["Volume"].astype(float).squeeze() if "Volume" in df.columns else pd.Series(0, index=df.index)

    df["ema20"] = ta.trend.EMAIndicator(close, window=20).ema_indicator()
    df["ema50"] = ta.trend.EMAIndicator(close, window=50).ema_indicator()
    df["ema200"] = ta.trend.EMAIndicator(close, window=200).ema_indicator()
    df["rsi"] = ta.momentum.RSIIndicator(close, window=14).rsi()
    df["atr"] = ta.volatility.AverageTrueRange(high, low, close, window=14).average_true_range()
    df["adx"] = ta.trend.ADXIndicator(high, low, close, window=14).adx()
    macd = ta.trend.MACD(close)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_hist"] = macd.macd_diff()
    bb = ta.volatility.BollingerBands(close, window=20, window_dev=2)
    df["bb_high"] = bb.bollinger_hband()
    df["bb_low"] = bb.bollinger_lband()
    df["bb_width"] = (df["bb_high"] - df["bb_low"]).replace(0, pd.NA)
    df["vol_sma20"] = pd.Series(volume, index=df.index).rolling(20).mean()
    return df.dropna().copy()
