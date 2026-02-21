from scoring_utils import threshold_based_score
from config import moat_weight
from dotenv import load_dotenv
import json

load_dotenv()

def fetch_moat_data_from_api(ticker) -> dict:
    """
    fetching moat financial metrics:
        -retrun on investment capital
        -free cash flow 3 year cagr
        -gross margin stability
        -r&d to revenue ratio
        
    """
    clean_ticker = ticker.strip().upper()

    file_path_3= f"data_reports/json_file_3_{clean_ticker}.json"
    with open(file_path_3, "r", encoding="utf-8") as f:
            file_3 = json.load(f)
    
    file_path_1 = f"data_reports/json_file_1_{clean_ticker}.json"
    with open(file_path_1, "r", encoding="utf-8") as f:
            file_1 = json.load(f)

    #Return on Invested Capital (ROIC) = NOPAT / Invested Capital
    #multipling by 100 to get metric in %
    #NOPAT = Operating Income(EBIT) * (1 - Tax Rate)
    #EBIT = operating margin * Revenue
    #Invested Capital = Total Debt + Total Equity - Cash
    
    total_debt = ["body"]["debt"]["TTM"]
    total_equity = moat_data_1["body"]["equity"]["TTM"]
    total_cash = moat_data_1["body"]["totalcash"]["TTM"]
    invested_capital = total_debt + total_equity - total_cash

    #get from fundamental module or api (consider function for api)

    operating_margin_raw = (file_1["quoteSummary"]["result"][0]
            ["financialData"]["operatingMargins"]["raw"])
    
    revenue = (file_1["quoteSummary"]["result"][0]
            ["financialData"]["totalRevenue"]["raw"])
    
    ebit = operating_margin_raw * revenue
    tax_rate = 0.21
    nopat = ebit * (1 - tax_rate)
    return_on_investment_capital_pct = nopat / invested_capital * 100 




    return {
        "return_on_investment_capital_pct": return_on_investment_capital_pct,
        "operating_margin_pct": operating_margin_pct,
        "debt_to_equity_ratio": debt_to_equity_ratio,
        "free_cash_flow_margin_pct": free_cash_flow_margin_pct
    }

RETURN_ON_INVESTMENT_CAPITAL_THRESHOLDS = [
    (3, 20),    
    (7, 40),    
    (12, 60),   
    (18, 80),   
    (25, 90),   
                    ]
RETURN_ON_INVESTMENT_CAPITAL_DEFAULT = 98   

FCF_3Y_GROWTH_THRESHOLDS = [
    (0, 20),    
    (5, 40),    
    (10, 60),   
    (20, 80),   
    (30, 90),   
                            ]
FCF_3Y_GROWTH_DEFAULT = 98  

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
    return threshold_based_score(roic_5y_avg, RETURN_ON_INVESTMENT_CAPITAL_THRESHOLDS, RETURN_ON_INVESTMENT_CAPITAL_DEFAULT)

def fcf_growth_score(fcf_3y_growth: float) -> int:
    return threshold_based_score(fcf_3y_growth, FCF_3Y_GROWTH_THRESHOLDS, FCF_3Y_GROWTH_DEFAULT)

def gross_m_stability_score(gm_list: list[float]) -> int:
    gm_range = max(gm_list) - min(gm_list)
    return threshold_based_score(gm_range,GM_STABILITY_THRESHOLDS,GM_STABILITY_DEFAULT)

def rnd_revenue_score(rnd: float, revenue:float) -> int:
    r_and_d_ratio = (rnd/revenue) * 100
    return threshold_based_score(r_and_d_ratio,RND_TO_REVENUE_RATIO_THRESHOLDS,RND_TO_REVENUE_RATIO_DEFAULT)

def moat_weighted_score(
    roic: int,
    fcf_3y_g: int,
    gm: int,
    rnd: int,
    wbs: dict
                        ) -> int:
    
    roic_weight = wbs['roic']
    fcf_3y_g_weight = wbs['free_cash_flow_3y_g']
    gm_weight = wbs['gm_stability']
    rnd_weight = wbs['rnd_to_rev']

    weighted_together = (roic_weight * roic + fcf_3y_g_weight * fcf_3y_g + gm_weight * gm + rnd_weight * rnd)
    return round(weighted_together)

def calculate_moat_scores(
    roic_raw_value: float,
    fcf_growth_raw: float,
    gross_margin_list: list,
    r_and_d_raw: float,
    revenue_growth_raw:float,
    sector_name: str
                        ) -> dict:   
    """
    Core function of the moat module.
    Gets raw inputs and returns all scores + final moat_score.
    """
    roic = roic_score(roic_raw_value)
    fcf = fcf_growth_score(fcf_growth_raw)
    gm = gross_m_stability_score(gross_margin_list)
    rnd = rnd_revenue_score(r_and_d_raw, revenue_growth_raw)
    weight_by_sector = moat_weight(sector_name)
    

    final_score = moat_weighted_score(roic, fcf, gm, rnd, weight_by_sector)

    return {
        "roic_score": roic,
        "gm_stability_score": gm,
        "fcf_growth_score": fcf,
        "rnd_to_revenue_score": rnd,
        "weight_currently_being_used": weight_by_sector,
        "moat_score": final_score
            }