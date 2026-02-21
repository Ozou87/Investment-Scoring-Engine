import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()


#API YH FINANCE/ stocks / balance-sheet
url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/modules"

querystring = {"ticker":"PLTR","module":"balance-sheet-v2"}

headers = {
    "x-rapidapi-key": os.getenv("API_MOAT_ONE"),
	"x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
    }

response = requests.get(url, headers=headers, params=querystring)

moat_data_1= response.json() 
file_path = f"data_reports/moat_PLTR_1.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(moat_data_1, f, indent=2)  