
from fundemental_module import calculate_fundamental_scores
from valuation_module import calculate_valuation_scores
from moat_module import calculate_moat_scores

def calculate_all_scores(fundamental_input: dict, valuation_input: dict, moat_input: dict):

    revenue_growth = fundamental_input["revenue_growth"]
    operating_margin = fundamental_input["operating_margin"]
    debt_to_equity = fundamental_input["debt_to_equity"]
    fcf_margin = fundamental_input["fcf_margin"]

    fundamentals_scores = calculate_fundamental_scores(
        growth_pct = revenue_growth,
        profit_pct = operating_margin,
        debt_to_equity = debt_to_equity,
        fcf_margin_pct = fcf_margin
                                                        )

    stock_pe = valuation_input["stock_pe"]
    sector_pe = valuation_input["sector_pe"]
    stock_fpe = valuation_input["stock_fpe"]
    sector_fpe = valuation_input["sector_fpe"]
    stock_eveb = valuation_input["stock_eveb"]
    sector_eveb = valuation_input["sector_eveb"]
    stock_ps = valuation_input["stock_ps"]
    sector_ps = valuation_input["sector_ps"]
    stock_pfcf = valuation_input["stock_pfcf"]
    sector_pfcf = valuation_input["sector_pfcf"]

    valuation_scores = calculate_valuation_scores(
        stock_pe = stock_pe,
        sector_pe = sector_pe,
        stock_fpe = stock_fpe,
        sector_fpe = sector_fpe,
        stock_eveb = stock_eveb,
        sector_eveb = sector_eveb,
        stock_ps = stock_ps,
        sector_ps = sector_ps,
        stock_pfcf = stock_pfcf,
        sector_pfcf = sector_pfcf
                                                )

    roic_raw_value = moat_input["roic_raw_value"]
    fcf_growth_raw = moat_input["fcf_growth_raw"]
    gross_margin_list = moat_input["gross_margin_list"]
    r_and_d_raw = moat_input["r_and_d_raw"]
    revenue_raw = moat_input["revenue_raw"]


    moat_scores = calculate_moat_scores(
        roic_raw_value = roic_raw_value,
        fcf_growth_raw = fcf_growth_raw,
        gross_margin_list = gross_margin_list,
        r_and_d_raw = r_and_d_raw,
        revenue_raw = revenue_raw
                                        )