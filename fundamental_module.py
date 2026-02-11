
from scoring_utils import score_by_thresholds
from config import fundamental_weight

#creating table with limits and score limits
REVENUE_GROWTH_YOY_THRESHOLDS = [
    (0.0,20),
    (5.0,40),
    (15.0,60),
    (30.0,80),
                    ]
REVENUE_GROWTH_YOY_DEFAULT = 95

GROSS_MARGIN_TTM_THRESHOLDS = [
    (0.0,20),
    (5.0,40),
    (15.0,60),
    (25.0,80),
                    ]
GROSS_MARGIN_TTM_DEFAULT = 95

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
def revenue_growth_yoy_score(revenue_growth_yoy: float) -> int:
    return score_by_thresholds(revenue_growth_yoy, REVENUE_GROWTH_YOY_THRESHOLDS, REVENUE_GROWTH_YOY_DEFAULT)

def gross_margin_ttm_score(gross_margin_ttm: float) -> int:
    return score_by_thresholds(gross_margin_ttm, GROSS_MARGIN_TTM_THRESHOLDS, GROSS_MARGIN_TTM_DEFAULT)

def dte_score(debt_to_equity: float) -> int:
    return score_by_thresholds(debt_to_equity, DTE_THRESHOLDS, DTE_DEFAULT)

def fcf_margin_score(free_cash_flow_margin_ttm: float) -> int:
    return score_by_thresholds(free_cash_flow_margin_ttm, FCF_MARGIN_THRESHOLDS, FCF_MARGIN_DEFAULT)

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
    revenue_growth_yoy: float,
    gross_margin_ttm: float,
    debt_to_equity: float,
    free_cash_flow_margin_ttm: float,
    sector_name: str
                                    ) -> dict:   
    """
    Core function of the fundamentals module.
    Gets raw inputs and returns all scores + final fundamentals_score.
    """
    g = revenue_growth_yoy_score(revenue_growth_yoy)
    p = gross_margin_ttm_score(gross_margin_ttm)
    d = dte_score(debt_to_equity)
    f = fcf_margin_score(free_cash_flow_margin_ttm)
    weight_by_sector = fundamental_weight(sector_name)

    final_score = fundamental_weighted_score(g, p, d, f, weight_by_sector)

    return {
        "revenue_growth_yoy_score": g,
        "profit_score": p,
        "debt_to_Equity_score": d,
        "free_Cash_Flow_margin_score": f,
        "sector_name": sector_name,
        "weight_currently_being_used": weight_by_sector,
        "fundamentals_score": final_score
            }




