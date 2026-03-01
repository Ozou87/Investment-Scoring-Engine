from scoring_utils import ScoringMethods
from config import valuation_weight
from dotenv import load_dotenv
from api_caller import create_financial_file_2 
import json
import os
import pandas as pd
import statistics

load_dotenv()

#creating table with limits and score limits
PE_INVALID = float('nan')
PE_THRESHOLDS = [
    (0.6,95),
    (0.85,80),
    (1.15,50),
    (1.5,30),
    (2.0,15),
                    ]
PE_DEFAULT = 0

FORWARD_PE_INVALID = float('nan')
FORWARD_PE_THRESHOLDS = [
    (0.60,95),
    (0.80,90),
    (0.90,75),
    (1.10,55),
    (1.30,40),
    (1.60,25),
    (2.00,15),
            ]
FORWARD_PE_DEFAULT = 5

EV_EBITDA_INVALID = float('nan')
EV_EBITDA_THRESHOLDS = [
    (0.70, 95),   
    (0.90, 85),   
    (1.10, 60),   
    (1.40, 40),   
    (2.00, 25),  
    (3.00, 15),   
                            ]
EV_EBITDA_DEFAULT = 5 

PS_INVALID = float('nan')
PS_THRESHOLDS = [
    (0.70, 95), 
    (0.90, 85),    
    (1.10, 60),   
    (1.40, 40),   
    (2.00, 25),   
    (3.00, 15),  
                    ]
PS_DEFAULT = 5     

P_FCF_INVALID = float('nan')
P_FCF_THRESHOLDS = [
    (0.70, 95),   
    (0.90, 85),  
    (1.10, 60),   
    (1.40, 40),   
    (2.00, 25),   
    (3.00, 15), 
                        ]
P_FCF_DEFAULT = 5  

#creating objects so i can use them as objects in this file
pe_scorer = ScoringMethods(
    PE_THRESHOLDS,
    PE_DEFAULT)

forward_pe_scorer = ScoringMethods(
    FORWARD_PE_THRESHOLDS,
    FORWARD_PE_DEFAULT)

ev_ebitda_scorer = ScoringMethods(
    EV_EBITDA_THRESHOLDS,
    EV_EBITDA_DEFAULT)

ps_scorer = ScoringMethods(
    PS_THRESHOLDS,
    PS_DEFAULT)

p_fcf_scorer = ScoringMethods(
    P_FCF_THRESHOLDS,
    P_FCF_DEFAULT)

def fetch_valuation_data_from_api(ticker) -> dict:
    """
    opening .json file and fetching valuation financial metrics:
        -stock_pe
        -stock forward pe
        -stock ev/ebitda multiple
        -stock p/s multiple
        -stock price/free cash flow multiple
    """
    clean_ticker = ticker.strip().upper()

    file_path_2 = f"data_reports/json_file_2_{clean_ticker}.json"
    with open(file_path_2, "r", encoding="utf-8") as f:
            file_2 = json.load(f)

    #P/E = current price / EPS (TTM)
    current_price = file_2["financialData"]["currentPrice"]
    eps_ttm = file_2["defaultKeyStatistics"]["trailingEps"]
    stock_pe = current_price / eps_ttm

    #Forward P/E = Current Price / Expected EPS (Next 12 Months)
    stock_forward_pe = file_2["defaultKeyStatistics"]["forwardPE"]

    #ev = Enterprise Value = market cap + (total debt - cash & cash equivalents)
    #ebitda = Earnings Before Interest, Taxes, Depreciation & Amortization = operating income(EBIT) + depreciation + amoritization
    #EV/EBITA MULTIPE = Enterprise Value / Ebitda
    ev_ebitda_multiple = file_2["defaultKeyStatistics"]["enterpriseToEbitda"]
    
    #Price/Sales = Market Cap / Revenue (ttm)
    stock_price_to_sales_multiple = file_2["summaryDetail"]["priceToSalesTrailing12Months"]

    #Price to Free Cash Flow multiple = Market Cap / Free Cash Flow
    stock_market_cap = file_2["summaryDetail"]["marketCap"]
    stock_free_cash_flow = file_2["financialData"]["freeCashflow"]
    stock_price_to_free_cash_flow_multiple = stock_market_cap / stock_free_cash_flow

    return {
        "pe": stock_pe,
        "forward_pe": stock_forward_pe,
        "ev_ebitda_multiple": ev_ebitda_multiple,
        "price_to_sales_multiple": stock_price_to_sales_multiple,
        "price_to_free_cash_flow_multiple": stock_price_to_free_cash_flow_multiple
    }

def calculate_sector_median(sector_metrics: dict, metric_name: str):
    values = [
        data[metric_name]
        for data in sector_metrics.values()
        if data.get(metric_name) is not None
    ]
    return statistics.median(values)

