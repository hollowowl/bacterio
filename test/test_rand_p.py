import unittest
import decimal

from app.rand_p import count_decimal_places, rand_p

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
