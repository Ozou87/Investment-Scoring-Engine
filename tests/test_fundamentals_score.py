
import pytest
from fundamental_module import calculate_fundamental_scores

def test_fundamentals_score_in_range(moker):

    fundamental_input = calculate_fundamental_scores(
        growth_pct=25,
        profit_pct=23,
        debt_to_equity=1.2,
        fcf_margin_pct=5,
        sector_name="Energy"

    )

    result = calculate_fundamental_scores(fundamental_input)

    final_fundamental_score = result["Fundamentals_score"]
    assert isinstance(final_fundamental_score, int)
    assert 0 <= final_fundamental_score <= 100