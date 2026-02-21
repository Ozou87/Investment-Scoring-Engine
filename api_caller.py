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

    file_path_1 = f"json_file_1_{clean_ticker}.json"
    with open(file_path_1, "w", encoding="utf-8") as f:
            json.dump(file_1, f, indent=2)

def create_financial_file_2(ticker):

    clean_ticker = ticker.strip().upper()
      
    #API Yahoo Finance Real Time/ stocks / get-summery
    url = "https://yahoo-finance-real-time1.p.rapidapi.com/stock/get-summary"

    querystring = {"lang":"en-US","symbol":clean_ticker,"region":"US"}

    headers = {
        "x-rapidapi-key": os.getenv("API_VALUATION_TWO"),
        "x-rapidapi-host": "yahoo-finance-real-time1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    file_2 = response.json()   

    os.makedirs("data_reports", exist_ok=True)

    file_path_2 = f"json_file_2{clean_ticker}.json"
    with open(file_path_2, "w", encoding="utf-8") as f:
        json.dump(file_2, f, indent=2)
