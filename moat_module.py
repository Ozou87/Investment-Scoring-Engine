
from scoring_utils import score_ratio
from scoring_utils import score_by_thresholds
ROIC_THRESHOLDS = [
    (3, 20),    
    (7, 40),    
    (12, 60),   
    (18, 80),   
    (25, 90),   
                    ]
ROIC_DEFAULT_SCORE = 98   

GM_STABILITY_THRESHOLDS = [
    (2, 90),    
    (5, 80),    
    (10, 60),   
    (15, 40),   
                            ]
GM_STABILITY_DEFAULT_SCORE = 25

FCF_5Y_GROWTH_THRESHOLDS = [
    (0, 20),    
    (5, 40),    
    (10, 60),   
    (20, 80),   
    (30, 90),   
                            ]
FCF_5Y_GROWTH_DEFAULT_SCORE = 98  


def roic(roic_5y_avg: float) -> int:
    return score_ratio(roic_5y_avg, ROIC_THRESHOLDS, ROIC_DEFAULT_SCORE)

def gm_stability_score(gm_list: list[float]) -> int:
    gm_range = max(gm_list) - min(gm_list)
    return score_by_thresholds(gm_range,GM_STABILITY_THRESHOLDS,GM_STABILITY_DEFAULT_SCORE)

