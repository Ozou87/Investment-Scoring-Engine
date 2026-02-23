import math

def threshold_based_score(value: float, thresholds: list[tuple[float, int]], default_score:int) -> int:
    """
    function will recieve value and convert it to a score from thershold table.
    """
    for limit, score in thresholds:
        if value < limit:
            return score
    return default_score

def score_relative_to_sector(
        stock_value: float,
        sector_value: float,
        thresholds: list[tuple[float, int]],
        default_score: int,
                ) -> int:
    """
    function for relative to sector scores
    """
    if sector_value == 0 or math.isnan(stock_value) or math.isnan(sector_value):
        return default_score
    
    relative_multiple = stock_value / sector_value
    return threshold_based_score(relative_multiple, thresholds, default_score)
    
class ThresholdScorer:
    def __init__(self, thresholds: list[tuple[float, int]], default_score: int):
        # state: החוקים נשמרים בתוך האובייקט
        self.thresholds = thresholds
        self.default_score = default_score

    def score(self, value: float) -> int:
        # behavior: משתמש בחוקים ששמרנו
        return threshold_based_score(value, self.thresholds, self.default_score)

    def score_relative(self, stock_value: float, sector_value: float) -> int:
        return score_relative_to_sector(
            stock_value=stock_value,
            sector_value=sector_value,
            thresholds=self.thresholds,   # שים לב: אצלך זה כתוב "thersholds" בפונקציה
            default_score=self.default_score,
        )
