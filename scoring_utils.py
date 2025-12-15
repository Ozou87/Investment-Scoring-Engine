#math tool file that calculate values
import math

def score_by_thresholds(value: float, thresholds: list[tuple[float, int]], default_score:int) -> int:
    """
    func will recieve value and convert it to a score from thershold table.
    """
    for limit, score in thresholds:
        if value < limit:
            return score
    return default_score

def score_ratio(
        stock_value: float,
        sector_value: float,
        thersholds: list[tuple[float, int]],
        default_score: int,
                ) -> int:
    """
    specific function for Ratios
    """
    if sector_value == 0 or math.isnan(stock_value) or math.isnan(sector_value):
        return default_score
    
    relative_multiple = stock_value / sector_value
    return score_by_thresholds(relative_multiple, thersholds, default_score)
    
