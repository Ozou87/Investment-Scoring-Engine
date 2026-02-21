from scoring_utils import threshold_based_score
from config import fundamental_weight
from dotenv import load_dotenv

load_dotenv()

#creating table with limits and score limits
REVENUE_GROWTH_THRESHOLDS = [
    (0.0,20),
    (5.0,40),
    (15.0,60),
    (30.0,80),
                    ]
REVENUE_GROWTH_DEFAULT = 95

OPERATING_MARGIN_THRESHOLDS = [
    (0.0,20),
    (5.0,40),
    (15.0,60),
    (25.0,80),
                    ]
OPERATING_MARGIN_DEFAULT = 95

DEBT_TO_EQUITY_THRESHOLDS = [
    (0.2, 95), 
    (0.5, 80),  
    (1.0, 60), 
    (2.0, 40),
                 ]
DEBT_TO_EQUITY_DEFAULT = 20

FREE_CASH_FLOW_THRESHOLDS = [
    (0, 20),
    (5, 40),
    (10, 60),
    (20, 80),
                ]
FREE_CASH_FLOW_DEFAULT = 95

def fetch_fundamental_data_from_api():
    with open(file_path, "r", encoding="utf-8") as f:
            json.dump(fundamental_data, f, indent=2)



#specific function that sends info to the generic function in order to help it find score
def revenue_score(revenue_growth_pct: float) -> int:
    return threshold_based_score(revenue_growth_pct, REVENUE_GROWTH_THRESHOLDS, REVENUE_GROWTH_DEFAULT)

def operating_margin_score(operating_margin_pct: float) -> int:
    return threshold_based_score(operating_margin_pct, OPERATING_MARGIN_THRESHOLDS, OPERATING_MARGIN_DEFAULT)

def debt_to_equity_score(debt_to_equity: float) -> int:
    return threshold_based_score(debt_to_equity, DEBT_TO_EQUITY_THRESHOLDS, DEBT_TO_EQUITY_DEFAULT)

def free_cash_flow_score(free_cash_flow_margin_pct: float) -> int:
    return threshold_based_score(free_cash_flow_margin_pct, FREE_CASH_FLOW_THRESHOLDS, FREE_CASH_FLOW_DEFAULT)

def fundamental_weighted_score(
        revenue_growth: int,
        operating_margin: int,
        debt_to_equity: int,
        free_cash_flow: int,
        wbs: dict
                            ) -> int:
    
    #FIX
    revenue_growth_weight = wbs['revenue_growth']      
    operating_margin_weight = wbs['operating_margin']   
    debt_to_equity_weight = wbs['debt_to_equity'] 
    free_cash_flow_weight = wbs['free_cash_flow']      

    #FIX
    weighted_together = (
    revenue_growth_weight * revenue_growth + operating_margin_weight * operating_margin + debt_to_equity_weight * debt_to_equity + free_cash_flow_weight * free_cash_flow)
    
    return round(weighted_together)

def calculate_fundamental_scores(
    revenue_growth_pct: float,
    operating_margin_pct: float,
    debt_to_equity_ratio: float,
    free_cash_flow_margin_pct: float,
    sector_name: str
                                    ) -> dict:   
    """
    Core function of the fundamentals module.
    Gets raw inputs and returns all scores + final fundamentals_score.
    """
    revenue_growth = revenue_score(revenue_growth_pct)
    operating_margin = operating_margin_score(operating_margin_pct)
    debt_to_equity = debt_to_equity_score(debt_to_equity_ratio)
    free_cash_flow = free_cash_flow_score(free_cash_flow_margin_pct)
    weight_by_sector = fundamental_weight(sector_name)

    final_score = fundamental_weighted_score(
    revenue_growth, operating_margin, debt_to_equity, free_cash_flow, weight_by_sector)

    return {
        "revenue_score": revenue_growth,
        "operating_margin_score": operating_margin,
        "debt_to_equity_score": debt_to_equity,
        "fcf_score": free_cash_flow,
        "sector_name": sector_name,
        "weight_currently_being_used": weight_by_sector,
        "fundamentals_score": final_score
            }




