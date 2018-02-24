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



if __name__=='__main__':
    import unittest
    
    class TestCountDecimalPlaces(unittest.TestCase):
        def test_float(self):
            self.assertEqual(count_decimal_places(0),0)
            self.assertEqual(count_decimal_places(0.5),1)
            self.assertEqual(count_decimal_places(0.503),3)
            self.assertEqual(count_decimal_places(0.550066),6)
    
        def test_str(self):
            self.assertEqual(count_decimal_places('0'),0)
            self.assertEqual(count_decimal_places('0.5'),1)
            self.assertEqual(count_decimal_places('0.503'),3)
            self.assertEqual(count_decimal_places('0.550066'),6)
    
        def test_decimal(self):
            self.assertEqual(count_decimal_places(decimal.Decimal('0')),0)
            self.assertEqual(count_decimal_places(decimal.Decimal('0.5')),1)
            self.assertEqual(count_decimal_places(decimal.Decimal('0.503')),3)
            self.assertEqual(count_decimal_places(decimal.Decimal('0.550066')),6)
    
    
    class TestRandP(unittest.TestCase):
        def test_float(self):
            p = 0.7
            s = 0
            sf = count_decimal_places(p)
            for x in range(100000):
                s+=rand_p(p,sf)
            self.assertGreaterEqual(s,69500)
            self.assertLessEqual(s,70500)
            
        def test_decimal(self):
            p = decimal.Decimal('0.7')
            s = 0
            sf = count_decimal_places(p)
            for x in range(100000):
                s+=rand_p(p,sf)
            self.assertGreaterEqual(s,69500)
            self.assertLessEqual(s,70500)

            
    
    unittest.main()
