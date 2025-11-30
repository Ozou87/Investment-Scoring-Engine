
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

FCF_THRESHOLDS = [
    (0, 20),
    (5, 40),
    (10, 60),
    (20, 80),
                ]
FCF_DEFAULT = 95



#specific function that sends info to the generic function in order to help it find score
def growth_score(growth_pct: float) -> int:
    return score_by_thresholds(growth_pct, GROWTH_THRESHOLDS, GROWTH_DEFAULT)

def profit_score(profit_pct: float) -> int:
    return score_by_thresholds(profit_pct,PROFIT_THRESHOLDS,PROFIT_DEFAULT)

def der_score(debt_to_eqity: float) -> int:
    return score_by_thresholds(debt_to_eqity,DER_THRESHOLDS,DER_DEFAULT)

def fcf_score(free_cash_flow: float) -> int:
    return score_by_thresholds(free_cash_flow,FCF_THRESHOLDS,FCF_DEFAULT)

#funcion that calculate the weighted of all results and bring back final score
def fundemental_score(g:int, p:int, d:int, f:int) -> int:

    weighted_together = (0.3 * g + 0.3 * p + 0.2 * d + 0.2 * f)
    return round(weighted_togethe)


