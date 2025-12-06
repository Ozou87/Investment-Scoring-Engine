


#loop that make sure its float and system wont crash
def get_float(prompt) -> float:

    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid input. PLS try again ")




#asking user for fundamentals inputs: (in the future will be API)
revenue_growth = get_float("Enter stock Revenue Growth %: ")
operating_margin = get_float("Enter stock Operating margin %: ")
debt_to_equity = get_float("Enter stock Debt to Equity ratio: ")
fcf_margin = get_float("Enter stock Free Cash Flow Margin %: ")

#placholder for Valuation values
#placholder for Moat values

#starting the fundamental cycle in order to get data
#fundamental_output = calculate_fundamental_scores(revenue_growth,operating_margin,debt_to_equity,fcf_margin)
# print(f"Score is: {fundamental_output}")


#valuation_output = 
#print(valuation_output)

#,oat_output = 
#print(moat_output)









