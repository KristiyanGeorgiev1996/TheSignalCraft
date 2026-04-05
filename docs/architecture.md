# Architecture

## Overview

**TheSignalCraft** is designed as a modular Python project for evaluating manually submitted trading signals.

The system is structured around a simple but clear separation of responsibilities. Each module is responsible for one main part of the workflow, which improves readability, maintainability, and future extensibility.

The current architecture follows a pipeline-oriented approach:

1. signal input
2. input parsing
3. market data retrieval
4. indicator calculation
5. signal evaluation
6. probability estimation
7. result formatting
8. result persistence

---

## High-Level Structure

```text
app/
├── main.py
├── config.py
├── indicators.py
├── instrument_profiles.py
├── logger.py
├── market_data.py
├── probability_model.py
├── scoring.py
├── signal_parser.py
└── symbol_mapper.py
