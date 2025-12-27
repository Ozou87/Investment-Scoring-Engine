
from scoring_utils import score_by_thresholds
from config import fundamental_weight

#creating table with limits and score limits
GROWTH_THRESHOLDS = [
    (0.0,20),
    (5.0,40),
    (15.0,60),
    (30.0,80),
                    ]
GROWTH_DEFAULT = 95

PROFIT_THRESHOLDS = [
    (0.0,20),
    (5.0,40),
    (15.0,60),
    (25,80),
                    ]
PROFIT_DEFAULT = 95

DTE_THRESHOLDS = [
    (0.2, 95), 
    (0.5, 80),  
    (1.0, 60), 
    (2.0, 40),
                 ]
DTE_DEFAULT = 20

FCF_MARGIN_THRESHOLDS = [
    (0, 20),
    (5, 40),
    (10, 60),
    (20, 80),
                ]
FCF_MARGIN_DEFAULT = 95

#specific function that sends info to the generic function in order to help it find score
def growth_score(growth_pct: float) -> int:
    return score_by_thresholds(growth_pct, GROWTH_THRESHOLDS, GROWTH_DEFAULT)

def profit_score(profit_pct: float) -> int:
    return score_by_thresholds(profit_pct,PROFIT_THRESHOLDS,PROFIT_DEFAULT)

def dte_score(debt_to_eqity: float) -> int:
    return score_by_thresholds(debt_to_eqity,DTE_THRESHOLDS,DTE_DEFAULT)

def fcf_margin_score(free_cash_flow: float) -> int:
    return score_by_thresholds(free_cash_flow,FCF_MARGIN_THRESHOLDS,FCF_MARGIN_DEFAULT)

def fundamental_weighted_score(
        g: int,
        p: int,
        d: int,
        f: int,
        wbs: dict
                            ) -> int:

    growth_weight = wbs['growth']          
    profit_weight = wbs['profit']          
    dte_weight = wbs['debt_to_equity']      
    fcf_weight = wbs['fcf']                

    weighted_together = (growth_weight * g + profit_weight * p + dte_weight * d + fcf_weight * f)
    return round(weighted_together)

def calculate_fundamental_scores(
    growth_pct: float,
    profit_pct: float,
    debt_to_equity: float,
    fcf_margin_pct: float,
    sector_name: str
                                    ) -> dict:   
    """
    Core function of the fundamentals module.
    Gets raw inputs and returns all scores + final fundamentals_score.
    """
    g = growth_score(growth_pct)
    p = profit_score(profit_pct)
    d = dte_score(debt_to_equity)
    f = fcf_margin_score(fcf_margin_pct)
    weight_by_sector = fundamental_weight(sector_name)

    final_score = fundamental_weighted_score(g, p, d, f, weight_by_sector)

    return {
        "Growth_score": g,
        "Profit_score": p,
        "Debt_to_Equity_score": d,
        "Free_Cash_Flow_margin_score": f,
        "weight_currently_being used": weight_by_sector,
        "Fundamentals_Score (range of 1-100)": final_score
            }




