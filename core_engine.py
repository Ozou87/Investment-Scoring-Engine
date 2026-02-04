
from fundamental_module import calculate_fundamental_scores
from valuation_module import calculate_valuation_scores
from moat_module import calculate_moat_scores
from config import final_score_weight

from dataclasses import dataclass

@dataclass
class Fundamental_input:
    revenue_growth_yoy: float
    gross_margin_ttm: float
    debt_to_equity: float
    fcf_margin: float
    sector: str

@dataclass
class Valuation_input:
    stock_pe : float
    sector_pe: float
    stock_fpe: float
    sector_fpe: float
    stock_eveb: float
    sector_eveb: float
    stock_ps: float
    sector_ps: float
    stock_pfcf: float
    sector_pfcf: float
    sector: str

@dataclass
class Moat_input:
    roic_raw_value: float
    fcf_growth_raw: float
    gross_margin_list: list[float]
    r_and_d_raw: float
    revenue_raw: float
    sector: str
        
def calculate_all_scores(
        fundamental_input: Fundamental_input,
        valuation_input: Valuation_input, 
        moat_input: Moat_input
                        ):

    revenue_growth_yoy = fundamental_input.revenue_growth_yoy
    gross_margin_ttm = fundamental_input.gross_margin_ttm
    debt_to_equity = fundamental_input.debt_to_equity
    fcf_margin = fundamental_input.fcf_margin
    f_sector_name = fundamental_input.sector

    fundamentals_scores = calculate_fundamental_scores(
        revenue_growth_yoy = revenue_growth_yoy,
        gross_margin_ttm = gross_margin_ttm,
        debt_to_equity = debt_to_equity,
        fcf_margin_pct = fcf_margin,
        sector_name = f_sector_name
                                                        )


    stock_pe = valuation_input.stock_pe
    sector_pe = valuation_input.sector_pe
    stock_fpe = valuation_input.stock_fpe
    sector_fpe = valuation_input.sector_fpe
    stock_eveb = valuation_input.stock_eveb
    sector_eveb = valuation_input.sector_eveb
    stock_ps = valuation_input.stock_ps
    sector_ps = valuation_input.sector_ps
    stock_pfcf = valuation_input.stock_pfcf
    sector_pfcf = valuation_input.sector_pfcf
    v_sector_name = valuation_input.sector

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
        sector_pfcf = sector_pfcf,
        sector_name = v_sector_name
                                                )

    roic_raw_value = moat_input.roic_raw_value
    fcf_growth_raw = moat_input.fcf_growth_raw
    gross_margin_list = moat_input.gross_margin_list
    r_and_d_raw = moat_input.r_and_d_raw
    revenue_raw = moat_input.revenue_raw
    m_sector_name = moat_input.sector

    moat_scores = calculate_moat_scores(
        roic_raw_value = roic_raw_value,
        fcf_growth_raw = fcf_growth_raw,
        gross_margin_list = gross_margin_list,
        r_and_d_raw = r_and_d_raw,
        revenue_raw = revenue_raw,
        sector_name = m_sector_name
                                        )
    # Extracting final scores from each module
    fundamentals_total = fundamentals_scores["Fundamentals_score"]
    valuation_total = valuation_scores["Valuation_score"]
    moat_total = moat_scores["Moat_score"]

    # Extracting sector_name
    SECTOR_NAME = fundamentals_scores["Sector_name"]

    # calling func of final weights
    dict_of_final_weights = final_score_weight(SECTOR_NAME)
    fw = dict_of_final_weights["f_weight"]
    vw = dict_of_final_weights["v_weight"]
    mw = dict_of_final_weights["m_weight"]

    final_score = round(fw * fundamentals_total + vw * valuation_total + mw * moat_total)

    return {
        "fundamentals": fundamentals_scores,
        "valuation": valuation_scores,
        "moat": moat_scores,
        "final_score": final_score,
            }