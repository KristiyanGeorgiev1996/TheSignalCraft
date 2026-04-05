from __future__ import annotations

import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
CSV_PATH = LOGS_DIR / "signal_log.csv"
DB_PATH = LOGS_DIR / "signals.db"

CSV_HEADERS = [
    "timestamp_utc",
    "pair",
    "direction",
    "entry",
    "tp",
    "sl",
    "framework",
    "score",
    "decision",
    "rr",
    "atr",
    "probability",
    "estimated_bars",
    "notes_json",
    "blockers_json",
]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def init_storage() -> None:
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_utc TEXT NOT NULL,
                pair TEXT NOT NULL,
                direction TEXT NOT NULL,
                entry REAL NOT NULL,
                tp REAL NOT NULL,
                sl REAL NOT NULL,
                framework TEXT NOT NULL,
                score INTEGER NOT NULL,
                decision TEXT NOT NULL,
                rr REAL NOT NULL,
                atr REAL NOT NULL,
                probability REAL NOT NULL,
                estimated_bars INTEGER NOT NULL,
                notes_json TEXT NOT NULL,
                blockers_json TEXT NOT NULL
            )
            """
        )
        conn.commit()


def build_log_record(signal_data: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": _utc_now_iso(),
        "pair": signal_data["pair"],
        "direction": signal_data["direction"],
        "entry": float(signal_data["entry"]),
        "tp": float(signal_data["tp"]),
        "sl": float(signal_data["sl"]),
        "framework": str(result["framework"]),
        "score": int(result["score"]),
        "decision": str(result["decision"]),
        "rr": float(result["rr"]),
        "atr": float(result["atr"]),
        "probability": float(result["probability"]),
        "estimated_bars": int(result["estimated_bars"]),
        "notes_json": json.dumps(result.get("notes", []), ensure_ascii=False),
        "blockers_json": json.dumps(result.get("blockers", []), ensure_ascii=False),
    }


def log_signal(signal_data: dict[str, Any], result: dict[str, Any]) -> None:
    init_storage()
    record = build_log_record(signal_data, result)

    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writerow(record)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO signals (
                timestamp_utc, pair, direction, entry, tp, sl,
                framework, score, decision, rr, atr, probability,
                estimated_bars, notes_json, blockers_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["timestamp_utc"],
                record["pair"],
                record["direction"],
                record["entry"],
                record["tp"],
                record["sl"],
                record["framework"],
                record["score"],
                record["decision"],
                record["rr"],
                record["atr"],
                record["probability"],
                record["estimated_bars"],
                record["notes_json"],
                record["blockers_json"],
            ),
        )
        conn.commit()
