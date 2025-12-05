
from scoring_utils import score_by_thresholds

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

DER_THRESHOLDS = [
    (0.2, 95), 
    (0.5, 80),  
    (1.0, 60), 
    (2.0, 40),
                 ]
DER_DEFAULT = 20

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

def der_score(debt_to_eqity: float) -> int:
    return score_by_thresholds(debt_to_eqity,DER_THRESHOLDS,DER_DEFAULT)

def fcf_margin_score(free_cash_flow: float) -> int:
    return score_by_thresholds(free_cash_flow,FCF_MARGIN_THRESHOLDS,FCF_MARGIN_DEFAULT)


def fundamental_weighted_score(g: int, p: int, d: int, f: int) -> int:
    """
    Calculates the final fundamentals score using fixed weights:
    growth - 30%
    profit - 30%
    D/E    - 20%
    FCF    - 20%
    """
    weighted_together = (0.3 * g + 0.3 * p + 0.2 * d + 0.2 * f)
    return round(weighted_together)

def calculate_fundamental_scores(
    growth_pct: float,
    profit_pct: float,
    debt_to_equity: float,
    fcf_margin_pct: float,
                                    ) -> dict:   
    """
    Core function of the fundamentals module.
    Gets raw inputs and returns all scores + final fundamentals_score.
    """
    g = growth_score(growth_pct)
    p = profit_score(profit_pct)
    d = der_score(debt_to_equity)
    f = fcf_margin_score(fcf_margin_pct)

    final_score = fundamental_weighted_score(g, p, d, f)

    return {
        "Growth_score": g,
        "Profit_score": p,
        "Debt_to_Equity_score": d,
        "Free_Cash_Flow_margin_score": f,
        "Fundamentals_Score (range of 1-100)": final_score,
            }




