import requests
import json

def fetch_stock_valuation_data(ticker: str) -> dict:

    clean_ticker = ticker.strip().upper()

    #API YH FINANCE/ stocks / earnings
    url = "https://yahoo-finance166.p.rapidapi.com/api/stock/get-financial-data"

    querystring = {"region":"US","symbol":clean_ticker}

    headers = {
        "x-rapidapi-key": "ac7d1c4b19mshe08636b12ca178bp1254e4jsn916ba406437e",
        "x-rapidapi-host": "yahoo-finance166.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data_1 = response.json()   

    with open(f"Saved to valuation1{clean_ticker}.json", "w", encoding="utf-8") as f:
        json.dump(data_1, f, indent=2)

    #API Yahoo Finance Real Time/ stocks / get-summery
    url = "https://yahoo-finance-real-time1.p.rapidapi.com/stock/get-summary"

    querystring = {"lang":"en-US","symbol":clean_ticker,"region":"US"}

    headers = {
        "x-rapidapi-key": "ac7d1c4b19mshe08636b12ca178bp1254e4jsn916ba406437e",
        "x-rapidapi-host": "yahoo-finance-real-time1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data_2 = response.json()   

    with open(f"Saved to valuation2{clean_ticker}.json", "w", encoding="utf-8") as f:
        json.dump(data_2, f, indent=2)

    #Stock P/E = current price / EPS (TTM)
    current_price = data_2["financialData"]["currentPrice"]
    eps_ttm = data_2["defaultKeyStatistics"]["trailingEps"]
    stock_pe = current_price / eps_ttm

    stock_forward_pe = data_2["defaultKeyStatistics"]["forwardPE"]

    #ev = Enterprise Value = market cap + (total debt - cash & cash equivalents)
    #ebitda = Earnings Before Interest, Taxes, Depreciation & Amortization = operating income(EBIT) + depreciation + amoritization
    #EV/EBITA MULTIPE = Enterprise Value / Ebitda
    ev_ebitda_multiple = data_2["defaultKeyStatistics"]["enterpriseToEbitda"]
    
    #Stock Price to Free Cash Flow multiple = Market Cap / Free Cash Flow
    stock_market_cap = data_2["summaryDetail"]["marketCap"]
    stock_free_cash_flow = data_2["financialData"]["freeCashflow"]

    stock_price_to_free_cash_flow_multiple = stock_market_cap / stock_free_cash_flow

    return {
        "stockpe": stock_pe,
        "stockforwardpe": stock_forward_pe,
        "stockevebitdamultiple": ev_ebitda_multiple,
        
        "stockricetofreecashflowmultiple": stock_price_to_free_cash_flow_multiple
    }



#     from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent  # הקובץ שבו הקוד הזה נמצא
# BENCH_DIR = BASE_DIR / "sector_benchmarks"

# SECTOR_TO_FILE = {
#     "Technology": BENCH_DIR / "holdings-daily-us-en-xlk.xlsx",
#     "Healthcare": BENCH_DIR / "holdings-daily-us-en-xlv.xlsx",
#     "Financial Services": BENCH_DIR / "holdings-daily-us-en-xlf.xlsx",
#     # ...
# }
