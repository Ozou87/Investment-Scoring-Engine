from scoring_utils import threshold_based_score
from config import fundamental_weight
from dotenv import load_dotenv
import json

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

def fetch_fundamental_data_from_api(ticker) -> dict:
    """
    opening file_1 and fetching fundamental financial metrics:
        -revenue growth pct
        -operating margin pct
        -debt/equity ratio
        -free cash flow margin pct
    """
    clean_ticker = ticker.strip().upper()
    file_path_1 = f"data_reports/json_file_1_{clean_ticker}.json"
    with open(file_path_1, "r", encoding="utf-8") as f:
            file_1 = json.load(f)

    #Quarterly Revenue Growth (yoy) = ( (New Quarter Revenue - Same Quarter Last Year Revenue) / Same Quarter Last Year Revenue ) * 100
    #multipling by 100 to get metric in %
    revenue_growth_raw = (file_1["quoteSummary"]["result"][0]
            ["financialData"]["revenueGrowth"]["raw"]
        )
    revenue_growth_pct = revenue_growth_raw * 100
    
    #operating margin (ttm) = Operating Income (EBIT) / Revenue
    #multipling by 100 to get metric in %
    operating_margin_raw = (file_1["quoteSummary"]["result"][0]
            ["financialData"]["operatingMargins"]["raw"]
        )
    operating_margin_pct = operating_margin_raw * 100

    #debt to equity = Total Debt / Total Shareholders' Equity
    debt_to_equity_ratio = (file_1["quoteSummary"]["result"][0]
            ["financialData"]["debtToEquity"]["raw"])

    #FREE CASH FLOW MARGIN(TTM)% = Levered free cash flow(ttm) / Revenue(ttm) * 100 
    #multipling by 100 to get metric in %
    revenue = (file_1["quoteSummary"]["result"][0]
            ["financialData"]["totalRevenue"]["raw"])
    
    levered_free_cash_flow = (file_1["quoteSummary"]["result"][0]
            ["financialData"]["freeCashflow"]["raw"])
    
    free_cash_flow_margin_pct = (levered_free_cash_flow / revenue) * 100

    return {
        "revenue_growth_pct": revenue_growth_pct,
        "operating_margin_pct": operating_margin_pct,
        "debt_to_equity_ratio": debt_to_equity_ratio,
        "free_cash_flow_margin_pct": free_cash_flow_margin_pct
    }


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




