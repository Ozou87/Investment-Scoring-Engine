import requests
import json
import pandas as pd
import os
import statistics
from dotenv import load_dotenv

load_dotenv()

def fetch_stock_valuation_data(ticker: str) -> dict:

    clean_ticker = ticker.strip().upper()

    #API YH FINANCE/ stocks / earnings
    url = "https://yahoo-finance166.p.rapidapi.com/api/stock/get-financial-data"

    querystring = {"region":"US","symbol":clean_ticker}

    headers = {
        "x-rapidapi-key": os.getenv("API_VALUATION_ONE"),
        "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data_1 = response.json()   

    os.makedirs("data_reports", exist_ok=True)
    file_path_1 = f"data_reports/valuation_1_{clean_ticker}.json"
    with open(file_path_1, "w", encoding="utf-8") as f:
        json.dump(data_1, f, indent=2)

    #API Yahoo Finance Real Time/ stocks / get-summery
    url = "https://yahoo-finance-real-time1.p.rapidapi.com/stock/get-summary"

    querystring = {"lang":"en-US","symbol":clean_ticker,"region":"US"}

    headers = {
        "x-rapidapi-key": os.getenv("API_VALUATION_TWO"),
        "x-rapidapi-host": "yahoo-finance-real-time1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data_2 = response.json()   

    os.makedirs("data_reports", exist_ok=True)
    file_path_2 = f"data_reports/valuation_2_{clean_ticker}.json"
    with open(file_path_2, "w", encoding="utf-8") as f:
        json.dump(data_2, f, indent=2)

    #P/E = current price / EPS (TTM)
    current_price = data_2["financialData"]["currentPrice"]
    eps_ttm = data_2["defaultKeyStatistics"]["trailingEps"]
    stock_pe = current_price / eps_ttm

    #Forward P/E = Current Price / Expected EPS (Next 12 Months)
    stock_forward_pe = data_2["defaultKeyStatistics"]["forwardPE"]

    #ev = Enterprise Value = market cap + (total debt - cash & cash equivalents)
    #ebitda = Earnings Before Interest, Taxes, Depreciation & Amortization = operating income(EBIT) + depreciation + amoritization
    #EV/EBITA MULTIPE = Enterprise Value / Ebitda
    ev_ebitda_multiple = data_2["defaultKeyStatistics"]["enterpriseToEbitda"]
    
    #Price/Sales = Market Cap / Revenue (ttm)
    stock_price_to_sales_multiple = data_2["summaryDetail"]["priceToSalesTrailing12Months"]

    #Price to Free Cash Flow multiple = Market Cap / Free Cash Flow
    stock_market_cap = data_2["summaryDetail"]["marketCap"]
    stock_free_cash_flow = data_2["financialData"]["freeCashflow"]
    stock_price_to_free_cash_flow_multiple = stock_market_cap / stock_free_cash_flow

    return {
        "pe": stock_pe,
        "forwardpe": stock_forward_pe,
        "evebitdamultiple": ev_ebitda_multiple,
        "pricetosalesmultiple": stock_price_to_sales_multiple,
        "pricetofreecashflowmultiple": stock_price_to_free_cash_flow_multiple
    }

def calculate_sector_median(sector_metrics: dict, metric_name: str):
    values = [
        data[metric_name]
        for data in sector_metrics.values()
        if data.get(metric_name) is not None
    ]
    return statistics.median(values)

def fetch_sector_valuation_data(sector: str,):

    #creating dict that connect sector name to sector file name
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

    tickers = df["Ticker"].astype(str).str.strip().head(3).tolist()


    sector_metrics = {}
    for ticker in tickers:
        try:
            metrics = fetch_stock_valuation_data(ticker)  
            sector_metrics[ticker] = metrics
        except Exception as e:
            print(f"Failed to fetch data for {ticker}: {e}")

    sector_median_pe = calculate_sector_median(sector_metrics, "pe")
    sector_median_forward_pe = calculate_sector_median(sector_metrics, "forwardpe")
    sector_median_ev_ebitda_multiple = calculate_sector_median(sector_metrics, "evebitdamultiple")
    sector_median_price_to_sales_multiple = calculate_sector_median(sector_metrics, "pricetosalesmultiple")
    sector_median_price_to_fcf = calculate_sector_median(sector_metrics, "pricetofreecashflowmultiple")

    return {
        "sector_median_pe": sector_median_pe,
        "sector_median_forward_pe": sector_median_forward_pe,
        "sector_median_ev_ebitda_multiple": sector_median_ev_ebitda_multiple,
        "sector_median_price_to_sales_multiple": sector_median_price_to_sales_multiple,
        "sector_median_price_to_fcf": sector_median_price_to_fcf
    }

    






    







    