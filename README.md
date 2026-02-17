# Investment Scoring Engine

A modular, sector-aware **multi-factor investment scoring engine** written in Python.
The system evaluates public companies using **Fundamental, Valuation, and Moat metrics**, and outputs both **module-level scores** and a **final weighted score (0–100)**.

An automated scoring engine designed to significantly reduce the time investors spend on research.

This project is designed as a **portfolio project**, with a clean, testable architecture that is ready for future automation via financial data APIs.

---

## High-Level Concept

The engine is built around three independent analytical pillars:

1. **Fundamentals** – How strong is the business today?
2. **Valuation** – How expensive the stock is relative to its sector?
3. **Moat** – How durable is the company’s competitive advantage?

Each pillar:

- Converts raw financial inputs into **normalized scores (0–100)** using threshold tables
- Applies **sector-specific weights** (defined centrally in `config.py`)
- Produces a final module score

A **Core Engine** then aggregates all module scores into a single **Final Score**, using sector-aware weights.

---

## Architecture Overview

- **Pure business logic** – no I/O inside modules
- **Dataclass-based inputs** for strong structure and clarity
- **Config-driven weighting system** (easy to extend per sector)
- **Fully testable** using pytest + mocking

---

## Project Structure

project_root/
│
├── main.py
├── core_engine.py
├── fundamental_module.py
├── valuation_module.py
├── moat_module.py
├── scoring_utils.py
├── config.py
│
├── tests/
│   ├── test_fundamentals_score.py
│   ├── test_valuation_score.py
│   ├── test_moat_score.py
│   └── test_final_score.py
│
├── LICENSE
└── README.md

## Future Roadmap

- Add support for real financial data via API
- Add earnings vs. estimates module
- Add compare companies tool
- Create a web dashboard
- Use Docker, Jenkins and Jira
- Deploy as a microservice

---

## Tests

Run all tests:

```bash
pytest -v
```

Optional coverage:

```bash
pytest --cov
```

All scores are validated to be integers between **0–100**.

---

## Running the Project

```bash
python app.py
```

You will be prompted for financial values manually.
A future version will pull all values automatically from APIs.
With API integration, the system will also automatically detect the company’s sector—no manual input required.


## disclaimer
Not financial advice. Personal opinion only. Do your own research.

## License

All Rights Reserved – Educational & Portfolio Use Only.
See the LICENSE file for full details.

## Author

Oz Efraty | Python developer & tech investor.

