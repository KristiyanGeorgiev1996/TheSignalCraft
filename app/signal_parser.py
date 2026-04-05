from __future__ import annotations


def parse_signal(text: str):
    """Parse manual signal text from Telegram.

    Supported format:
    /signal PAIR DIRECTION ENTRY TP SL
    Example:
    /signal GBPUSD BUY 1.2750 1.2820 1.2700
    """
    parts = text.strip().replace(",", ".").split()
    if len(parts) != 6:
        raise ValueError("Expected format: /signal PAIR DIRECTION ENTRY TP SL")

    command, pair, direction, entry, tp, sl = parts
    if command.lower() != "/signal":
        raise ValueError("Command must start with /signal")

    direction = direction.upper()
    if direction not in {"BUY", "SELL"}:
        raise ValueError("Direction must be BUY or SELL")

    signal = {
        "pair": pair.upper(),
        "direction": direction,
        "entry": float(entry),
        "tp": float(tp),
        "sl": float(sl),
    }
    return signal
