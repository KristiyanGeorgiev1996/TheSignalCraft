from instrument_profiles import normalize_instrument


# Ръчни мапинги за не-forex инструменти и специални случаи
SYMBOL_MAP = {
    # Metals
    "XAUUSD": "GC=F",
    "XAGUSD": "SI=F",
    "COPPER": "HG=F",

    # Energy
    "NATURALGAS": "NG=F",

    # Indices
    "US500": "^GSPC",
    "US30": "^DJI",
    "NAS100": "^NDX",
    "UK100": "^FTSE",

    # Crypto
    "BTCUSD": "BTC-USD",
    "ETHUSD": "ETH-USD",
    "SOLUSD": "SOL-USD",
    "AVAXUSD": "AVAX-USD",
    "XRPUSD": "XRP-USD",
    "ATOMUSD": "ATOM-USD",
    "BCHUSD": "BCH-USD",
}


FOREX_CURRENCIES = {
    "EUR", "USD", "GBP", "AUD", "NZD", "CHF", "CAD", "JPY"
}


def _is_forex_pair(symbol: str) -> bool:
    """
    Пример:
    EURUSD -> True
    GBPJPY -> True
    EURAUD -> True
    XAUUSD -> False
    BTCUSD -> False
    """
    if len(symbol) != 6:
        return False

    base = symbol[:3]
    quote = symbol[3:]

    if base == quote:
        return False

    return base in FOREX_CURRENCIES and quote in FOREX_CURRENCIES


def get_symbol(pair: str) -> str:
    normalized = normalize_instrument(pair)

    # 1) Ако имаме специален ръчен mapping -> ползваме него
    if normalized in SYMBOL_MAP:
        return SYMBOL_MAP[normalized]

    # 2) Ако е стандартна forex двойка -> автоматично я правим Yahoo forex symbol
    if _is_forex_pair(normalized):
        return f"{normalized}=X"

    # 3) Fallback
    return normalized
