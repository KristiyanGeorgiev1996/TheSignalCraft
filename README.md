# TheSignalCraft

<p align="center">
  <b>Turning raw signals into reasoned decisions.</b>
</p>

<p align="center">
  A modular Python project for evaluating manually submitted trading signals through technical analysis, scoring logic, and probability-based decision support.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/github/license/KristiyanGeorgiev1996/TheSignalCraft" alt="License">
  <img src="https://img.shields.io/github/repo-size/KristiyanGeorgiev1996/TheSignalCraft" alt="Repository size">
  <img src="https://img.shields.io/github/last-commit/KristiyanGeorgiev1996/TheSignalCraft" alt="Last commit">
  <img src="https://img.shields.io/github/issues/KristiyanGeorgiev1996/TheSignalCraft" alt="Issues">
  <img src="https://img.shields.io/badge/status-active-success" alt="Status">
  <img src="https://img.shields.io/badge/focus-signal%20evaluation-informational" alt="Focus">
</p>

---

## Overview

**TheSignalCraft** is a modular signal evaluation project built to help assess the quality of manually submitted trading signals.

Instead of executing trades automatically, the system processes a signal, fetches market data, applies technical indicators, evaluates the setup through a scoring framework, estimates the probability of take-profit being reached before stop-loss, and returns a structured decision.

The goal is not to replace judgment, but to support more disciplined and risk-aware trade evaluation.

---

## Screenshots

> Store the images below inside the `screenshots/` folder and keep the filenames exactly as shown.

### 1. Signal analysis output
![Signal analysis output](screenshots/signal-analysis.png)

### 2. Project structure / code overview
![Project structure](screenshots/project-structure.png)

### 3. Example bot interaction
![Bot interaction](screenshots/bot-interaction.png)

---

## Key Features

- **Manual signal parsing** through a simple Telegram command interface
- **Multi-timeframe market analysis** using M15, H1, and H4 data
- **Technical indicator enrichment** with:
  - EMA 20 / 50 / 200
  - RSI
  - ATR
  - ADX
  - MACD
  - Bollinger Bands
- **Signal scoring engine** based on:
  - trend alignment
  - momentum confirmation
  - timing quality
  - stop-loss and take-profit realism
  - risk/reward quality
  - structural room to target
- **Probability estimation** for TP-first outcomes using historical analog setups
- **Instrument-aware profiles** for forex, crypto, indices, metals, and energy markets
- **Persistent logging** to CSV and SQLite for tracking and review
- **Modular architecture** for easier extension and maintenance

---

## How It Works

The system follows a straightforward evaluation pipeline:

1. A trading signal is submitted manually  
2. The input is parsed into a structured format  
3. Market data is fetched for the requested instrument  
4. Technical indicators are added to the dataset  
5. The signal is evaluated through scoring logic  
6. A probability estimate is generated  
7. A final decision is returned  
8. The result is stored for later review  

---

## Decision Model

The project currently classifies signals into four outcome categories:

- **REJECT**
- **RISKY**
- **ACCEPT**
- **STRONG TRADE**

These decisions are based on a weighted scoring framework that takes into account market structure, volatility, trend strength, entry timing, and probability context.

---

## Tech Stack

- **Python**
- **pandas**
- **numpy**
- **yfinance**
- **ta**
- **python-telegram-bot**
- **SQLite**
- **CSV logging**

---

## Project Structure

```text
TheSignalCraft/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── indicators.py
│   ├── instrument_profiles.py
│   ├── logger.py
│   ├── market_data.py
│   ├── probability_model.py
│   ├── scoring.py
│   ├── signal_parser.py
│   └── symbol_mapper.py
├── screenshots/
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
