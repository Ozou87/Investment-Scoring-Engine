
from core_engine import calculate_all_scores

#loop that make sure its float and system wont crash
def get_float(prompt) -> float:

    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid input. PLS try again ")

print("Welcome to the Investment Scoring Algorithm")
stock = input("PLS ENter a stock/symbol: ")

### inputs- soon to be API###

# asking user for fundamentals inputs: 
revenue_growth = get_float("Enter stock Revenue Growth %: ")
operating_margin = get_float("Enter stock Operating margin %: ")
debt_to_equity = get_float("Enter stock Debt to Equity ratio: ")
fcf_margin = get_float("Enter stock Free Cash Flow Margin %: ")

fundamental_input = {
    "revenue_growth": revenue_growth,
    "operating_margin": operating_margin,
    "debt_to_equity": debt_to_equity,
    "fcf_margin": fcf_margin,
                    }

# asking user for valuation inputs: 
print("\n--- Valuation inputs (stock vs sector) ---")
stock_pe = get_float("Enter STOCK P/E: ")
sector_pe = get_float("Enter SECTOR P/E: ")

stock_fpe = get_float("Enter STOCK Forward P/E: ")
sector_fpe = get_float("Enter SECTOR Forward P/E: ")

stock_eveb = get_float("Enter STOCK EV/EBITDA: ")
sector_eveb = get_float("Enter SECTOR EV/EBITDA: ")

stock_ps = get_float("Enter STOCK Price/Sales: ")
sector_ps = get_float("Enter SECTOR Price/Sales: ")

stock_pfcf = get_float("Enter STOCK Price/Free Cash Flow: ")
sector_pfcf = get_float("Enter SECTOR Price/Free Cash Flow: ")

valuation_input = {
    "stock_pe": stock_pe,
    "sector_pe": sector_pe,
    "stock_fpe": stock_fpe,
    "sector_fpe": sector_fpe,
    "stock_eveb": stock_eveb,
    "sector_eveb": sector_eveb,
    "stock_ps": stock_ps,
    "sector_ps": sector_ps,
    "stock_pfcf": stock_pfcf,
    "sector_pfcf": sector_pfcf,
                    }

# asking user for moat inputs: 
print("\n--- Moat inputs ---")
roic_raw_value = get_float("Enter ROIC 5Y average %: ")
fcf_growth_raw = get_float("Enter FCF 5Y CAGR %: ")

print("\nEnter Gross Margin % for the last 5 years:")
gm1 = get_float("Year 1 Gross Margin %: ")
gm2 = get_float("Year 2 Gross Margin %: ")
gm3 = get_float("Year 3 Gross Margin %: ")
gm4 = get_float("Year 4 Gross Margin %: ")
gm5 = get_float("Year 5 Gross Margin %: ")
gross_margin_list = [gm1, gm2, gm3, gm4, gm5]

r_and_d_raw = get_float("Enter total R&D (same units as revenue): ")
revenue_raw = get_float("Enter total Revenue (same units as R&D): ")

moat_input = {
    "roic_raw_value": roic_raw_value,
    "fcf_growth_raw": fcf_growth_raw,
    "gross_margin_list": gross_margin_list,
    "r_and_d_raw": r_and_d_raw,
    "revenue_raw": revenue_raw,
            }

# running core engine and final score
scores = calculate_all_scores(fundamental_input, valuation_input, moat_input)

fundamentals_total = scores["fundamentals"]["Fundamentals_Score (range of 1-100)"]
valuation_total = scores["valuation"]["valuation_score"]
moat_total = scores["moat"]["moat_score"]

final_score = scores["final_score"]

print(f"{stock}'s Fundamentals score: {fundamentals_total}")
print(f"{stock}'s Valuation score: {valuation_total}")
print(f"{stock}'s Moat score: {moat_total}")
print("-" * 35)
print(f"TOTAL FINAL SCORE for {stock} is: {final_score}")










