## 📁 Folder Structure

The folder represents a modular system for analyzing and evaluating trading signals. Each file has a clearly defined responsibility:

### 🔹 Core Modules

- `main.py`  
  Entry point of the application. Initializes the Telegram bot, receives signals, and orchestrates the full processing flow.

- `config.py`  
  Loads configuration values from environment variables (e.g., Telegram token).

- `signal_parser.py`  
  Parses raw input text into a structured signal (pair, direction, entry, TP, SL).

---

### 📊 Analysis & Logic

- `indicators.py`  
  Enriches market data with technical indicators (EMA, RSI, MACD, ATR, ADX, Bollinger Bands).

- `scoring.py`  
  Core signal evaluation logic. Combines multiple factors such as trend structure, momentum, risk/reward, and market context.

- `probability_model.py`  
  Estimates the probability of TP being hit before SL using historical analog setups.

---

### 📈 Data & Instruments

- `market_data.py`  
  Fetches market data via `yfinance` and prepares a multi-timeframe structure (M15, H1, H4).

- `symbol_mapper.py`  
  Normalizes different symbol formats into a standardized format for data sources.

- `instrument_profiles.py`  
  Defines profiles and parameters for different instrument categories (forex, crypto, indices, etc.).

---

### 💾 Storage & Logging

- `logger.py`  
  Persists analyzed signals into CSV and SQLite for tracking and further analysis.

---

## 🧠 Processing Flow

1. Receive signal  
2. Parse input  
3. Fetch market data  
4. Apply technical indicators  
5. Compute score and probability  
6. Generate final decision  
7. Store result  

---

## ⚙️ Notes

- The project is modular by design for easier extension  
- Each component can be tested and used independently  
- Responsibilities are separated between data handling, analysis, and evaluation
