import yfinance as yf
import contextlib
import io

#is it in USE?
class DataFetchError(Exception):
    """Raised when the external data source fails or returns invalid data."""
    
def fetch_company_metadata(ticker: str) -> dict:
    if not ticker or not ticker.strip():
        raise ValueError("Ticker is required")
    
    clean_ticker = ticker.strip().upper()

    #fetch from yahoo finance
    try:
    #Silence noisy output that may be printed by yfinance/urllib
    
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            t = yf.Ticker(clean_ticker)
            info = t.info

    except Exception:
    #Raise a user-friendly error without leaking internal HTTP details
        raise DataFetchError(f"Ticker {clean_ticker} not found") from None
    
    #Validate response is usable
    if not isinstance(info, dict) or len(info) == 0:
        raise DataFetchError(f"No metadata returned for ticker: {clean_ticker}")
    
    if not (info.get("shortName") or info.get("longName")):
        raise DataFetchError(f"Ticker {clean_ticker} not found (no company name)")

    #Extract fields safely 
    company_name = info.get("shortName") or info.get("longName") 
    sector = info.get("sector")  

    return {
        "ticker": clean_ticker,
        "company_name": company_name,
        "sector": sector
    }

      
