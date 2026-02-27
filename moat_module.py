from scoring_utils import ScoringMethods
from config import moat_weight
from dotenv import load_dotenv
import json

load_dotenv()

ROIC_THRESHOLDS = [
    (3, 20),    
    (7, 40),    
    (12, 60),   
    (18, 80),   
    (25, 90),   
                    ]
ROIC_DEFAULT = 98   

FCF_3Y_CAGR_THRESHOLDS = [
    (0, 20),    
    (5, 40),    
    (10, 60),   
    (20, 80),   
    (30, 90),   
                            ]
FCF_3Y_CAGR_DEFAULT = 98  

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

#creating objects so i can use them as objects in this file
roic_scorer = ScoringMethods(
    ROIC_THRESHOLDS,
    ROIC_DEFAULT)

fcf_3y_cagr_scorer = ScoringMethods(
    FCF_3Y_CAGR_THRESHOLDS,
    FCF_3Y_CAGR_DEFAULT)

gm_stability_scorer = ScoringMethods(
    GM_STABILITY_THRESHOLDS,
    GM_STABILITY_DEFAULT)

rnd_revenue_scorer = ScoringMethods(
    RND_TO_REVENUE_RATIO_THRESHOLDS,
    RND_TO_REVENUE_RATIO_DEFAULT)

def fetch_moat_data_from_api(ticker) -> dict:
    """
    opening .json file and fetching moat financial metrics:
    -retrun on investment capital
    -free cash flow 3 year cagr
    -gross margin stability
    -r&d to revenue ratio
        
    """
    clean_ticker = ticker.strip().upper()
    
    file_path_1 = f"data_reports/json_file_1_{clean_ticker}.json"
    with open(file_path_1, "r", encoding="utf-8") as f:
            file_1 = json.load(f)

    file_path_3= f"data_reports/json_file_3_{clean_ticker}.json"
    with open(file_path_3, "r", encoding="utf-8") as f:
            file_3 = json.load(f)

    file_path_4= f"data_reports/json_file_3_{clean_ticker}.json"
    with open(file_path_4, "r", encoding="utf-8") as f:
            file_4 = json.load(f)

    #ROIC:

    #Return on Invested Capital (ROIC) = nopat / invested Capital
    #nopat = Operating Income(ebit) * (1 - tax Rate)
    #ebit = operating margin * revenue
    #Invested Capital = total Debt + total Equity - total cash
    
    total_debt = file_3["body"]["debt"]["TTM"]
    total_equity = file_3["body"]["equity"]["TTM"]
    total_cash = file_3["body"]["totalcash"]["TTM"]
    invested_capital = total_debt + total_equity - total_cash

    operating_margin_raw = (file_1["quoteSummary"]["result"][0]
            ["financialData"]["operatingMargins"]["raw"])
    
    revenue = (file_1["quoteSummary"]["result"][0]
            ["financialData"]["totalRevenue"]["raw"])
    
    ebit = operating_margin_raw * revenue
    tax_rate = 0.21
    nopat = ebit * (1 - tax_rate)
    #multipling by 100 to get metric in %
    return_on_investment_capital_pct = nopat / invested_capital * 100 


    #FCF_3Y_CAGR:

    #FCF_3Y_CAGR = Compound-Annual-Growth-Rate of Free Cash Flow 
    #FCF_3Y_CAGR = (free cash_flow_latest / free_cash_flow_3_years_ago)^(1/3) - 1
    annual_fcf = (file_4["quoteSummary"]["result"][0]["timeseries"]["annualFreeCashFlow"])

    annual_fcf_sorted = sorted(
        annual_fcf,
        key=lambda x: x["asOfDate"]
    )

    free_cash_flow_3y_cagr = None

    if len(annual_fcf_sorted) >= 4:

        free_cash_flow_latest = annual_fcf_sorted[-1]["reportedValue"]["raw"]
        free_cash_flow_3_years_ago = annual_fcf_sorted[-4]["reportedValue"]["raw"]

        if free_cash_flow_3_years_ago != 0:
            free_cash_flow_3y_cagr = (free_cash_flow_latest / free_cash_flow_3_years_ago) ** (1/3) - 1

    #GROSS MARGIN STABILITY: get from API



    #R&D TO REVENUE RATIO: get from API


    return {
        "return_on_investment_capital_pct": return_on_investment_capital_pct,
        "free_cash_flow_3y_cagr": free_cash_flow_3y_cagr,
        "gross_margin_stability": gross_margin_stability,
        "r_and_d_to_revenue": r_and_d_to_revenue
    }

def moat_weighted_score(
    roic: int,
    fcf_3y_cagr: int,
    gm: int,
    rnd: int,
    wbs: dict
                        ) -> int:
    
    roic_weight = wbs['roic']
    fcf_3y_cagr_weight = wbs['free_cash_flow_3y_cagr']
    gm_weight = wbs['gm_stability']
    rnd_weight = wbs['rnd_to_revenue']

    weighted_together = (roic_weight * roic + fcf_3y_cagr_weight * fcf_3y_cagr + gm_weight * gm + rnd_weight * rnd)
    return round(weighted_together)

def calculate_moat_scores(
    return_on_investment_capital: float,
    fcf_3y_cagr: float,
    gross_margin_list: list,
    rnd_raw: float,
    revenue_growth_raw:float,
    sector_name: str
                        ) -> dict:   
    """
    Core function of the moat module.
    Gets raw inputs and returns all scores + final moat_score.
    """

    #calling a specific function from the Class in scoring_utils.py
    return_on_investment_capital = roic_scorer.threshold_based_score(return_on_investment_capital)
    fcf_3y_cagr = fcf_3y_cagr_scorer.threshold_based_score(fcf_3y_cagr)

    gm_range = max(gross_margin_list) - min(gross_margin_list)
    gm_stability = gm_stability_scorer.threshold_based_score(gm_range)

    rnd = rnd_raw/revenue_growth_raw * 100
    rnd_to_revenue = rnd_revenue_scorer.threshold_based_score(rnd)

    weight_by_sector = moat_weight(sector_name)
    
    final_score = moat_weighted_score(
    return_on_investment_capital, fcf_3y_cagr, gm_stability, rnd, weight_by_sector)

    #change names
    return {
        "roic_score": return_on_investment_capital,
        "fcf_3y_cagr_score": fcf_3y_cagr,
        "gm_stability_score": gm_stability,
        "rnd_to_revenue_score": rnd_to_revenue,
        "weight_currently_being_used": weight_by_sector,
        "moat_score": final_score
            }

