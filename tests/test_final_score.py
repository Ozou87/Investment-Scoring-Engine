
import pytest
from core_engine import (
    calculate_all_scores, 
    Fundamental_input, 
    Valuation_input, 
    Moat_input)


def test_fs_in_range(mocker):

    mocker.patch(
        "core_engine.calculate_fundamental_scores",
        return_value={
            "Fundamentals_score": 80,
            "Sector_name": "technology"
        }
    )
    
    mocker.patch(
        "core_engine.calculate_valuation_scores",
        return_value={
            "Valuation_score": 60
        }
    )

    mocker.patch(
        "core_engine.calculate_moat_scores",
        return_value={
            "Moat_score": 85
        }
    )

    mocker.patch(
        "core_engine.final_score_weight",
        return_value={
            "f_weight": 0.4,
            "v_weight": 0.3,
            "m_weight": 0.3
        }
    )

    fundamental_input = Fundamental_input(
        revenue_growth=10,
        operating_margin=20,
        debt_to_equity=1.0,
        fcf_margin=15,
        sector="technology"
    )

    valuation_input = Valuation_input(
        stock_pe=20,
        sector_pe=25,
        stock_fpe=18,
        sector_fpe=22,
        stock_eveb=15,
        sector_eveb=18,
        stock_ps=5,
        sector_ps=6,
        stock_pfcf=20,
        sector_pfcf=25,
        sector="technology"
    )

    moat_input = Moat_input(
        roic_raw_value=15,
        fcf_growth_raw=10,
        gross_margin_list=[60, 61, 59, 62, 60],
        r_and_d_raw=100,
        revenue_raw=1000,
        sector="technology"
    )

    """
    RUN
    """
    result = calculate_all_scores(fundamental_input,valuation_input,moat_input)

    final_score = result["final_score"]


    assert isinstance(final_score, int)
    assert 0 <= final_score <= 100
