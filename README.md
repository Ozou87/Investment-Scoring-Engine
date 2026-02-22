# Investment Scoring Engine

A modular, sector-aware multi-factor investment scoring engine written
in Python.\
The system evaluates public companies using Fundamental, Valuation, and
Moat metrics, and outputs both module-level scores and a final weighted
score (0--100).

An automated scoring engine designed to significantly reduce the time
investors spend on research.

------------------------------------------------------------------------

## High-Level Concept

The engine is built around three independent analytical pillars:

1.  Fundamentals -- How strong is the business today?
2.  Valuation -- How expensive the stock is relative to its sector?
3.  Moat -- How durable is the company's competitive advantage?

Each pillar:

-   Converts raw financial inputs into normalized scores (0--100)
-   Applies sector-specific weights (defined in config.py)
-   Produces a final module score

A Core Engine then aggregates all module scores into a single Final
Score.

------------------------------------------------------------------------

## Architecture Overview

-   Pure business logic (no I/O inside modules)
-   Centralized API layer (api_caller.py)
-   Clean orchestration layer (assemble_data.py)
-   Config-driven weighting system
-   Fully testable using pytest
-   Modular and scalable design

------------------------------------------------------------------------

## Project Structure

``` bash
investment-scoring-engine/
│
├── api_caller.py
├── app.py
├── assemble_data.py
├── company_provider.py
├── config.py
├── core_engine.py
├── fundamental_module.py
├── valuation_module.py
├── moat_module.py
├── scoring_utils.py
│
├── sector_reports_10-2-26/
│
├── data_reports/
│
├── tests/
│   ├── test_final_score.py
│   ├── test_fundamentals_score.py
│   ├── test_moat_score.py
│   └── test_valuation_score.py
│
├── requirements.txt
├── LICENSE
└── README.md
```

------------------------------------------------------------------------

## Tests

Run all tests:

``` bash
pytest -v
```

Optional coverage:

``` bash
pytest --cov
```

------------------------------------------------------------------------

## Running the Project

``` bash
python app.py
```

------------------------------------------------------------------------

## Disclaimer

Not financial advice. Do your own research.

------------------------------------------------------------------------

## License

All Rights Reserved -- Educational & Portfolio Use Only.

------------------------------------------------------------------------

## Author

Oz Efraty\
Python Developer \| Finance & Tech Enthusiast
