
#creating table with limits and score limits
GROWTH_THRESHOLDS = [
    (0.0,20),
    (5.0,40),
    (15.0,60),
    (30.0,80),
                    ]
GROWTH_DEFAULT = 95

PROFIT_THRESHOLDS = [
    (0.0,20),
    (5.0,40),
    (15.0,60),
    (25,80),
                    ]
PROFIT_DEFAULT = 95

DER_THRESHOLDS = [
    (0.2, 95), 
    (0.5, 80),  
    (1.0, 60), 
    (2.0, 40),
                 ]
DER_DEFAULT = 20

FCF_THRESHOLDS = [
    (0, 20),
    (5, 40),
    (10, 60),
    (20, 80),
                ]
FCF_DEFAULT = 95

#generic function that will find score and send it to specific function
def score_by_thresholds(value, thresholds, default_score):
    for limit, score in thresholds:
        if value < limit:
            return score
    return default_score

#specific function that sends info to the generic function in order to help it find score
def growth_score(growth_pct: float) -> int:
    return score_by_thresholds(growth_pct, GROWTH_THRESHOLDS, GROWTH_DEFAULT)

def profit_score(profit_pct: float) -> int:
    return score_by_thresholds(profit_pct,PROFIT_THRESHOLDS,PROFIT_DEFAULT)

def der_score(debt_to_eqity: float) -> int:
    return score_by_thresholds(debt_to_eqity,DER_THRESHOLDS,DER_DEFAULT)

def fcf_score(free_cash_flow: float) -> int:
    return score_by_thresholds(free_cash_flow,FCF_THRESHOLDS,FCF_DEFAULT)

#let user input values
user_growth_input = input("PLS enter Annual Revenue Growth in %: ")
user_profit_input = input("PLS enter Operating Margin in %: ")
user_der_input = input("PLS enter Dept to Equity Ratio: ")
user_fcf_input = input("PLS enter Free Cash Flow Margin in %: ")

#converting the input into a float
growth_value = float(user_growth_input)
profit_value = float(user_profit_input)
der_value = float(user_der_input)
fcf_value = float(user_fcf_input)

#calling the generic functions and storing the value in "result_ "
result_1 = growth_score(growth_value)
result_2 = profit_score(profit_value)
result_3 = der_score(der_value)
result_4 = fcf_score(fcf_value)

#funcion that calculate the weighted of all results and bring back final score
def fundemental_score(g:int, p:int, d:int, f:int) -> int:

    weighted_together = (0.3 * g + 0.3 * p + 0.2 * d + 0.2 * f)
    return round(weighted_together)

#calling to weighted func and sending all the results
final_fun_score = fundemental_score(result_1,result_2,result_3,result_4)

print(f"The fundemental score is: {final_fun_score}")

