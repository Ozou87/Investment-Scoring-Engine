from dotenv import load_dotenv
import json

load_dotenv()

def fetch_company_profile_from_api(ticker) -> dict:
    """
    opening .json file and fetching cmpany profile metrics:
    -company name
    -sector
    """
    clean_ticker = ticker.strip().upper()

    file_path_0 = f"data_reports/json_file_0_{clean_ticker}.json"
    with open(file_path_0, "r", encoding="utf-8") as f:
            file_0 = json.load(f)

    file_path_6 = f"data_reports/json_file_6_{clean_ticker}.json"
    with open(file_path_6, "r", encoding="utf-8") as f:
            file_6 = json.load(f)
    
    #Extracting from json files:
    company_name = file_6['data'][1]['quoteSummary']['result'][0]['price']['longName']
    sector = file_0['data']['quoteSummary']['result'][0]['assetProfile']['sector']

    return {
        "company_name": company_name,
        "sector": sector
    }

    
