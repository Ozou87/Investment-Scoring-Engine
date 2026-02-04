import yfinance as yf
import contextlib
import io
import math

class fundamentalFetchError(Exception):
    """Raised when the external data source fails or returns invalid data."""

def fetch_fundamental_data(ticker: str) -> dict:
    # 1) validate input
    if not ticker or not ticker.strip():
        raise ValueError("Ticker is required")
    
    clean_ticker = ticker.strip().upper()

    # 2) create ticker object (silence yfinance noise)
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            t = yf.Ticker(clean_ticker)
            annual = t.financials
            quarterly = t.quarterly_financials
    except Exception as e:
        raise fundamentalFetchError(f"Failed to fetch data for {clean_ticker}") from e

    # 3) basic dataframe checks (exists / not empty)
    if annual is None or getattr(annual, "empty", True):
        raise fundamentalFetchError(f"No annual financials available for {clean_ticker}")
    
    # 4) extract revenue series (row may not exist)
    try:
        revenue_y = annual.loc["Total Revenue"]
    except KeyError as e:
        raise fundamentalFetchError(f"Anual 'Total Revenue' revenue row not found for {clean_ticker}") from e

    # 5) check we have at least 8 quarters for TTM YoY
    if len(revenue_y) < 2:
        raise fundamentalFetchError(f"Not enough annual revenue data to compute YoY growth for {clean_ticker}")

    latest = revenue_y.iloc[0]
    previous = revenue_y.iloc[1]

    if previous == 0 or (isinstance(previous, float) and math.isnan(previous)):
        raise fundamentalFetchError(
            f"Invalid previous year revenue for {clean_ticker}")

    revenue_growth_yoy = ((latest - previous) / previous) * 100

    if quarterly is None or getattr(quarterly, "empty", True):
        raise fundamentalFetchError(f"No quarterly financials available for {clean_ticker}")

    try:
        revenue_q = quarterly.loc["Total Revenue"]
    except KeyError as e:
        raise fundamentalFetchError(
            f"Quarterly 'Total Revenue' row not found for {clean_ticker}"
        ) from e

    try:
        gross_profit_q = quarterly.loc["Gross Profit"]
    except KeyError as e:
        raise fundamentalFetchError(
            f"Quarterly 'Gross Profit' row not found for {clean_ticker}"
        ) from e

    if len(revenue_q) < 4 or len(gross_profit_q) < 4:
        raise fundamentalFetchError(
            "Not enough quarterly data to compute TTM gross margin (requires 4 quarters)"
        )

    rev_ttm = revenue_q.iloc[0:4].sum()
    gp_ttm = gross_profit_q.iloc[0:4].sum()

    if rev_ttm == 0 or (isinstance(rev_ttm, float) and math.isnan(rev_ttm)):
        raise fundamentalFetchError(
            "Invalid TTM revenue (zero or NaN), cannot compute gross margin"
        )

    gross_margin_ttm = (gp_ttm / rev_ttm) * 100

    # -------------------------
    # Final payload
    # -------------------------
    return {
        
        "revenue_growth_yoy": float(revenue_growth_yoy),
        "gross_margin_ttm": float(gross_margin_ttm),
    }
    