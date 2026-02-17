import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

# def fetch_moat_data(ticker: str) -> dict:

#     clean_ticker = ticker.strip().upper()

#     #API YH FINANCE/ stocks / balance-sheet
#     url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/modules"

#     querystring = {"ticker":clean_ticker,"module":"balance-sheet-v2"}

#     headers = {
# 	"x-rapidapi-key": os.getenv("API_MOAT_ONE"),
# 	"x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
#     }

#     response = requests.get(url, headers=headers, params=querystring)

#     moat_data_1= response.json() 
#     file_path = f"data_reports/moat_{clean_ticker}_1.json"
#     with open(file_path, "w", encoding="utf-8") as f:
#         json.dump(moat_data_1, f, indent=2)  

#     #Return on Invested Capital (ROIC) = NOPAT / Invested Capital
#     #multipling by 100 to get metric in %
#     #NOPAT = Operating Income(EBIT) * (1 - Tax Rate)
#     #EBIT = operating margin * Revenue
#     #Invested Capital = Total Debt + Total Equity - Cash
    
#     total_debt = moat_data_1["body"]["debt"]["TTM"]
#     total_equity = moat_data_1["body"]["equity"]["TTM"]
#     total_cash = moat_data_1["body"]["totalcash"]["TTM"]
#     invested_capital = total_debt + total_equity - total_cash
#     #get from fundamental module or api (consider function for api)
#     nopat = operating_margin * revenue
#     return_on_investment_capital_pct = nopat / invested_capital * 100 


#     FCF_3Y_CAGR = Compound-Annual-Growth-Rate of Free Cash Flow 
#     FCF_3Y_CAGR = (free cash_flow_latest / free_cash_flow_3_years_ago)^(1/3) - 1
#     free cash flow latest from fundamental module
#     get - free cash flow 3 years ago



#     return {
#         "return_on_investment_capital_pct": return_on_investment_capital_pct,
#         "free_cash_flow_3_cagr": ,
#         
#     }
#     pass