
def fundamental_weight(sector_name: str) -> dict:
    
    SECTOR_WEIGHTS = {
    "Technology": {
        "revenue_growth": 0.30,
        "operating_margin": 0.30,
        "debt_to_equity": 0.20,
        "free_cash_flow": 0.20
                },
    "Financial Services": {
        "revenue_growth": 0.20,
        "operating_margin": 0.40,
        "debt_to_equity": 0.30,
        "free_cash_flow": 0.10
                    },
    "Consumer Cyclical": {
        "revenue_growth": 0.40,
        "operating_margin": 0.30,
        "debt_to_equity": 0.15,
        "free_cash_flow": 0.15
                    },
    "Communication Services": {
        "revenue_growth": 0.30,
        "operating_margin": 0.25,
        "debt_to_equity": 0.25,
        "free_cash_flow": 0.20
                    },
    "Healthcare": {
        "revenue_growth": 0.25,
        "operating_margin": 0.35,
        "debt_to_equity": 0.20,
        "free_cash_flow": 0.20
                },
    "Industrials": {
        "revenue_growth": 0.35,
        "operating_margin": 0.30,
        "debt_to_equity": 0.20,
        "free_cash_flow": 0.15
                },
    "Consumer Defensive": {
        "revenue_growth": 0.40,
        "operating_margin": 0.30,
        "debt_to_equity": 0.20,
        "free_cash_flow": 0.10
                    },
    "Energy": {
        "growth": 0.25,
        "operating_margin": 0.40,
        "debt_to_equity": 0.25,
        "free_cash_flow": 0.10
                    },
    "Basic Materials": {
        "growth": 0.25,
        "operating_margin": 0.40,
        "debt_to_equity": 0.25,
        "free_cash_flow": 0.10
                    },
    "Real Estate": {
        "growth": 0.20,
        "operating_margin": 0.35,
        "debt_to_equity": 0.30,
        "free_cash_flow": 0.15
                    },
    "Utilities": {
        "growth": 0.25,
        "operating_margin": 0.35,
        "debt_to_equity": 0.25,
        "free_cash_flow": 0.15
                    }
                    }

    sector_name = sector_name.lower().strip().title()

    if sector_name not in SECTOR_WEIGHTS:
        raise ValueError(f"Unsupported sector: sector {sector_name} is not defind in the system")
    return SECTOR_WEIGHTS[sector_name]
    
def valuation_weight(sector_name: str) -> dict:
    SECTOR_WEIGHTS = {
    "Technology": {
        "pe": 0.20,
        "forward_pe": 0.30,
        "ev_ebitda": 0.20,
        "ps": 0.20,
        "price_free_cash_flow": 0.10
                },
    "Financial Services": {
        "pe": 0.25,
        "forward_pe": 0.30,
        "ev_ebitda": 0.25,
        "ps": 0.10,
        "price_free_cash_flow": 0.10
                    },
    "Healthcare": {
        "pe": 0.30,
        "forward_pe": 0.25,
        "ev_ebitda": 0.25,
        "ps": 0.10,
        "price_free_cash_flow": 0.10
                    },
    "Consumer Cyclical": {
        "pe": 0.30,
        "forward_pe": 0.25,
        "ev_ebitda": 0.20,
        "ps": 0.15,
        "price_free_cash_flow": 0.10
                },
    "Consumer Defensive": {
        "pe": 0.30,
        "forward_pe": 0.25,
        "ev_ebitda": 0.20,
        "ps": 0.15,
        "price_free_cash_flow": 0.10
                    },
    "Communication Services": {
        "pe": 0.25,
        "forward_pe": 0.25,
        "ev_ebitda": 0.25,
        "ps": 0.15,
        "price_free_cash_flow": 0.10
                    },
    "Industrials": {
        "pe": 0.30,
        "forward_pe": 0.25,
        "ev_ebitda": 0.25,
        "ps": 0.15,
        "price_free_cash_flow": 0.05
                },
    "Energy": {
        "pe": 0.30,
        "forward_pe": 0.25,
        "ev_ebitda": 0.25,
        "ps": 0.15,
        "price_free_cash_flow": 0.05
                    },
    "Utilities": {
        "pe": 0.30,
        "forward_pe": 0.25,
        "ev_ebitda": 0.25,
        "ps": 0.15,
        "price_free_cash_flow": 0.05
                    },
    "Basic Materials": {
        "pe": 0.30,
        "forward_pe": 0.25,
        "ev_ebitda": 0.25,
        "ps": 0.15,
        "price_free_cash_flow": 0.05
                    },
    "Real Estate": {
        "pe": 0.30,
        "forward_pe": 0.25,
        "ev_ebitda": 0.25,
        "ps": 0.15,
        "price_free_cash_flow": 0.05
                    }
                    }
    
    sector_name = sector_name.lower().strip().title()

    if sector_name not in SECTOR_WEIGHTS:
        raise ValueError(f"Unsupported sector: sector {sector_name} is not defind in the system")
    return SECTOR_WEIGHTS[sector_name]