def fetch_sector_valuation_data(sector: str):
    """
    fetching sector_valuation financial metrics:
        -sector pe
        -sector forward pe
        -sector ev/ebitda multiple
        -sector p/s multiple
        -sector price/free cash flow multiple
    """
    #creating dict which connecting SECTOR NAME to SECTOR FILE NAME
    SECTOR_FILE_MAP = {
        "Basic Materials": "holdings-daily-us-en-xlb.xlsx",
        "Communication Services": "holdings-daily-us-en-xlc.xlsx",
        "Energy": "holdings-daily-us-en-xle.xlsx",
        "Financial Services": "holdings-daily-us-en-xlf.xlsx",
        "Industrials": "holdings-daily-us-en-xli.xlsx",
        "Technology": "holdings-daily-us-en-xlk.xlsx",
        "Consumer Defensive": "holdings-daily-us-en-xlp.xlsx",
        "Real Estate": "holdings-daily-us-en-xlre.xlsx",
        "Utilities": "holdings-daily-us-en-xlu.xlsx",
        "Healthcare": "holdings-daily-us-en-xlv.xlsx",
        "Consumer Cyclical": "holdings-daily-us-en-xly.xlsx",
    }
    
    #using the dict to find the right file name
    file_name = SECTOR_FILE_MAP.get(sector)

    #if file name=None -> raise Error
    if not file_name:
        raise ValueError(f"No benchmark file found for sector: {sector}")
    
    #creating full path using 'os'
    file_path = os.path.join("sector_reports_10-2-26", file_name)

    df_raw = pd.read_excel(file_path, skiprows=3)

    header = df_raw.iloc[0].tolist()
    df = df_raw.iloc[1:].copy()
    df.columns = header

    #number in --head()-- is how many stocks from etf will it valuate median from
    tickers = df["Ticker"].astype(str).str.strip().head(3).tolist()

    sector_metrics = {}
    for ticker in tickers:
        try:
            create_financial_file_2(ticker)
            metrics = fetch_valuation_data_from_api(ticker)  
            sector_metrics[ticker] = metrics
        except Exception as e:
            print(f"Failed to fetch data for {ticker}: {e}")

    sector_median_pe = calculate_sector_median(sector_metrics, "pe")
    sector_median_forward_pe = calculate_sector_median(sector_metrics, "forward_pe")
    sector_median_ev_ebitda_multiple = calculate_sector_median(sector_metrics, "ev_ebitda_multiple")
    sector_median_price_to_sales_multiple = calculate_sector_median(sector_metrics, "price_to_sales_multiple")
    sector_median_price_to_fcf = calculate_sector_median(sector_metrics, "price_to_free_cash_flow_multiple")

    return {
        "sector_median_pe": sector_median_pe,
        "sector_median_forward_pe": sector_median_forward_pe,
        "sector_median_ev_ebitda_multiple": sector_median_ev_ebitda_multiple,
        "sector_median_price_to_sales_multiple": sector_median_price_to_sales_multiple,
        "sector_median_price_to_fcf": sector_median_price_to_fcf
    }

def valuation_weighted_score(
        pe:int,
        forward_pe:int,
        ev_ebitda:int,
        ps: int,
        price_fcf:int,
        wbs: dict
                        )-> int:
       
    pe_weight = wbs['pe']
    forward_pe_weight = wbs['forward_pe']
    ev_ebitda_weight = wbs['ev_ebitda']
    ps_weight = wbs['ps']
    price_fcf_weight = wbs['price_free_cash_flow']

    weighted_together = (
    pe_weight * pe + forward_pe_weight * forward_pe + ev_ebitda_weight * ev_ebitda + ps_weight * ps + price_fcf_weight * price_fcf)
    
    return round(weighted_together)

def calculate_valuation_scores(
    stock_pe: float,
    sector_median_pe: float,
    stock_forward_pe: float,
    sector_median_forward_pe:float,
    stock_ev_ebitda_multiple:float,
    sector_median_ev_ebitda_multiple: float,
    stock_price_to_sales_multiple: float,
    sector_median_price_to_sales_multiple: float,
    stock_price_to_free_cash_flow_multiple: float,
    sector_median_price_to_free_cash_flow_multiple: float,
    sector_name: str,
                              ) -> dict:   
    """
    Core function of the valuation module.
    Gets raw inputs and returns all scores + final valuation_score
    """

    #calling a specific function from the Class in scoring_utils.py
    pe = pe_scorer.score_relative_to_sector(stock_pe, sector_median_pe)
    forward_pe = forward_pe_scorer.score_relative_to_sector(stock_forward_pe,sector_median_forward_pe)
    ev_ebitda = ev_ebitda_scorer.score_relative_to_sector(stock_ev_ebitda_multiple, sector_median_ev_ebitda_multiple)
    ps = ps_scorer.score_relative_to_sector(stock_price_to_sales_multiple, sector_median_price_to_sales_multiple)
    price_fcf = p_fcf_scorer.score_relative_to_sector(stock_price_to_free_cash_flow_multiple, sector_median_price_to_free_cash_flow_multiple)

    weight_by_sector = valuation_weight(sector_name)

    final_score = valuation_weighted_score(pe, forward_pe, ev_ebitda, ps, price_fcf, weight_by_sector)

    return {
        "pe_score": pe,
        "forward_pe_score": forward_pe,
        "ev_ebitda_score": ev_ebitda,
        "ps_score": ps,
        "price_fcf_score": price_fcf,
        "weight_currently_being_used": weight_by_sector,
        "valuation_score": final_score
        }

    





