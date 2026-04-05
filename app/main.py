from __future__ import annotations

import asyncio
import platform

from telegram.ext import ApplicationBuilder, CommandHandler

from config import TELEGRAM_TOKEN
from indicators import add_indicators
from logger import log_signal
from market_data import get_data
from scoring import calculate
from signal_parser import parse_signal


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def _decorate_timeframes(raw: dict):
    result = {}
    for tf, df in raw.items():
        result[tf] = add_indicators(df) if not df.empty else df
    return result


async def signal(update, context):
    try:
        text = update.message.text or ""
        signal_data = parse_signal(text)

        raw_data = get_data(signal_data["pair"])
        if raw_data["1h"].empty:
            await update.message.reply_text(f"No market data found for {signal_data['pair']}")
            return

        tf_data = _decorate_timeframes(raw_data)
        if tf_data["1h"].empty:
            await update.message.reply_text(
                f"Not enough processed 1H data for {signal_data['pair']}. Try again later or use another symbol."
            )
            return

        result = calculate(signal_data, tf_data)
        log_signal(signal_data, result)

        message = (
            "Signal Analysis\n\n"
            f"Pair: {signal_data['pair']}\n"
            f"Direction: {signal_data['direction']}\n"
            f"Entry: {signal_data['entry']}\n"
            f"TP: {signal_data['tp']}\n"
            f"SL: {signal_data['sl']}\n\n"
            f"Framework: {result['framework']}\n"
            f"Profile: {result['profile_name']}\n"
            f"Category: {result['category']}\n"
            f"ATR(1H): {result['atr']:.5f}\n"
            f"Risk/Reward: {result['rr']:.2f}\n"
            f"TP-first probability: {result['probability']:.1f}%\n"
            f"Estimated duration: ~{result['estimated_bars']} H1 bars\n\n"
            f"Score: {result['score']}/100\n"
            f"Decision: {result['decision']}\n\n"
            "Why it may be good:\n"
        )

        if result["notes"]:
            for note in result["notes"]:
                message += f"+ {note}\n"
        else:
            message += "+ No strong positives found\n"

        message += "\nWhy it may fail:\n"
        if result["blockers"]:
            for item in result["blockers"]:
                message += f"- {item}\n"
        else:
            message += "- No major blockers detected\n"

        await update.message.reply_text(message)

    except ValueError as exc:
        await update.message.reply_text(f"Signal format error: {exc}")
    except Exception as exc:
        await update.message.reply_text(f"Unexpected error: {exc}")


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("signal", signal))

print("Bot running...")
app.run_polling()
