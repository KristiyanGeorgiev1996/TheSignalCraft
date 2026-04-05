# Workflow

## Overview

TheSignalCraft processes a manually submitted trading signal through a structured, multi-step workflow.

The purpose of this workflow is not trade execution, but consistent and explainable signal evaluation.

---

## Signal Processing Flow

```text
Signal Input
     ↓
Signal Parsing
     ↓
Market Data Retrieval
     ↓
Indicator Enrichment
     ↓
Scoring Engine
     ↓
Probability Model
     ↓
Final Decision
     ↓
Logging
```

---

## Step-by-Step Breakdown

### 1. Signal Input

A signal is submitted manually using a predefined command format:

```text
/signal PAIR DIRECTION ENTRY TP SL
```

Example:
```
/signal GBPUSD BUY 1.2750 1.2820 1.2700
```

---

### 2. Signal Parsing

The raw input is parsed into a structured object containing:

- pair  
- direction  
- entry  
- take profit  
- stop loss  

At this stage, the system validates:

- command format  
- allowed directions (BUY / SELL)  
- numeric values  

---

### 3. Market Data Retrieval

The system retrieves market data for the requested instrument.

The current implementation uses multiple timeframes:

- M15 → entry timing  
- H1 → main analysis  
- H4 → higher timeframe context  

---

### 4. Indicator Enrichment

The retrieved data is enriched with technical indicators:

- EMA (20, 50, 200)  
- RSI  
- ATR  
- ADX  
- MACD  
- Bollinger Bands  

These indicators provide the analytical foundation for evaluation.

---

### 5. Scoring Engine

The signal is evaluated using a weighted scoring system.

Key factors include:

- trend direction and alignment  
- momentum strength  
- RSI conditions  
- volatility (ATR)  
- trend strength (ADX)  
- entry timing  
- stop-loss distance  
- take-profit realism  
- risk/reward ratio  
- structural room to target  

---

### 6. Probability Model

The system estimates the probability of TP being reached before SL.

This is done using a heuristic approach based on historical analog conditions, not a machine learning model.

---

### 7. Final Decision

The signal is classified into one of the following categories:

- REJECT  
- RISKY  
- ACCEPT  
- STRONG TRADE  

This decision is based on:

- final score  
- detected blockers  
- overall signal quality  

---

### 8. Logging

The evaluated signal is stored for later analysis.

Current storage formats:

- CSV  
- SQLite  

This allows tracking performance and reviewing past decisions.

---

## Summary

The workflow is designed to be:

- linear  
- interpretable  
- modular  

Each step builds on the previous one, resulting in a structured and explainable evaluation process.
