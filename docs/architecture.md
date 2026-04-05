# Architecture

## Overview

**TheSignalCraft** is designed as a modular Python project for evaluating manually submitted trading signals.

The system follows a structured and sequential processing approach, where each module has a clearly defined responsibility. This separation improves readability, maintainability, and allows easier future extensions.

The overall architecture is built around a pipeline:

1. signal input  
2. input parsing  
3. market data retrieval  
4. indicator calculation  
5. signal evaluation  
6. probability estimation  
7. decision generation  
8. result logging  

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
```

---

## Responsibility Layers

### Input Layer

Handles incoming user input and converts it into a structured format.

- `main.py`  
- `signal_parser.py`  

---

### Data Layer

Responsible for symbol normalization and market data retrieval.

- `market_data.py`  
- `symbol_mapper.py`  
- `instrument_profiles.py`  

---

### Analysis Layer

Performs technical analysis and signal evaluation.

- `indicators.py`  
- `scoring.py`  
- `probability_model.py`  

---

### Persistence Layer

Stores processed signals for tracking and later analysis.

- `logger.py`  

---

### Configuration Layer

Handles environment-based configuration.

- `config.py`  

---

## Architectural Principles

The project follows several core principles:

- **Modularity**  
  Each module has a single, focused responsibility.  

- **Separation of Concerns**  
  Input handling, data processing, analysis, and storage are clearly separated.  

- **Traceability**  
  All processed signals can be logged and reviewed later.  

- **Extensibility**  
  New indicators, rules, or instruments can be added with minimal changes.  

- **Simplicity**  
  The system avoids unnecessary complexity and remains easy to understand.  

---

## Design Rationale

This architecture is intentionally lightweight and practical.

It works well for this project because:

- the input format is simple and structured  
- the analysis flow is sequential  
- the scoring logic is rule-based  
- the system does not require a heavy framework  
- each module can be tested independently  

---

## Summary

The current architecture provides a clean and maintainable foundation for a signal evaluation system.

It balances simplicity with structure, making the project suitable for both demonstration and further development.
