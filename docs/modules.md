# Modules

## Overview

This document describes the role and responsibility of each core module in the **TheSignalCraft** project.

The system is designed in a modular way, where each file has a clearly defined purpose within the signal evaluation pipeline.

---

## Core Modules

### `main.py`

This is the main entry point of the application.

Responsibilities:

- initializes the Telegram bot  
- receives incoming signals  
- orchestrates the full processing workflow  
- connects all modules together  
- sends the final response back to the user  

This file acts as the coordination layer of the system.

---

### `config.py`

Handles environment-based configuration.

Responsibilities:

- loads environment variables  
- provides access to runtime configuration (e.g. Telegram token)  

This ensures that sensitive data is not stored directly in the codebase.

---

### `signal_parser.py`

Responsible for parsing and validating incoming signals.

Responsibilities:

- validates command format  
- validates direction (BUY / SELL)  
- converts values to numeric types  
- returns structured signal data  

This is the first validation layer in the system.

---

### `market_data.py`

Handles retrieval of market data.

Responsibilities:

- fetches price data from external sources (`yfinance`)  
- prepares multi-timeframe datasets  
- ensures data is ready for analysis  

---

### `symbol_mapper.py`

Normalizes trading symbols.

Responsibilities:

- converts user input into standardized formats  
- maps symbols to data provider formats  
- handles aliases (e.g. GOLD → XAUUSD)  
- provides fallback behavior  

---

### `instrument_profiles.py`

Defines instrument-specific parameters.

Responsibilities:

- assigns instruments to categories (forex, crypto, etc.)  
- defines scoring thresholds  
- applies overrides for specific instruments  
- supports alias normalization  

This allows the evaluation model to adapt across markets.

---

### `indicators.py`

Adds technical indicators to market data.

Responsibilities:

- calculates EMA (20, 50, 200)  
- calculates RSI  
- calculates ATR  
- calculates ADX  
- calculates MACD  
- calculates Bollinger Bands  

This module prepares the data used by the scoring engine.

---

### `scoring.py`

Core evaluation engine of the system.

Responsibilities:

- evaluates signal quality  
- applies weighted scoring logic  
- detects blockers  
- generates notes  
- calculates risk/reward  
- produces final classification  

This is the most important decision-making module.

---

### `probability_model.py`

Provides probability and duration estimations.

Responsibilities:

- estimates probability of TP vs SL  
- estimates time to target (in bars)  

This module complements scoring with probabilistic context.

---

### `logger.py`

Handles persistence of analyzed signals.

Responsibilities:

- creates log records  
- saves results to CSV  
- saves results to SQLite  
- ensures traceability  

---

## Summary

Each module in TheSignalCraft has a clearly defined role within the system.

This modular structure makes the project:

- easier to understand  
- easier to test  
- easier to extend  
- safer to modify  

The separation of responsibilities ensures that changes in one part of the system have minimal impact on others.
