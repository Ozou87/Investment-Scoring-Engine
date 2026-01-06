
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
            "Fundamental_Score": 80,
            "Sector_name": "technology"
        }
    )
    

        