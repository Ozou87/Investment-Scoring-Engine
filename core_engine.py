
from fundamental_module import calculate_fundamental_scores
from valuation_module import calculate_valuation_scores
from moat_module import calculate_moat_scores
from config import final_score_weight

from dataclasses import dataclass

@dataclass
class Fundamental_input:
    revenue_growth_pct: float
    operating_margin_pct: float
    debt_to_equity_ratio: float
    free_cash_flow_margin_pct: float
    sector: str

@dataclass
class Valuation_input:
    stock_pe : float
    sector_median_pe: float
    stock_forward_pe: float
    sector_median_forward_pe: float
    stock_ev_ebitda_multiple: float
    sector_median_ev_ebitda_multiple: float
    stock_price_to_sales_multiple: float
    sector_median_price_to_sales_multiple: float
    stock_price_to_free_cash_flow_multiple: float
    sector_median_price_to_free_cash_flow_multiple: float
    sector: str

@dataclass
class Moat_input:
    return_on_investment_capital_pct: float
    free_cash_flow_3y_cagr: float
    gross_margin_list: list[float]
    r_and_d_raw: float
    revenue_growth_raw: float
    sector: str
        
def calculate_all_scores(
        fundamental_input: Fundamental_input,
        valuation_input: Valuation_input, 
        moat_input: Moat_input
                        ):

    revenue_growth_pct = fundamental_input.revenue_growth_pct
    operating_margin_pct = fundamental_input.operating_margin_pct
    debt_to_equity_ratio = fundamental_input.debt_to_equity_ratio
    free_cash_flow_margin_pct = fundamental_input.free_cash_flow_margin_pct
    f_sector_name = fundamental_input.sector

    fundamentals_scores = calculate_fundamental_scores(
        revenue_growth_pct = revenue_growth_pct,
        operating_margin_pct = operating_margin_pct,
        debt_to_equity_ratio = debt_to_equity_ratio,
        free_cash_flow_margin_pct = free_cash_flow_margin_pct,
        sector_name = f_sector_name
                                                        )

    stock_pe = valuation_input.stock_pe
    sector_median_pe = valuation_input.sector_median_pe
    stock_forward_pe = valuation_input.stock_forward_pe
    sector_median_forward_pe = valuation_input.sector_median_forward_pe
    stock_ev_ebitda_multiple = valuation_input.stock_ev_ebitda_multipe
    sector_median_ev_ebitda_multiple = valuation_input.sector_median_ev_ebitda_multiple
    stock_price_to_sales_multiple = valuation_input.stock_price_to_sales_multiple
    sector_median_price_to_sales_multiple = valuation_input.sector_median_price_to_sales_multiple
    stock_price_to_free_cash_flow_multiple = valuation_input.stock_price_to_free_cash_flow_multiple
    sector_median_price_to_free_cash_flow_multiple = valuation_input.sector_median_price_to_free_cash_flow_multiple
    v_sector_name = valuation_input.sector

    valuation_scores = calculate_valuation_scores(
        stock_pe = stock_pe,
        sector_median_pe = sector_median_pe,
        stock_forward_pe = stock_forward_pe,
        sector_median_forward_pe = sector_median_forward_pe,
        stock_ev_ebitda_multiple = stock_ev_ebitda_multiple,
        sector_median_ev_ebitda_multiple = sector_median_ev_ebitda_multiple,
        stock_price_to_sales_multiple = stock_price_to_sales_multiple,
        sector_median_price_to_sales_multiple = sector_median_price_to_sales_multiple,
        stock_price_to_free_cash_flow_multiple = stock_price_to_free_cash_flow_multiple,
        sector_median_price_to_free_cash_flow_multiple = sector_median_price_to_free_cash_flow_multiple,
        sector_name = v_sector_name
                                                )

    return_on_investment_capital_pct = moat_input.return_on_investment_capital_pct
    free_cash_flow_3y_cagr = moat_input.free_cash_flow_3y_cagr
    gross_margin_list = moat_input.gross_margin_list
    r_and_d_raw = moat_input.r_and_d_raw
    revenue_growth_raw = moat_input.revenue_growth_raw
    m_sector_name = moat_input.sector

    moat_scores = calculate_moat_scores(
        return_on_investment_capital_pct = return_on_investment_capital_pct,
        free_cash_flow_3y_cagr = free_cash_flow_3y_cagr,
        gross_margin_list = gross_margin_list,
        r_and_d_raw = r_and_d_raw,
        revenue_growth_raw = revenue_growth_raw,
        sector_name = m_sector_name
                                        )
    # Extracting final scores from each module
    fundamentals_total = fundamentals_scores["fundamentals_score"]
    valuation_total = valuation_scores["valuation_score"]
    moat_total = moat_scores["moat_score"]

    # Extracting sector_name
    SECTOR_NAME = fundamentals_scores["sector_name"]

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