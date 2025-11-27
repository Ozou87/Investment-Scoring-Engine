PE_INVALID = float('nan')
PE_RATIO_THRESHOLDS = [
    (0.6,95),
    (0.85,80),
    (1.15,50),
    (1.5,30),
    (2.0,15),
                    ]
PE_RATIO_DEFAULT = 0

F_PE_INVALID = float('nan')
F_PE_RATIO = [
    (0.60,95),
    (0.80,90),
    (0.90,75),
    (1.10,55),
    (1.30,40),
    (1.60,25),
    (2.00,15),
            ]
F_PE_DEFAULT = 5

PS_INVALID = float('nan')
PS_RATIO_THRESHOLDS = [
    (0.70, 95), 
    (0.90, 85),    
    (1.10, 60),   
    (1.40, 40),   
    (2.00, 25),   
    (3.00, 15),  
                    ]
PS_RATIO_DEFAULT = 5   

EVEBITDA_INVALID = float('nan')
EVEBITDA_RATIO_THRESHOLDS = [
    (0.70, 95),   
    (0.90, 85),   
    (1.10, 60),   
    (1.40, 40),   
    (2.00, 25),  
    (3.00, 15),   
                            ]
EVEBITDA_RATIO_DEFAULT = 5   

PFCF_INVALID = float('nan')
PFCF_RATIO_THRESHOLDS = [
    (0.70, 95),   
    (0.90, 85),  
    (1.10, 60),   
    (1.40, 40),   
    (2.00, 25),   
    (3.00, 15), 
                        ]
PFCF_RATIO_DEFAULT = 5   

#generic function that will find score and send it to specific function
def score_by_thresholds(stock_value: float, sector_value: float, thresholds, pe_default) -> float:
    
    #להוסיף הגנה מפני חלוקה ב-0

    relative_multiple = stock_value / sector_value

    for limit, score in thresholds:
        if relative_multiple < limit:
            return score
    return pe_default

stock_pe = input("pls enter stock pe: ")
sector_pe = input("pls enter sector pe: ")
st_pe = float(stock_pe)
sec_pe = float(sector_pe)

result_1 = score_by_thresholds(st_pe,sec_pe, PE_RATIO_THRESHOLDS, PE_RATIO_DEFAULT)
print(f"this is the score for this data: {result_1}")

