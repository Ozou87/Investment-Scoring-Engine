import math

#creating a Class for both scoring tools
class ScoringMethods:
    
    #here only parameters that are avalable to any function inside the Class
    #no need to pass them again to the functions
    #instance atribiutes
    #parameter that belogs to the calculation method -> will be in __int__
    def __init__(self, thresholds: list[tuple[float, int]], default_score: int):
        self.thresholds = thresholds
        self.default_score = default_score

    #stock value and sector value
    #Go in only when icall the function
    #Once the function ends, paramerters dissapear
    #Method paramerters
    #parameter that belogs to the specific current calcualtion proccess -> will NOT be in __int__
    def threshold_based_score(self, stock_value) -> int:

        for limit, score in self.thresholds:
            if stock_value < limit:
                return score
        return self.default_score

    def score_relative_to_sector(self, stock_value, sector_value) -> int:
        
        if sector_value == 0 or math.isnan(stock_value) or math.isnan(sector_value):
            return self.default_score
    
        relative_multiple = stock_value / sector_value
        return self.threshold_based_score(relative_multiple)

