
from core_engine import calculate_all_scores
from core_engine import Fundamental_input, Valuation_input, Moat_input

from company_provider import fetch_company_metadata, DataFetchError
from fundamental_provider import fetch_fundamental_data, fundamentalFetchError


data = None
ticker = None
sector = None
stock_label = None
revenue_growth_yoy = None
gross_margin_ttm = None

print("Welcome to the Investment Scoring Engine")

#loop that make sure its float and system wont crash
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

        fundamental_data = fetch_fundamental_data(user_ticker)

        revenue_growth_yoy = fundamental_data.get("revenue_growth_yoy")
        gross_margin_ttm = fundamental_data.get("gross_margin_ttm")

        print(revenue_growth_yoy)
        print(gross_margin_ttm)

        
        break

    except ValueError as e:
        print(f"Input error: {e}")

    except DataFetchError:
        print("Ticker not found. Try again")

    except fundamentalFetchError as e:
        print(f"Fundamentals unavailable for {user_ticker.upper()}: {e}")
        continue
    
    except Exception as e:
        print(f"Unexpected error: {e}")

if data is None:
    raise SystemExit(0)

# asking user for fundamentals inputs: 
debt_to_equity = get_float("Enter stock Debt to Equity ratio: ")
fcf_margin = get_float("Enter stock Free Cash Flow Margin %: ")

fundamental_input = Fundamental_input(
    revenue_growth_yoy=revenue_growth_yoy,
    gross_margin_ttm=gross_margin_ttm,
    debt_to_equity=debt_to_equity,
    fcf_margin=fcf_margin,
    sector=sector
                                    )

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

valuation_input= Valuation_input(
    stock_pe=stock_pe,
    sector_pe=sector_pe,
    stock_fpe=stock_fpe,
    sector_fpe=sector_fpe,
    stock_eveb=stock_eveb,
    sector_eveb=sector_eveb,
    stock_ps=stock_ps,
    sector_ps=sector_ps,
    stock_pfcf=stock_pfcf,
    sector_pfcf=sector_pfcf,
    sector=sector
                                )

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

moat_input = Moat_input(
    roic_raw_value=roic_raw_value,
    fcf_growth_raw=fcf_growth_raw,
    gross_margin_list=gross_margin_list,
    r_and_d_raw=r_and_d_raw,
    revenue_raw=revenue_raw,
    sector=sector
                        )

# running core engine and final score
scores = calculate_all_scores(fundamental_input, valuation_input, moat_input)

fundamentals_total = scores["fundamentals"]["Fundamentals_score"]
valuation_total = scores["valuation"]["Valuation_score"]
moat_total = scores["moat"]["Moat_score"]

final_score = scores["final_score"]

print(f"{stock_label}'s Fundamentals score: {fundamentals_total}")
print(f"{stock_label}'s Valuation score: {valuation_total}")
print(f"{stock_label}'s Moat score: {moat_total}")
print("-" * 35)
print(f"TOTAL FINAL SCORE for {stock_label} is: {final_score}")










