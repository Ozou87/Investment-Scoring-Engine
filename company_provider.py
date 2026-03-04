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
    
    #Extract from API:
    company_name = file_0['data']['quoteSummary']['result'][0]['assetProfile']['longBusinessSummary'] 
    sector = file_0['data']['quoteSummary']['result'][0]['assetProfile']['sector']

    return {
        "company_name": company_name,
        "sector": sector
    }

    
