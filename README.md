# Investment Scoring Engine (V1)

A modular, sector-aware **multi-factor investment scoring engine** written in Python.  
The system evaluates public companies using **Fundamental, Valuation, and Moat metrics**, and outputs both **module-level scores** and a **final weighted score (0–100)**.

This project is designed as a **learning + portfolio project**, with a clean architecture that is ready for future automation via financial data APIs.

---

## High-Level Concept

The engine is built around three independent analytical pillars:

1. **Fundamentals** – How strong is the business today?
2. **Valuation** – How expensive the stock is relative to its sector?
3. **Moat** – How durable is the company’s competitive advantage?

Each pillar:
- Converts raw financial inputs into **normalized scores (0–100)** using threshold tables
- Applies **sector-specific weights**
- Produces a final module score

A **Core Engine** then aggregates all module scores into a single **Final Score**, using sector-aware weights.

---

## Project Structure

```
project_root/
│
├── main.py
├── core_engine.py
├── fundamental_module.py
├── valuation_module.py
├── moat_module.py
├── scoring_utils.py
├── config.py
├── LICENSE
└── README.md
```

## Future Roadmap

- add tests using pytest
- Add support for real financial data via API    
- Add sentiment/analyst module  
- Create a web dashboard or REST API  
- Deploy as a microservice  
---

## Running the Project

```bash
python main.py

```
You will be prompted for financial values manually.  
A future version will pull all values automatically from APIs.

---

## License

All Rights Reserved – Educational & Portfolio Use Only.
See the LICENSE file for full details.

## Author

**Oz Efraty**  
Python developer & tech investor.
Sharing my journey on Linkedin.
