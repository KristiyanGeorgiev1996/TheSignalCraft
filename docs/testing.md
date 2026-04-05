# Testing

## Overview

TheSignalCraft includes an automated test suite that validates the core analytical and decision-making components of the system.

The goal of testing is to ensure correctness, reduce regressions, and provide a reliable foundation for future improvements.

---

## Test Scope

The current test suite covers the most critical parts of the system:

- signal parsing and input validation  
- symbol normalization and mapping  
- instrument categorization and profile resolution  
- probability model behavior  
- scoring and decision logic  
- main signal-processing flow  

---

## Test Structure

```text
tests/
├── test_signal_parser.py
├── test_symbol_mapper.py
├── test_instrument_profiles.py
├── test_probability_model.py
├── test_scoring.py
├── test_main_flow.py
└── README.md
```

---

## Testing Approach

The project uses a combination of testing strategies:

### Unit Tests

Test individual functions and isolated logic.

Examples:

- parsing input signals  
- mapping symbols  
- validating instrument profiles  

---

### Behavior Tests

Validate expected outcomes under defined conditions.

Examples:

- correct decision classification  
- valid vs invalid signal handling  
- scoring output structure  

---

### Flow-Oriented Tests

Test how different modules interact together.

Examples:

- signal processing from input to final response  
- interaction between parser, data, and scoring  
- handling of edge cases in the main flow  

---

## Why This Matters

The current test coverage focuses on the most important aspects of the system:

- correctness of input handling  
- reliability of analysis logic  
- consistency of decision output  
- safety during future changes  

This ensures the project remains stable as it evolves.

---

## Running Tests

Run all tests:

```bash
py -m pytest -v
```

Run a specific file:
```
py -m pytest tests/test_scoring.py -v
```

Run a specific test:
```
py -m pytest tests/test_scoring.py::test_valid_signal -v
```

---

## Future Improvements

Potential improvements to the test suite include:

- logger and persistence testing  
- market data mocking  
- indicator validation tests  
- output formatting tests  
- regression scenarios  
- test coverage reporting  
- CI integration (GitHub Actions)  

---

## Summary

The current test suite provides a solid and practical foundation.

It ensures that the core logic of TheSignalCraft is validated, stable, and ready for further development.
