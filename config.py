
def fundamental_weight(sector_name: str) -> dict:
    
    SECTOR_WEIGHTS = {
    "Technology": {
        "growth": 0.30,
        "profit": 0.30,
        "debt_to_equity": 0.20,
        "fcf": 0.20
                },
    "Financial services": {
        "growth": 0.20,
        "profit": 0.40,
        "debt_to_equity": 0.30,
        "fcf": 0.10
                    },
    "Healthcare": {
        "growth": 0.25,
        "profit": 0.35,
        "debt_to_equity": 0.20,
        "fcf": 0.20
                    },
    "Consumer cyclical": {
        "growth": 0.30,
        "profit": 0.30,
        "debt_to_equity": 0.20,
        "fcf": 0.20
                },
    "Consumer defensive": {
        "growth": 0.20,
        "profit": 0.40,
        "debt_to_equity": 0.30,
        "fcf": 0.10
                    },
    "Communication services": {
        "growth": 0.25,
        "profit": 0.35,
        "debt_to_equity": 0.20,
        "fcf": 0.20
                    },
    "Industrials": {
        "growth": 0.30,
        "profit": 0.30,
        "debt_to_equity": 0.20,
        "fcf": 0.20
                },
    "Energy": {
        "growth": 0.20,
        "profit": 0.40,
        "debt_to_equity": 0.30,
        "fcf": 0.10
                    },
    "Utilities": {
        "growth": 0.25,
        "profit": 0.35,
        "debt_to_equity": 0.20,
        "fcf": 0.20
                    },
    "Basic materials": {
        "growth": 0.20,
        "profit": 0.40,
        "debt_to_equity": 0.30,
        "fcf": 0.10
                    },
    "Real estate": {
        "growth": 0.25,
        "profit": 0.35,
        "debt_to_equity": 0.20,
        "fcf": 0.20
                    }
                    }

    sector_name = sector_name.lower().strip()

    if sector_name not in SECTOR_WEIGHTS:
        raise ValueError(f"Unsupported sector: sector {sector_name} is not defind in the system")
    return SECTOR_WEIGHTS[sector_name]
    
def valuation_weight(sector_name: str) -> dict:
    SECTOR_WEIGHTS = {
    "Technology": {
        "pe": 0.20,
        "fpe": 0.30,
        "ev_ebitda": 0.20,
        "ps": 0.20,
        "price_fcf": 0.1
                },
    "Financial services": {
        "pe": 0.25,
        "fpe": 0.30,
        "ev_ebitda": 0.25,
        "ps": 0.10,
        "price_fcf": 0.10
                    },
    "Healthcare": {
        "pe": 0.30,
        "fpe": 0.25,
        "ev_ebitda": 0.25,
        "ps": 0.10,
        "price_fcf": 0.10
                    },
    "Consumer cyclical": {
        "pe": 0.30,
        "fpe": 0.30,
        "ev_ebitda": 0.20,
        "ps": 0.20,
        "price_fcf": 0.1
                },
    "Consumer defensive": {
        "pe": 0.30,
        "fpe": 0.30,
        "ev_ebitda": 0.20,
        "ps": 0.20,
        "price_fcf": 0.1
                    },
    "Communication services": {
        "pe": 0.30,
        "fpe": 0.30,
        "ev_ebitda": 0.20,
        "ps": 0.20,
        "price_fcf": 0.1
                    },
    "Industrials": {
        "pe": 0.30,
        "fpe": 0.30,
        "ev_ebitda": 0.20,
        "ps": 0.20,
        "price_fcf": 0.1
                },
    "Energy": {
        "pe": 0.30,
        "fpe": 0.30,
        "ev_ebitda": 0.20,
        "ps": 0.20,
        "price_fcf": 0.1
                    },
    "Utilities": {
        "pe": 0.30,
        "fpe": 0.30,
        "ev_ebitda": 0.20,
        "ps": 0.20,
        "price_fcf": 0.1
                    },
    "Basic materials": {
        "pe": 0.30,
        "fpe": 0.30,
        "ev_ebitda": 0.20,
        "ps": 0.20,
        "price_fcf": 0.1
                    },
    "Real estate": {
        "pe": 0.30,
        "fpe": 0.30,
        "ev_ebitda": 0.20,
        "ps": 0.20,
        "price_fcf": 0.1
                    }
                    }
    
    sector_name = sector_name.lower().strip()

    if sector_name not in SECTOR_WEIGHTS:
        raise ValueError(f"Unsupported sector: sector {sector_name} is not defind in the system")
    return SECTOR_WEIGHTS[sector_name]

def moat_weight(sector_name: str) -> dict:
    SECTOR_WEIGHTS = {
    "Technology": {
        "roic": 0.35,
        "fcf_5y_g": 0.20,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.25
                },
    "Financial services": {
        "roic": 0.45,
        "fcf_5y_g": 0.25,
        "gm_stability": 0.25,
        "rnd_to_rev": 0.05
                    },
    "Healthcare": {
        "roic": 0.30,
        "fcf_5y_g": 0.15,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.35
                    },
    "Consumer cyclical": {
        "roic": 0.35,
        "fcf_5y_g": 0.20,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.25
                },
    "Consumer defensive": {
        "roic": 0.35,
        "fcf_5y_g": 0.20,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.25
                    },
    "Communication services": {
        "roic": 0.35,
        "fcf_5y_g": 0.20,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.25
                    },
    "Industrials": {
        "roic": 0.35,
        "fcf_5y_g": 0.20,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.25
                },
    "Energy": {
        "roic": 0.35,
        "fcf_5y_g": 0.20,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.25
                    },
    "Utilities": {
        "roic": 0.35,
        "fcf_5y_g": 0.20,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.25
                    },
    "Basic materials": {
        "roic": 0.35,
        "fcf_5y_g": 0.20,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.25
                    },
    "Real estate": {
        "roic": 0.35,
        "fcf_5y_g": 0.20,
        "gm_stability": 0.20,
        "rnd_to_rev": 0.25
                    }
                    }
    
    sector_name = sector_name.lower().strip()

    if sector_name not in SECTOR_WEIGHTS:
        raise ValueError(f"Unsupported sector: sector {sector_name} is not defind in the system")
    return SECTOR_WEIGHTS[sector_name]


#for the total score weighting
def total_weight(sector_name: str) -> dict:
    pass

