from flask import Flask, request, jsonify
from core_engine import calculate_all_scores, Fundamental_input, Valuation_input, Moat_input
from company_provider import fetch_company_metadata, DataFetchError
from assemble_data import complete_dict_of_data

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate_scores():
    data = request.json

    if not data or "ticker" not in data:
        return jsonify({"error": "Ticker not provided"}), 400

    ticker = data["ticker"]

    try:
        # --- Fetch company metadata ---
        metadata = fetch_company_metadata(ticker)
        sector = metadata.get("sector")
        stock_label = metadata.get("company_name", ticker)

        # --- Fetch all data for ticker ---
        all_data = complete_dict_of_data(ticker, sector)

        # --- Build Fundamental_input ---
        fundamental_json = data.get("fundamental", {})
        fundamental_input = Fundamental_input(
            revenue_growth_pct=fundamental_json.get("revenue_growth_pct", all_data["fundamental"]["revenue_growth_pct"]),
            operating_margin_pct=fundamental_json.get("operating_margin_pct", all_data["fundamental"]["operating_margin_pct"]),
            debt_to_equity_ratio=fundamental_json.get("debt_to_equity_ratio", all_data["fundamental"]["debt_to_equity_ratio"]),
            free_cash_flow_margin_pct=fundamental_json.get("free_cash_flow_margin_pct", all_data["fundamental"]["free_cash_flow_margin_pct"]),
            sector=sector
        )

        # --- Build Valuation_input ---
        valuation_json = data.get("valuation", {})
        valuation_input = Valuation_input(
            stock_pe=valuation_json.get("stock_pe", all_data["valuation_stock"]["pe"]),
            sector_median_pe=valuation_json.get("sector_median_pe", all_data["valuation_sector"]["sector_median_pe"]),
            stock_forward_pe=valuation_json.get("stock_forward_pe", all_data["valuation_stock"]["forward_pe"]),
            sector_median_forward_pe=valuation_json.get("sector_median_forward_pe", all_data["valuation_sector"]["sector_median_forward_pe"]),
            stock_ev_ebitda_multiple=valuation_json.get("stock_ev_ebitda_multiple", all_data["valuation_stock"]["ev_ebitda_multiple"]),
            sector_median_ev_ebitda_multiple=valuation_json.get("sector_median_ev_ebitda_multiple", all_data["valuation_sector"]["sector_median_ev_ebitda_multiple"]),
            stock_price_to_sales_multiple=valuation_json.get("stock_price_to_sales_multiple", all_data["valuation_stock"]["price_to_sales_multiple"]),
            sector_median_price_to_sales_multiple=valuation_json.get("sector_median_price_to_sales_multiple", all_data["valuation_sector"]["sector_median_price_to_sales_multiple"]),
            stock_price_to_free_cash_flow_multiple=valuation_json.get("stock_price_to_free_cash_flow_multiple", all_data["valuation_stock"]["price_to_free_cash_flow_multiple"]),
            sector_median_price_to_free_cash_flow_multiple=valuation_json.get("sector_median_price_to_free_cash_flow_multiple", all_data["valuation_sector"]["sector_median_price_to_fcf"]),
            sector=sector
        )

        # --- Build Moat_input ---
        moat_json = data.get("moat", {})
        moat_input = Moat_input(
            return_on_investment_capital=moat_json.get("return_on_investment_capital", all_data["moat"]["return_on_investment_capital"]),
            free_cash_flow_3y_cagr=moat_json.get("free_cash_flow_3y_cagr", all_data["moat"]["free_cash_flow_3y_cagr"]),
            gross_margin_list=moat_json.get("gross_margin_list", []),
            r_and_d_raw=moat_json.get("r_and_d_raw", 0),
            revenue_growth_raw=moat_json.get("revenue_growth_raw", 0),
            sector=sector
        )

        # --- Run core engine ---
        scores = calculate_all_scores(fundamental_input, valuation_input, moat_input)

        # --- Prepare response ---
        response = {
            "ticker": ticker,
            "company_name": stock_label,
            "fundamentals_score": scores["fundamentals"]["fundamentals_score"],
            "valuation_score": scores["valuation"]["valuation_score"],
            "moat_score": scores["moat"]["moat_score"],
            "final_score": scores["final_score"]
        }

        return jsonify(response)

    except DataFetchError:
        return jsonify({"error": "Ticker not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)