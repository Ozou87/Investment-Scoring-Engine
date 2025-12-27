
# file will help determine between differnet type of sector and help selidify weighted scores per sector.

def fundamental_weight(sector_name: str) -> dict:
    
    SECTOR_WEIGHTS = {
    "technology": {
        "growth": 0.30,
        "profit": 0.30,
        "debt_to_equity": 0.20,
        "fcf": 0.20
                },
    "healthcare": {
        "growth": 0.25,
        "profit": 0.35,
        "debt_to_equity": 0.20,
        "fcf": 0.20
                    },
    "financials": {
        "growth": 0.20,
        "profit": 0.40,
        "debt_to_equity": 0.30,
        "fcf": 0.10
                    }
                    }

    sector_name = sector_name.lower().strip()

    if sector_name not in SECTOR_WEIGHTS:
        raise ValueError(f"Unsupported sector: sector {sector_name} is not defind in the system")
    return SECTOR_WEIGHTS[sector_name]
    
def valuation_weight(sector_name: str) -> dict:
    SECTOR_WEIGHTS = {
    "technology": {
        "pe": 0.20,
        "fpe": 0.30,
        "ev_ebitda": 0.20,
        "ps": 0.20,
        "price_fcf": 0.1
                },
    "financials": {
        "pe": 0.25,
        "forward_pe": 0.30,
        "ev_ebitda": 0.25,
        "ps": 0.10,
        "price_fcf": 0.10
                    },
    "healthcare": {
        "pe": 0.30,
        "forward_pe": 0.25,
        "ev_ebitda": 0.25,
        "ps": 0.10,
        "price_fcf": 0.10
                    }
                    }
    
    sector_name = sector_name.lower().strip()

    if sector_name not in SECTOR_WEIGHTS:
        raise ValueError(f"Unsupported sector: sector {sector_name} is not defind in the system")
    return SECTOR_WEIGHTS[sector_name]

def moat_weight(sector_name: str) -> dict:
    SECTOR_WEIGHTS = {
    "technology": {
        "roic": 0.35,
        "fcf_5y_g": 0.20,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.25
                },
    "financials": {
        "roic": 0.45,
        "fcf_5y_g": 0.25,
        "gm_stability": 0.25,
        "rnd_to_rev": 0.05
                    },
    "healthcare": {
        "roic": 0.30,
        "fcf_5y_g": 0.15,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.35
                    }
                    }
    
    sector_name = sector_name.lower().strip()

    if sector_name not in SECTOR_WEIGHTS:
        raise ValueError(f"Unsupported sector: sector {sector_name} is not defind in the system")
    return SECTOR_WEIGHTS[sector_name]


#for the total score weighting
def total_weight(sector_name: str) -> dict:
    pass

