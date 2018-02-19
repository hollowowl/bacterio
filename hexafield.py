'''
Here we use isometric approach for calculating hexagons
Each given hexagon has 3 coords: X, Y, Z

    Y___
    /   \X
    \___/
    Z
    
For every hexagon X+Y+Z remains constant (as far as for every shift one coord doesn't change, one increases by 1, and the left one decreases by one)
Consider hexagon with coords (0,0,0).
Its heighbours will have coords (0,1,-1), (1,0,-1), (1,-1,0), (0,-1,1), (-1,0,1), (-1, 1, 0)
X+Y+Z=0 for every hexagon 
So far every hexagon can be characterized only having 2 coords (we will use X and Y, Z=-X-Y)
 *       __
 *    __/01\__
 *   /-1\__/10\__
 *   \__/00\__/2-\
 *   /-0\__/1-\__/
 *   \__/0-\__/
 *      \__/        
 

'''

import math

class HexCoords(object):
    '''
    z always equal to -x-y
    '''
    __slots__ = ['x', 'y']
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def shift(self, dx=0, dy=0):
        '''
        Returns shifted HexCoords
        '''
        return HexCoords(self.x+dx, self.y+dy)
    
    def __eq__(self, other):
        if isinstance(other, HexCoords):
            return self.x==other.x and self.y==other.y
        return False
        
    def __hash__(self):
        return hash((self.x,self.y))
    
    def __repr__(self):
        return 'HexCoords(x=%s, y=%s)' % (self.x, self.y)


class HexafieldBase(object):
    '''
    Describes hexagonal field.
    field is dictionary where keys are HexCoords and values are any objects
    (None by default)
    '''
    __slots__ = ['field']
    
    def __init__(self, field):
        self.field = field
    
    def get_neighbours(self, hexCoords, radius = 1):
        '''
        Returns list of tuples (HexCoords, object) of all cells close to hexCoords
        in given radius (excluding hexCoords itself)
        '''
        res = []
        for dx in range(-radius, radius+1):
            for dy in range (-radius, radius+1):
                if abs(dx+dy)<=radius and abs(dx)+abs(dy)>0:
                    hc = HexCoords(hexCoords.x+dx, hexCoords.y+dy)
                    if hc in self.field:
                        res.append((hc,self.field[hc]))
        return res
    
    def get_at_exact_range(self, hexCoords, radius = 1):
        '''
        Returns list of tuples (HexCoords, object) of all cells located at
        exact radius from hexCoords
        TODO: need optimizations - its not good to iterate through such big area
        '''
        res = []
        for dx in range(-radius, radius+1):
            for dy in range (-radius, radius+1):
                if abs(dx+dy) + abs(dx) + abs(dy)==2*radius:
                    hc = HexCoords(hexCoords.x+dx, hexCoords.y+dy)
                    if hc in self.field:
                        res.append((hc,self.field[hc]))
        return res


class CircleHexafield(HexafieldBase):
    '''
    Describes circle-shaped hexagonal field
    '''
    __slots__ = []
    def __init__(self, fieldRadius = 2):
        field = {}
        for x in range(-fieldRadius, fieldRadius+1):
            for y in range(-fieldRadius, fieldRadius+1):
                if abs(x+y)<=fieldRadius:
                    field[HexCoords(x,y)] = None
        HexafieldBase.__init__(self,field)
    


SQRT3D2 = math.sqrt(3.0)/2.0

def round(x):
    '''
    Rounds to nearest integer
    '''
    i = math.trunc(x)
    diff = x-i
    if (diff<=-0.5): return i-1
    if (diff>=0.5): return i+1
    return i


class HexCoordConverter(object):
    '''
    Converts HexCoords to plain (top, left) and vice-versa.
    '''
    __slots__=['leftHex0', 'topHex0', 'hexRadius', 'hexHeight']
    
    def __init__(self, leftHex0=0.0, topHex0=0.0, hexRadius=1.0):
        '''
        topHex0 and leftHex0 are plain coords of the center of hex with coords (0,0,0),
        hexRadius is a distance between hex's center and hex's corner in plain coords.
        hexHeight could be calculated from simple geometric equation:
            hexHeight^2 + (hexRadius/2)^2 = hexRadius^2
        so
            hexHeight = sqrt(3)/2 * hexRadius
        '''
        self.leftHex0 = leftHex0
        self.topHex0 = topHex0
        self.hexRadius = hexRadius
        self.hexHeight = SQRT3D2 * hexRadius
    
    def hex_to_plain(self, hexCoords):
        '''
        returns plain coords of the center of given hex as a tuple (left, top)
        '''
        left = self.leftHex0 + hexCoords.x*1.5*self.hexRadius
        top = self.topHex0 - hexCoords.y*2*self.hexHeight - hexCoords.x*self.hexHeight
        return (left, top)
    
    def plain_to_hex(self, left, top):
        '''
        returns HexCoords which contains (left,top) plain point
        '''
        hexCoords = HexCoords(x = round((left - self.leftHex0)/(1.5*self.hexRadius)))
        hexCoords.y = round( (top-self.topHex0+hexCoords.x*self.hexHeight)/(-2.0*self.hexHeight) )
        return hexCoords
    
    def get_hex_vertices(self, hexCoords):
        '''
        Calculates plain coords of vertices of hexagon with given hexCoords.
        Returns list of hexagon coorditanes
        '''
        center = self.hex_to_plain(hexCoords)
        return [ center[0]-self.hexRadius, center[1],
                 center[0]-self.hexRadius/2.0, center[1]-self.hexHeight,
                 center[0]+self.hexRadius/2.0, center[1]-self.hexHeight,
                 center[0]+self.hexRadius, center[1],
                 center[0]+self.hexRadius/2.0, center[1]+self.hexHeight,
                 center[0]-self.hexRadius/2.0, center[1]+self.hexHeight
        ]

if __name__=='__main__':
    import unittest

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
            self.assertEqual(len(hf.field),7)
            hf = CircleHexafield(2)
            self.assertEqual(len(hf.field),19)
            
        def test_get_neighbours(self):
            hf = CircleHexafield(2)
            nb = hf.get_neighbours(HexCoords(1,0))
            self.assertEqual(len(nb),6)
            nb = hf.get_neighbours(HexCoords(0,2))
            self.assertEqual(len(nb),3)
            self.assertTrue( (HexCoords(-1,2), None) in nb)
            self.assertTrue( (HexCoords(0,1), None) in nb)
            self.assertTrue( (HexCoords(1,1), None) in nb)
            nb = hf.get_neighbours(HexCoords(0,2),2)
            self.assertEqual(len(nb),8)
            
        def test_get_at_exact_range(self):
            hf = CircleHexafield(2)
            nb = hf.get_at_exact_range(HexCoords(0,2))
            self.assertEqual(len(nb),3)
            self.assertTrue( (HexCoords(-1,2), None) in nb)
            self.assertTrue( (HexCoords(0,1), None) in nb)
            self.assertTrue( (HexCoords(1,1), None) in nb)
            nb = hf.get_at_exact_range(HexCoords(0,2),2)
            self.assertEqual(len(nb),5)
            self.assertTrue( (HexCoords(-2,2), None) in nb)
            self.assertTrue( (HexCoords(-1,1), None) in nb)
            self.assertTrue( (HexCoords(0,0), None) in nb)
            self.assertTrue( (HexCoords(1,0), None) in nb)
            self.assertTrue( (HexCoords(2,0), None) in nb)

    
    unittest.main()
