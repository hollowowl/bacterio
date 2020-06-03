import unittest

from app.hexafield import HexCoords, HexCoordConverter, CircleHexafield, get_step_to, get_distance_between, SQRT3D2

class TestRound(unittest.TestCase):

    def test_round(self):
        self.assertEqual(round(7.5),8)
        self.assertEqual(round(-7.5),-8)
        self.assertEqual(round(-7.4),-7)
        self.assertEqual(round(7.4),7)
        self.assertEqual(round(7),7)
        self.assertEqual(round(-7),-7)


class TestHexCoords(unittest.TestCase):

    def test_eq(self):
        hc1 = HexCoords(1,-1)
        hc2 = HexCoords(-1,1)
        hc3 = HexCoords(1,-1)
        hc4 = HexCoords(1,0)
        hc5 = 42
        self.assertTrue(hc1==hc1)
        self.assertTrue(hc1==hc3)
        self.assertFalse(hc1==hc2)
        self.assertFalse(hc1==hc4)
        self.assertFalse(hc1==hc5)
        self.assertFalse(hc1==None)

    def test_get_distance_between(self):
        self.assertEqual(get_distance_between(HexCoords(1,1),HexCoords(1,1)),0)
        hc1 = HexCoords(0,-1)
        hc2 = HexCoords(-1,2)
        self.assertEqual(get_distance_between(hc1,hc2), 3)
        self.assertEqual(get_distance_between(hc2,hc1), 3)
        hc1 = HexCoords(1,-2)
        hc2 = HexCoords(2,-1)
        self.assertEqual(get_distance_between(hc1,hc2), 2)
        self.assertEqual(get_distance_between(hc2,hc1), 2)

    def test_get_step_to(self):
        self.assertEqual(get_step_to(HexCoords(1,1),HexCoords(1,1)),HexCoords(1,1))
        # neighbours
        hc1 = HexCoords(0,-1)
        hc2 = HexCoords(1,-2)
        self.assertEqual(get_step_to(hc1,hc2),hc2)
        self.assertEqual(get_step_to(hc2,hc1),hc1)
        # far away
        hc1 = HexCoords(-1,-1)
        hc2 = HexCoords(2,-1)
        self.assertEqual(get_step_to(hc1,hc2),HexCoords(0,-1))
        hc1 = HexCoords(-2,2)
        hc2 = HexCoords(2,-2)
        self.assertEqual(get_step_to(hc1,hc2),HexCoords(-1,1))
        # two possible results
        hc1 = HexCoords(0,-1)
        hc2 = HexCoords(1,0)
        hc = get_step_to(hc1,hc2)
        self.assertTrue(hc==HexCoords(0,0) or hc==HexCoords(1,-1))


class TestHexCoordConverter(unittest.TestCase):

    def test_hex_to_plain(self):
        conv = HexCoordConverter(leftHex0=5, topHex0=5, hexRadius=1)
        self.assertEqual(conv.hex_to_plain(HexCoords(0,0)), (5,5))
        self.assertEqual(conv.hex_to_plain(HexCoords(2,-1)), (8,5))
        self.assertEqual(conv.hex_to_plain(HexCoords(0,1)), (5,5-2*SQRT3D2))
        self.assertEqual(conv.hex_to_plain(HexCoords(1,0)), (6.5,5-SQRT3D2))

    def test_plain_to_hex(self):
        conv = HexCoordConverter(leftHex0=5, topHex0=5, hexRadius=1)
        self.assertEqual(conv.plain_to_hex(5,5), HexCoords(0,0))
        self.assertEqual(conv.plain_to_hex(8,5), HexCoords(2,-1))
        self.assertEqual(conv.plain_to_hex(8.5,5), HexCoords(2,-1))
        self.assertEqual(conv.plain_to_hex(7.5,5), HexCoords(2,-1))
        self.assertEqual(conv.plain_to_hex(2.5,5), HexCoords(-2,1))
        self.assertEqual(conv.plain_to_hex(1.5,5), HexCoords(-2,1))
        self.assertEqual(conv.plain_to_hex(5.8,5-SQRT3D2), HexCoords(1,0))


class TestCircleHexafield(unittest.TestCase):

    def test_initialization(self):
        hf = CircleHexafield(1)
        self.assertEqual(len(hf._field),7)
        hf = CircleHexafield(2)
        self.assertEqual(len(hf._field),19)

    def test_get_neighbours(self):
        hf = CircleHexafield(2)
        nb = hf.get_neighbours(HexCoords(1,0))
        self.assertEqual(len(nb),6)
        nb = hf.get_neighbours(HexCoords(0,2))
        self.assertEqual(len(nb),3)
        self.assertTrue( HexCoords(-1,2) in nb)
        self.assertTrue( HexCoords(0,1) in nb)
        self.assertTrue( HexCoords(1,1) in nb)
        nb = hf.get_neighbours(HexCoords(0,2),2)
        self.assertEqual(len(nb),8)

    def test_get_all_within(self):
        hf = CircleHexafield(2)
        nb = hf.get_all_within(HexCoords(1,0),1)
        self.assertEqual(len(nb),7)
        nb = hf.get_all_within(HexCoords(0,2),1)
        self.assertEqual(len(nb),4)
        self.assertTrue( HexCoords(-1,2) in nb)
        self.assertTrue( HexCoords(0,1) in nb)
        self.assertTrue( HexCoords(1,1) in nb)
        self.assertTrue( HexCoords(0,2) in nb)
        nb = hf.get_all_within(HexCoords(0,2),2)
        self.assertEqual(len(nb),9)

    def test_get_at_exact_range(self):
        hf = CircleHexafield(2)
        nb = hf.get_at_exact_range(HexCoords(0,2))
        self.assertEqual(len(nb),3)
        self.assertTrue( HexCoords(-1,2) in nb)
        self.assertTrue( HexCoords(0,1) in nb)
        self.assertTrue( HexCoords(1,1) in nb)
        nb = hf.get_at_exact_range(HexCoords(0,2),2)
        self.assertEqual(len(nb),5)
        self.assertTrue( HexCoords(-2,2) in nb)
        self.assertTrue( HexCoords(-1,1) in nb)
        self.assertTrue( HexCoords(0,0) in nb)
        self.assertTrue( HexCoords(1,0) in nb)
        self.assertTrue( HexCoords(2,0) in nb)

    def test_max_coord_value(self):
        hf = CircleHexafield(7)
        self.assertEqual(hf.get_max_coord_value(), 7)
