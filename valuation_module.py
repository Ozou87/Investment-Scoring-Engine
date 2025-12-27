from scoring_utils import score_ratio
from config import valuation_weight

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
F_PE_RATIO_THRESHOLDS = [
    (0.60,95),
    (0.80,90),
    (0.90,75),
    (1.10,55),
    (1.30,40),
    (1.60,25),
    (2.00,15),
            ]
F_PE_DEFAULT = 5

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

#specific function that sends info to the generic function in order to help it find score
def pe_ratio(stock_pe: float, sector_pe:float) -> int:
    return score_ratio(stock_pe, sector_pe, PE_RATIO_THRESHOLDS, PE_RATIO_DEFAULT )

def forward_pe_ratio(stock_f_pe: float, sector_f_pe:float) -> int:
    return score_ratio(stock_f_pe, sector_f_pe, F_PE_RATIO_THRESHOLDS, F_PE_DEFAULT)

def evebitda_ratio(stock_eveb:float, sector_eveb:float) -> int:
    return score_ratio(stock_eveb, sector_eveb, EVEBITDA_RATIO_THRESHOLDS, EVEBITDA_RATIO_DEFAULT)

def ps_ratio(stock_ps:float, sector_ps: float) -> int:
    return score_ratio(stock_ps, sector_ps, PS_RATIO_THRESHOLDS, PS_RATIO_DEFAULT)

def price_fcf_ratio(stock_pfcf:float, sector_pfcf: float) -> int:
    return score_ratio(stock_pfcf, sector_pfcf, PFCF_RATIO_THRESHOLDS, PFCF_RATIO_DEFAULT)

def valuation_weighted_score(
        pe:int,
        fpe:int,
        eveb:int,
        ps: int,
        pfcf:int,
        wbs: dict
                            ) -> int:
    """
    Calculates the final valuation score using fixed weights:
    PE         - 30%
    forward PE - 25%
    EV_ebitda  - 20%
    PS         - 15%
    price_FCF  - 10%

    """
    weighted_together = (0.3 * pe + 0.25 * fpe + 0.2 * eveb + 0.15 * ps + 0.1 * pfcf)
    return round(weighted_together)

def calculate_valuation_scores(
    stock_pe: float,
    sector_pe: float,
    stock_fpe: float,
    sector_fpe:float,
    stock_eveb:float,
    sector_eveb: float,
    stock_ps: float,
    sector_ps:float,
    stock_pfcf: float,
    sector_pfcf:float,
    sector_name:str,
                              ) -> dict:   
    """
    Core function of the valuation module.
    Gets raw inputs and returns all scores + final valuation_score.
    """
    pe = pe_ratio(stock_pe, sector_pe)
    fpe = forward_pe_ratio(stock_fpe, sector_fpe)
    eveb = evebitda_ratio(stock_eveb, sector_eveb)
    ps = ps_ratio(stock_ps, sector_ps)
    pfcf = price_fcf_ratio(stock_pfcf, sector_pfcf)
    weight_by_sector = valuation_weight(sector_name)

    final_score = valuation_weighted_score(pe, fpe, eveb, ps, pfcf, weight_by_sector)

    return {
        "pe_score": pe,
        "forward_pe_score": fpe,
        "ev_ebitda_score": eveb,
        "ps_score": ps,
        "price_fcf_score": pfcf,
        "weight_currently_being used": weight_by_sector,
        "valuation_score": final_score
           }

    





