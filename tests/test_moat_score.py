
from moat_module import calculate_moat_scores

def test_moat_score_int_range():
    result = calculate_moat_scores(

    roic_raw_value=15,
    fcf_growth_raw=13,
    gross_margin_list= [11,13,14,15,16],
    r_and_d_raw=11,
    revenue_raw=16,
    sector_name="Real estate"
    )

    final_moat_score = result["Moat_score"]

    assert isinstance (final_moat_score, int)
    assert 0 <= final_moat_score <= 100

    