# Tests

This directory contains the automated test suite for the core modules of **TheSignalCraft**.

The current tests are focused on validating the most important analytical and decision-support components of the project. Their purpose is to improve reliability, reduce regressions, and support safer future changes.

## Scope

The test suite currently covers:

- signal parsing and input validation
- symbol normalization and mapping
- instrument categorization and profile resolution
- probability model behavior
- scoring and decision logic

## Test Files

- `test_signal_parser.py`  
  Verifies supported input format, direction validation, numeric parsing, and invalid signal handling.

- `test_symbol_mapper.py`  
  Validates symbol normalization and conversion logic for forex pairs, metals, crypto, and indices.

- `test_instrument_profiles.py`  
  Tests alias handling, category detection, and instrument profile selection.

- `test_probability_model.py`  
  Covers probability helper functions, fallback behavior, and selected edge cases.

- `test_scoring.py`  
  Validates the core evaluation workflow, including invalid setups, output structure, and decision classification.

## Purpose

These tests are intended to:

- validate core business logic
- protect expected behavior during refactoring
- improve maintainability
- provide a safer foundation for future extensions

## Run the Test Suite

```bash
py -m pytest -v
```

