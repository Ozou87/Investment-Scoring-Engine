from core_engine import calculate_all_scores
from core_engine import Fundamental_input, Valuation_input, Moat_input

from company_provider import fetch_company_metadata, DataFetchError
from assemble_data import complete_dict_of_data

data = None
ticker = None
sector = None
stock_label = None

print("Welcome to the Investment Scoring Engine")

#loop that make sure its float and system wont crash( check weather i need it)
#check if needed when connecting FLASK
def get_float(prompt) -> float:

    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid input. PLS try again ")

while True:
    user_ticker = input("Enter stock ticker: (or 'q' to quit) ").strip()

    if user_ticker.lower() in {"q", "quit", "exit"}:
        print("Goodbye")
        break
    try:

        data = fetch_company_metadata(user_ticker)

        ticker = data["ticker"]
        sector = data.get("sector")
        stock_label = data.get("company_name") or ticker

        print(f"Ticker: {data['ticker']}")
        print(f"Company: {data['company_name']}")

        if sector:
            print(f"Sector: {sector}")
        else:
            print("Sector: Not available")

        #getting fundamental and valuation data for ticker:
        all_data = complete_dict_of_data(ticker, sector)

        revenue_growth_pct = all_data["fundamental"]["revenue_growth_pct"]
        operating_margin_pct = all_data["fundamental"]["operating_margin_pct"]
        debt_to_equity_ratio = all_data["fundamental"]["debt_to_equity_ratio"]
        free_cash_flow_margin_pct = all_data["fundamental"]["free_cash_flow_margin_pct"]

        stock_pe = all_data["valuation_stock"]["pe"]
        stock_forward_pe = all_data["valuation_stock"]["forward_pe"]
        stock_ev_ebitda_multiple = all_data["valuation_stock"]["ev_ebitda_multiple"]
        stock_price_to_sales_multiple = all_data["valuation_stock"]["price_to_sales_multiple"]
        stock_price_to_free_cash_flow_multiple = all_data["valuation_stock"]["price_to_free_cash_flow_multiple"]

        sector_median_pe = all_data["valuation_sector"]["sector_median_pe"]
        sector_median_forward_pe = all_data["valuation_sector"]["sector_median_forward_pe"]
        sector_median_ev_ebitda_multiple = all_data["valuation_sector"]["sector_median_ev_ebitda_multiple"]
        sector_median_price_to_sales_multiple = all_data["valuation_sector"]["sector_median_price_to_sales_multiple"]
        sector_median_price_to_fcf = all_data["valuation_sector"]["sector_median_price_to_fcf"]

        return_on_investment_capital_pct = all_data["moat"]["return_on_investment_capital_pct"]
        free_cash_flow_3y_cagr = all_data["moat"]["free_cash_flow_3y_cagr"]

        break

    except Exception as e:
        print("Unexpected error:", repr(e))
        raise

    except ValueError as e:
        print(f"Input error: {e}")

    except DataFetchError:
        print("Ticker not found. Try again")
    
    except Exception as e:
        print(f"Unexpected error: {e}")

if data is None:
    raise SystemExit(0)

print("\n--- Fundamental Metrics ---")
print(f"Quarterly revenue_growth Growth (YoY): {revenue_growth_pct:.2f}%")
print(f"Operating Margin (TTM): {operating_margin_pct:.2f}%")
print(f"Total Debt / Equity (MRQ): {debt_to_equity_ratio:.2f}")
print(f"Free Cash Flow Margin (TTM): {free_cash_flow_margin_pct:.2f}%")

fundamental_input = Fundamental_input(
    revenue_growth_pct=revenue_growth_pct,
    operating_margin_pct=operating_margin_pct,
    debt_to_equity_ratio=debt_to_equity_ratio,
    free_cash_flow_margin_pct=free_cash_flow_margin_pct,
    sector=sector
                                    )

print("\n--- Valuation Metrics ---")
print(f"Stock P/E: {stock_pe:.2f}")
print(f"Sector P/E: {sector_median_pe:.2f}")
print(f"Stock Forward P/E: {stock_forward_pe:.2f}")
print(f"Sector Forward P/E: {sector_median_forward_pe:.2f}")
print(f"Stock EV/EBITDA multiple: {stock_ev_ebitda_multiple:.2f}%")
print(f"Sector EV/EBITDA multiple: {sector_median_ev_ebitda_multiple:.2f}%")
print(f"Total Debt / Equity (MRQ): {debt_to_equity_ratio:.2f}")
print(f"Free Cash Flow Margin (TTM): {free_cash_flow_margin_pct:.2f}%")

valuation_input= Valuation_input(
    stock_pe=stock_pe,
    sector_median_pe=sector_median_pe,
    stock_forward_pe=stock_forward_pe,
    sector_median_forward_pe=sector_median_forward_pe,
    stock_ev_ebitda_multiple=stock_ev_ebitda_multiple,
    sector_median_ev_ebitda_multiple=sector_median_ev_ebitda_multiple,
    stock_price_to_sales_multiple=stock_price_to_sales_multiple,
    sector_median_price_to_sales_multiple=sector_median_price_to_sales_multiple,
    stock_price_to_free_cash_flow_multiple=stock_price_to_free_cash_flow_multiple,
    sector_median_price_to_fcf=sector_median_price_to_fcf,
    sector=sector
                                )

print("\n--- Moat inputs ---")

print("\nEnter Gross Margin % for the last 5 years:")
gm1 = get_float("Year 1 Gross Margin %: ")
gm2 = get_float("Year 2 Gross Margin %: ")
gm3 = get_float("Year 3 Gross Margin %: ")
gm4 = get_float("Year 4 Gross Margin %: ")
gm5 = get_float("Year 5 Gross Margin %: ")
gross_margin_list = [gm1, gm2, gm3, gm4, gm5]

r_and_d_raw = get_float("Enter total R&D (same units as revenue_growth): ")
revenue_growth_raw = get_float("Enter total revenue_growth (same units as R&D): ")

moat_input = Moat_input(
    return_on_investment_capital_pct=return_on_investment_capital_pct,
    free_cash_flow_3y_cagr=free_cash_flow_3y_cagr,
    gross_margin_list=gross_margin_list,
    r_and_d_raw=r_and_d_raw,
    revenue_growth_raw=revenue_growth_raw,
    sector=sector
                        )

# running core engine and final score
scores = calculate_all_scores(fundamental_input, valuation_input, moat_input)

fundamentals_total = scores["fundamentals"]["fundamentals_score"]
valuation_total = scores["valuation"]["valuation_score"]
moat_total = scores["moat"]["moat_score"]

final_score = scores["final_score"]

print(f"{stock_label}'s Fundamentals score: {fundamentals_total}")
print(f"{stock_label}'s Valuation score: {valuation_total}")
print(f"{stock_label}'s Moat score: {moat_total}")
print("-" * 35)
print(f"TOTAL FINAL SCORE for {stock_label} is: {final_score}")









