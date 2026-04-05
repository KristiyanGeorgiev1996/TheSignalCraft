from symbol_mapper import get_symbol


def test_get_symbol_maps_forex_pair_to_yahoo_format():
    assert get_symbol("EURUSD") == "EURUSD=X"


def test_get_symbol_maps_forex_pair_with_slash():
    assert get_symbol("EUR/USD") == "EURUSD=X"


def test_get_symbol_maps_gold():
    assert get_symbol("XAUUSD") == "GC=F"


def test_get_symbol_maps_bitcoin():
    assert get_symbol("BTCUSD") == "BTC-USD"


def test_get_symbol_maps_sp500_alias():
    assert get_symbol("SP500") == "^GSPC"


def test_get_symbol_returns_fallback_for_unknown_symbol():
    assert get_symbol("UNKNOWN") == "UNKNOWN"
