from instrument_profiles import (
    get_instrument_category,
    get_instrument_profile,
    normalize_instrument,
)


def test_normalize_instrument_handles_slash_format():
    assert normalize_instrument("EUR/USD") == "EURUSD"


def test_normalize_instrument_handles_alias():
    assert normalize_instrument("GOLD") == "XAUUSD"


def test_get_instrument_category_for_forex_major():
    assert get_instrument_category("EURUSD") == "forex_major"


def test_get_instrument_category_for_crypto():
    assert get_instrument_category("BTCUSD") == "crypto"


def test_get_instrument_category_for_unknown_defaults():
    assert get_instrument_category("UNKNOWN") == "default"


def test_get_instrument_profile_contains_required_keys():
    profile = get_instrument_profile("EURUSD")

    assert "instrument" in profile
    assert "category" in profile
    assert "adx_good" in profile
    assert "rr_good" in profile
    assert profile["instrument"] == "EURUSD"
    assert profile["category"] == "forex_major"


def test_get_instrument_profile_applies_override():
    profile = get_instrument_profile("BTCUSD")

    assert profile["instrument"] == "BTCUSD"
    assert profile["category"] == "crypto"
    assert profile["name"] == "btcusd"