def moat_weight(sector_name: str) -> dict:
    SECTOR_WEIGHTS = {
    "Technology": {
        "roic": 0.45,
        "free_cash_flow_3y_cagr": 0.20,
        "rnd_to_revenue": 0.35
                },
    "Financial Services": {
        "roic": 0.55,
        "free_cash_flow_3y_cagr": 0.35,
        "rnd_to_revenue": 0.10
                    },
    "Healthcare": {
        "roic": 0.30,
        "free_cash_flow_3y_cagr": 0.20,
        "rnd_to_revenue": 0.50
                    },
    "Consumer Cyclical": {
        "roic": 0.40,
        "free_cash_flow_3y_cagr": 0.35,
        "rnd_to_revenue": 0.25
                },
    "Consumer Defensive": {
        "roic": 0.40,
        "free_cash_flow_3y_cagr": 0.40,
        "rnd_to_revenue": 0.20
                    },
    "Communication Services": {
        "roic": 0.40,
        "free_cash_flow_3y_cagr": 0.30,
        "rnd_to_revenue": 0.30
                    },
    "Industrials": {
        "roic": 0.45,
        "free_cash_flow_3y_cagr": 0.35,
        "rnd_to_revenue": 0.20
                },
    "Energy": {
        "roic": 0.35,
        "free_cash_flow_3y_cagr": 0.25,
        "rnd_to_revenue": 0.20
                    },
    "Utilities": {
        "roic": 0.45,
        "free_cash_flow_3y_cagr": 0.40,
        "rnd_to_revenue": 0.15
                    },
    "Basic Materials": {
        "roic": 0.45,
        "free_cash_flow_3y_cagr": 0.35,
        "rnd_to_revenue": 0.20
                    },
    "Real Estate": {
        "roic": 0.55,
        "free_cash_flow_3y_cagr": 0.40,
        "rnd_to_revenue": 0.05
                    }
                    }
    
    sector_name = sector_name.lower().strip().title()

    if sector_name not in SECTOR_WEIGHTS:
        raise ValueError(f"Unsupported sector: sector {sector_name} is not defind in the system")
    return SECTOR_WEIGHTS[sector_name]

#for the total score weighting
def final_score_weight(sector_name: str) -> dict:

    FINAL_WEIGHTS = {
    "Technology": {
        "f_weight": 0.25,
        "v_weight": 0.30,
        "m_weight": 0.45
                },
    "Financial Services": {
        "f_weight": 0.35,
        "v_weight": 0.40,
        "m_weight": 0.25
                    },
    "Healthcare": {
        "f_weight": 0.35,
        "v_weight": 0.25,
        "m_weight": 0.40
                    },
    "Consumer Cyclical": {
        "f_weight": 0.35,
        "v_weight": 0.40,
        "m_weight": 0.25
                },
    "Consumer Defensive": {
        "f_weight": 0.40,
        "v_weight": 0.35,
        "m_weight": 0.25
                    },
    "Communication Services": {
        "f_weight": 0.30,
        "v_weight": 0.30,
        "m_weight": 0.40
                    },
    "Industrials": {
        "f_weight": 0.35,
        "v_weight": 0.35,
        "m_weight": 0.30
                },
    "Energy": {
        "f_weight": 0.35,
        "v_weight": 0.40,
        "m_weight": 0.25
                    },
    "Utilities": {
        "f_weight": 0.40,
        "v_weight": 0.35,
        "m_weight": 0.25
                    },
    "Basic Materials": {
        "f_weight": 0.35,
        "v_weight": 0.40,
        "m_weight": 0.25
                    },
    "Real Estate": {
        "f_weight": 0.30,
        "v_weight": 0.45,
        "m_weight": 0.25
                    }}
    
    sector_name = sector_name.lower().strip().title()

    if sector_name not in FINAL_WEIGHTS:
        raise ValueError(f"Unsupported sector: sector {sector_name} is not defind in the system")
    return FINAL_WEIGHTS[sector_name]

