
from scoring_utils import score_by_thresholds

ROIC_THRESHOLDS = [
    (3, 20),    
    (7, 40),    
    (12, 60),   
    (18, 80),   
    (25, 90),   
                    ]
ROIC_DEFAULT = 98   

FCF_5Y_GROWTH_THRESHOLDS = [
    (0, 20),    
    (5, 40),    
    (10, 60),   
    (20, 80),   
    (30, 90),   
                            ]
FCF_5Y_GROWTH_DEFAULT = 98  

GM_STABILITY_THRESHOLDS = [
    (2, 90),    
    (5, 80),    
    (10, 60),   
    (15, 40),   
                            ]
GM_STABILITY_DEFAULT = 25

RND_TO_REVENUE_RATIO_THRESHOLDS = [
    (3, 25),     
    (7, 40),     
    (12, 60),    
    (20, 80),    
    (30, 90),    
                            ]
RND_TO_REVENUE_RATIO_DEFAULT = 98   

def roic_score(roic_5y_avg: float) -> int:
    return score_by_thresholds(roic_5y_avg, ROIC_THRESHOLDS, ROIC_DEFAULT)

def fcf_growth_score(fcf_5y_growth: float) -> int:
    return score_by_thresholds(fcf_5y_growth, FCF_5Y_GROWTH_THRESHOLDS, FCF_5Y_GROWTH_DEFAULT)

def gross_m_stability_score(gm_list: list[float]) -> int:
    gm_range = max(gm_list) - min(gm_list)
    return score_by_thresholds(gm_range,GM_STABILITY_THRESHOLDS,GM_STABILITY_DEFAULT)

def rnd_revenue_score(rnd: float, revenue:float) -> int:
    r_and_d_ratio = (rnd/revenue) * 100
    return score_by_thresholds(r_and_d_ratio,RND_TO_REVENUE_RATIO_THRESHOLDS,RND_TO_REVENUE_RATIO_DEFAULT)

def moat_weighted_score(roic: int, fcf: int, gm: int, rnd: int) -> int:
    """
    Calculates the final moat score using fixed weights:
    ROIC            - 40%
    FCF_GROWTH      - 30%
    GrossMargin     - 20%
    R&D             - 10%
    """
    weighted_together = (0.4 * roic + 0.3 * fcf + 0.2 * gm + 0.1 * rnd)
    return round(weighted_together)

def calculate_moat_scores(
    roic_raw_value: float,
    fcf_growth_raw: float,
    gross_margin_list: float,
    r_and_d_raw: float,
                        ) -> dict:   
    """
    Core function of the moat module.
    Gets raw inputs and returns all scores + final moat_score.
    """
    roic = roic_score(roic_raw_value)
    fcf = fcf_growth_score(fcf_growth_raw)
    gm = gross_m_stability_score(gross_margin_list)
    rnd = rnd_revenue_score(r_and_d_raw)

    final_score = moat_weighted_score(roic, fcf, gm, rnd)

    return {
        "Growth_score": roic,
        "Profit_score": fcf,
        "Debt_to_Equity_score": gm,
        "Free_Cash_Flow_margin_score": rnd,
        "Moat_Score (range of 1-100)": final_score,
            }
