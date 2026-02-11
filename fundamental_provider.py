import requests
import json

def fetch_fundamental_data(ticker: str) -> dict:

    clean_ticker = ticker.strip().upper()

    #API Yfinance / stocks / financialData 
    url = "https://yahoo-finance166.p.rapidapi.com/api/stock/get-financial-data"

    querystring = {"region":"US","symbol":clean_ticker}

    headers = {
        "x-rapidapi-key": "ac7d1c4b19mshe08636b12ca178bp1254e4jsn916ba406437e",
        "x-rapidapi-host": "yahoo-finance166.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()   

    with open(f"Saved to fundamental_{clean_ticker}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    #Quarterly Revenue Growth (yoy)% = ( (New Quarter Revenue - Same Quarter Last Year Revenue) / Same Quarter Last Year Revenue ) * 100
    #multipling by 100 to get the metric in %
    revenue_growth_raw = (
    data["quoteSummary"]["result"][0]
            ["financialData"]["revenueGrowth"]["raw"]
        )
    revenue_growth_pct = revenue_growth_raw * 100
    
    #operating margin% = Operating Income (EBIT) / Revenue
    #multipling by 100 to get the metric in %
    operating_margin_raw = (
    data["quoteSummary"]["result"][0]
            ["financialData"]["operatingMargins"]["raw"]
        )
    operating_margin = operating_margin_raw * 100

    #debt to equity = Total Debt / Total Shareholders' Equity
    debt_to_equity = (
    data["quoteSummary"]["result"][0]
            ["financialData"]["debtToEquity"]["raw"])

    #FREE CASH FLOW MARGIN(TTM)% = ( Levered free cash flow(ttm) / Revenue(ttm) * 100 )
    #multipling by 100 to get the metric in %
    revenue = (
    data["quoteSummary"]["result"][0]
            ["financialData"]["totalRevenue"]["raw"])
    levered_free_cash_flow = (
    data["quoteSummary"]["result"][0]
            ["financialData"]["freeCashflow"]["raw"])
    free_cash_flow_margin = (levered_free_cash_flow / revenue) * 100

    return {
        "revenuegrowth": revenue_growth_pct,
        "operatingmargin": operating_margin,
        "debttoequity": debt_to_equity,
        "freecashflowmargin": free_cash_flow_margin
    }

