'''
Generates 0 or 1 with given probability
'''

import decimal
import random


def count_decimal_places(p) -> int:
    '''
    p is probability (as float number or decimal.Decimal or string like '0.045').
    Float will be converted to str to avoid counting long mantissa tail.
    Returns number of digits after decimal point
    '''
    if isinstance(p,decimal.Decimal):
        return -p.as_tuple().exponent
    if isinstance(p,str):
        return -decimal.Decimal(p).as_tuple().exponent
    return -decimal.Decimal(str(p)).as_tuple().exponent


def rand_p(p, sig_figures=None) -> int:
    '''
    p is probability (as float number or decimal.Decimal or string like '0.045').
    sig_figures is number of significant figures (if None it will be calculated with count_decimal_places).
    Retuns 1 with probability p or 0 with probability (1-p)
    '''
    sf = count_decimal_places(p) if sig_figures is None else sig_figures
    rbound = 10**sf
    if isinstance(p,(decimal.Decimal,float)):
        offset = p*rbound
    elif isinstance(p,str):
        offset = float(p)*rbound
    return 1 if random.randrange(rbound)<offset else 0
