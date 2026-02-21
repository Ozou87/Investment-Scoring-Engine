import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def create_financial_file_1(ticker):
    clean_ticker = ticker.strip().upper()
    """
    creating .json file from API to be used for fetching financial data
    """    
    
    clean_ticker = ticker.strip().upper()
    #API Yfinance / stocks / financialData 
    url = "https://yahoo-finance166.p.rapidapi.com/api/stock/get-financial-data"

    querystring = {"region":"US","symbol":clean_ticker}

    headers = {
            "x-rapidapi-key": os.getenv("API_FUNDAMENTAL_ONE"),
            "x-rapidapi-host": "yahoo-finance166.p.rapidapi.com"
        }

    response = requests.get(url, headers=headers, params=querystring)

    file_1 = response.json()   

    os.makedirs("data_reports", exist_ok=True)

    file_path = f"data_reports/fundamental_{clean_ticker}.json"
    with open(file_path, "w", encoding="utf-8") as f:
            json.dump(file_1, f, indent=2)