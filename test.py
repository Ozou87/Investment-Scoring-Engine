
import yfinance as yf

ticker = yf.Ticker("pltr")

quarterly = ticker.quarterly_financials
revenue_q = quarterly.loc["Total Revenue"]

ttm_current = revenue_q.iloc[0:4].sum()
ttm_previous = revenue_q.iloc[4:8].sum()

ttm_yoy_growth = ((ttm_current - ttm_previous) / ttm_previous) * 100
print(ttm_yoy_growth)



t = yf.Ticker("PLTR")
q = t.quarterly_financials  # Income Statement רבעוני

gross_profit_q = q.loc["Gross Profit"]
revenue_q = q.loc["Total Revenue"]

gp_ttm = gross_profit_q.iloc[0:4].sum()
rev_ttm = revenue_q.iloc[0:4].sum()

gross_margin_ttm = (gp_ttm / rev_ttm) * 100
print(gross_margin_ttm)


