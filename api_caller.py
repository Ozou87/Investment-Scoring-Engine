import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def save_api_response(url, headers, params, file_path):

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    os.makedirs("data_reports", exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def create_financial_file_1(ticker):
    """
    creating .json file_1 from API to be used for fetching financial data
    """    
    clean_ticker = ticker.strip().upper()

    #API Yfinance / stocks / financialData 
    url = "https://yahoo-finance166.p.rapidapi.com/api/stock/get-financial-data"

    querystring = {"region":"US","symbol":clean_ticker}

    headers = {
            "x-rapidapi-key": os.getenv("API_FUNDAMENTAL_ONE"),
            "x-rapidapi-host": "yahoo-finance166.p.rapidapi.com"
        }

    file_path_1 = f"data_reports/json_file_1_{clean_ticker}.json"
    save_api_response(url, headers, querystring, file_path_1)
    
def create_financial_file_2(ticker):
    """
    creating .json file_2 from API to be used for fetching financial data
    """    
    clean_ticker = ticker.strip().upper()
      
    #API Yahoo Finance Real Time/ stocks / get-summery
    url = "https://yahoo-finance-real-time1.p.rapidapi.com/stock/get-summary"

    querystring = {"lang":"en-US","symbol":clean_ticker,"region":"US"}

    headers = {
        "x-rapidapi-key": os.getenv("API_VALUATION_ONE"),
        "x-rapidapi-host": "yahoo-finance-real-time1.p.rapidapi.com"
    }

    file_path_2 = f"data_reports/json_file_2_{clean_ticker}.json"
    save_api_response(url, headers, querystring, file_path_2)
    
def create_financial_file_3(ticker):
    """
    creating .json file_3 from API to be used for fetching financial data
    """    
    clean_ticker = ticker.strip().upper()

    #API YH FINANCE/ stocks / balance-sheet
    url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/modules"

    querystring = {"ticker":clean_ticker,"module":"balance-sheet-v2"}

    headers = {
	"x-rapidapi-key": os.getenv("API_MOAT_ONE"),
	"x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
    }

    file_path_3 = f"data_reports/json_file_3_{clean_ticker}.json"
    save_api_response(url, headers, querystring, file_path_3)
    
def create_financial_file_4(ticker):
    """
    creating .json file_4 from API to be used for fetching financial data
    """    
    clean_ticker = ticker.strip().upper()

    #API Yahoo Finance Real Time/ stocks / get-cashflow
    url = "https://yahoo-finance-real-time1.p.rapidapi.com/stock/get-cashflow"

    querystring = {"region":"US","lang":"en-US","symbol":clean_ticker}

    headers = {
	"x-rapidapi-key":os.getenv("API_MOAT_TWO"),
	"x-rapidapi-host": "yahoo-finance-real-time1.p.rapidapi.com"
    }

    file_path_4 = f"data_reports/json_file_4_{clean_ticker}.json"
    save_api_response(url, headers, querystring, file_path_4)
    





