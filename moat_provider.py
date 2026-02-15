import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_moat_data(ticker: str) -> dict:

    clean_ticker = ticker.strip().upper()

    #API YH FINANCE/ stocks / balance-sheet
    url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/modules"

    querystring = {"ticker":clean_ticker,"module":"balance-sheet-v2"}

    headers = {
	"x-rapidapi-key": os.getenv("API_MOAT_ONE"),
	"x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    moat_data_1= response.json() 
    file_path = f"data_reports/moat_{clean_ticker}_1.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(moat_data_1, f, indent=2)  

    #Return on Invested Capital (ROIC) = NOPAT / Invested Capital
    #NOPAT = Operating Income * (1 - Tax Rate)
    #Invested Capital = Total Debt + Total Equity - Cash

    total_debt = moat_data_1["body"]["debt"]["TTM"]
    total_equity = moat_data_1["body"]["equity"]["TTM"]
    total_cash = moat_data_1["body"]["totalcash"]["TTM"]
    invested_capital = total_debt + total_equity - total_cash

    

    return {
        "revenuegrowth": revenue_growth_pct,
        "operatingmargin": operating_margin,
        "debttoequity": debt_to_equity,
        "freecashflowmargin": free_cash_flow_margin
    }
    pass