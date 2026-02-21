from api_caller import create_financial_file_1, create_financial_file_2
from fundamental_module import fetch_fundamental_data_from_api
from valuation_module import fetch_valuation_data_from_api, fetch_sector_valuation_data

def complete_dict_of_data(ticker,sector):

    #calling api functions
    create_financial_file_1(ticker)
    create_financial_file_2(ticker)

    #calling module functions
    fundamental_metrics_dict = fetch_fundamental_data_from_api(ticker)
    valuation_metrics_dict_1 = fetch_valuation_data_from_api(ticker)
    valuation_metrics_dict_2 = fetch_sector_valuation_data(sector)

    return {
        "fundamental":fundamental_metrics_dict,
        "valuation_stock":valuation_metrics_dict_1, 
        "valuation_sector":valuation_metrics_dict_2
    }

