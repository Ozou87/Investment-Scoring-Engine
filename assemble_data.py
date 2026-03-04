from company_provider import fetch_company_profile_from_api
from fundamental_module import fetch_fundamental_data_from_api
from valuation_module import fetch_valuation_data_from_api, fetch_sector_valuation_data
from moat_module import fetch_moat_data_from_api
from api_caller import (create_financial_file_0,
                        create_financial_file_1,
                        create_financial_file_2,
                        create_financial_file_3,
                        create_financial_file_4,
                        create_financial_file_5
                        )
def company_profile_data(ticker) -> dict:

    #calling company_profile_api
    create_financial_file_0(ticker)

    company_profile_dict = fetch_company_profile_from_api(ticker)

    return {
        "company_profile": company_profile_dict
        }

def complete_dict_of_data(ticker,sector) -> dict:

    #calling api functions
    create_financial_file_1(ticker)
    create_financial_file_2(ticker)
    create_financial_file_3(ticker)
    create_financial_file_4(ticker)
    create_financial_file_5(ticker)

    #calling module functions
    fundamental_metrics_dict = fetch_fundamental_data_from_api(ticker)
    valuation_metrics_dict_1 = fetch_valuation_data_from_api(ticker)
    valuation_metrics_dict_2 = fetch_sector_valuation_data(sector)
    moat_metrics_dict_3 = fetch_moat_data_from_api(ticker)

    #creating 4 dicts
    return {
        "fundamental":fundamental_metrics_dict,
        "valuation_stock":valuation_metrics_dict_1, 
        "valuation_sector":valuation_metrics_dict_2,
        "moat":moat_metrics_dict_3
    }

