from flask import Flask, request, jsonify
#flask - main department that create flask
#request - object that contain all the data that the user will send
#jsonify - function that transfer json to python dict
from company_provider import fetch_company_metadata, DataFetchError
from assemble_data import complete_dict_of_data
from core_engine import calculate_all_scores, Fundamental_input, Valuation_input, Moat_input

app = Flask(__name__)
#tell flask where is the file

@app.route("/analyze", methods=["GET"])
#when someone enter this address, loat this GET request with the function underneeth me
def analyze():
    #taking the ticker from the url that was entered by the user
    ticker = request.args.get("ticker")

    if not ticker:
        return jsonify({"error": "pls provide ticker"}), 400
    
    try:
        data = fetch_company_metadata(ticker)

        company_name = data.get("company_name") or ticker
        sector = data.get("sector")

        #getting all financual data
        all_data = complete_dict_of_data(ticker, sector)

        fundamental_input = Fundamental_input(
            revenue_growth_pct=all_data["fundamental"]["revenue_growth_pct"],
            operating_margin_pct=all_data["fundamental"]["operating_margin_pct"],
            debt_to_equity_ratio=all_data["fundamental"]["debt_to_equity_ratio"],
            free_cash_flow_margin_pct=all_data["fundamental"]["free_cash_flow_margin_pct"],
            sector=sector
        )

        valuation_input = Valuation_input(
            stock_pe=all_data["valuation_stock"]["pe"],
            sector_median_pe=all_data["valuation_sector"]["sector_median_pe"],
            stock_forward_pe=all_data["valuation_stock"]["forward_pe"],
            sector_median_forward_pe=all_data["valuation_sector"]["sector_median_forward_pe"],
            stock_ev_ebitda_multiple=all_data["valuation_stock"]["ev_ebitda_multiple"],
            sector_median_ev_ebitda_multiple=all_data["valuation_sector"]["sector_median_ev_ebitda_multiple"],
            stock_price_to_sales_multiple=all_data["valuation_stock"]["price_to_sales_multiple"],
            sector_median_price_to_sales_multiple=all_data["valuation_sector"]["sector_median_price_to_sales_multiple"],
            stock_price_to_free_cash_flow_multiple=all_data["valuation_stock"]["price_to_free_cash_flow_multiple"],
            sector_median_price_to_free_cash_flow_multiple=all_data["valuation_sector"]["sector_median_price_to_fcf"],
            sector=sector
        )

        moat_input = Moat_input(
            return_on_investment_capital=all_data["moat"]["return_on_investment_capital"],
            free_cash_flow_3y_cagr=all_data["moat"]["free_cash_flow_3y_cagr"],
            r_and_d_to_revenue=all_data["moat"]["r_and_d_to_revenue"],
            sector=sector
        )
        
        scores = calculate_all_scores(fundamental_input, valuation_input, moat_input)

        return jsonify({
            "ticker": ticker,
            "company_name": company_name,
            "sector": sector,
            "scores": scores
        }), 200
    
    except DataFetchError:
        return jsonify({"error": "Ticker not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
