import yfinance as yf
import pandas as pd

def fetch_fundamental_data(ticker_symbol: str) -> dict:
    ticker = ticker_symbol.strip().upper()
    t = yf.Ticker(ticker)
    
    # שליפת נתונים בסיסיים
    info = t.info
    
    # 1. Operating Margin - ניסיון מ-info ואז מ-financials
    op_margin = info.get("operatingMargins")
    if op_margin is None:
        try:
            # financials ttm logic
            income_stmt = t.get_income_stmt()
            op_income = income_stmt.loc['Operating Income'].iloc[0]
            total_rev = income_stmt.loc['Total Revenue'].iloc[0]
            op_margin = op_income / total_rev
        except:
            op_margin = 0

    # 2. Revenue Growth (YoY) - חישוב מהדוחות הרבעוניים אם info ריק
    growth = info.get("revenueGrowth")
    if growth is None:
        try:
            q_financials = t.get_quarterly_income_stmt()
            revs = q_financials.loc['Total Revenue']
            # רבעון נוכחי מול רבעון מקביל אשתקד (בדרך כלל מרחק 4 עמודות)
            current_rev = revs.iloc[0]
            last_year_rev = revs.iloc[4] if len(revs) > 4 else revs.iloc[-1]
            growth = (current_rev - last_year_rev) / last_year_rev
        except:
            growth = 0

    # 3. Debt to Equity - מהמאזן (Balance Sheet)
    d_e = info.get("debtToEquity")
    if d_e is None:
        try:
            bs = t.get_balance_sheet()
            total_debt = bs.loc['Total Debt'].iloc[0]
            equity = bs.loc['Stockholders Equity'].iloc[0]
            d_e = (total_debt / equity) * 100
        except:
            d_e = 0

    # 4. Free Cash Flow Margin
    # ננסה להשתמש ב-fast_info למחיר שוק, אבל לתזרים נלך לדוחות
    fcf = info.get("freeCashflow")
    total_rev = info.get("totalRevenue")
    
    if fcf is None or total_rev is None:
        try:
            cf = t.get_cashflow()
            financials = t.get_income_stmt()
            fcf = cf.loc['Free Cash Flow'].iloc[0]
            total_rev = financials.loc['Total Revenue'].iloc[0]
        except:
            fcf, total_rev = 0, 1

    fcf_margin = fcf / total_rev if total_rev != 0 else 0

    return {
        "revenue_growth_yoy": round(float(growth) * 100, 2),
        "operating_margin_ttm": round(float(op_margin) * 100, 2),
        "debt_to_equity": round(float(d_e), 2),
        "free_cash_flow_margin": round(float(fcf_margin) * 100, 2)
    }

# הרצה ובדיקה
if __name__ == "__main__":
    ticker_input = input("Enter Ticker: ")
    try:
        results = fetch_fundamental_data(ticker_input)
        print(f"\n--- Results for {ticker_input} ---")
        for key, value in results.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error occurred: {e}")
