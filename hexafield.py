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
    _coords is tuple (x,y). x and y are integers.
    (z always equal to -x-y)
    Assumed that HexCoords is immutable.
    To access coordinate components 'x','y' and 'z' properties could be used.
    '''
    __slots__ = ['_coords']
    
    def __init__(self, x, y):
        self._coords = (x,y)
    
    @property
    def x(self):
        return self._coords[0]
    
    @property
    def y(self):
        return self._coords[1]
    
    @property
    def z(self):
        return -self._coords[0]-self._coords[1]
        
    def __eq__(self, other):
        if isinstance(other, HexCoords):
            return self._coords == other._coords
        return False
        
    def __hash__(self):
        return hash(self._coords)
    
    def __repr__(self):
        return 'HexCoords(x=%s, y=%s)' % (self.x, self.y)


def make_hex_coords(x=None, y=None, z=None, base=HexCoords(0,0)):
    '''
    Makes HexCoords using any two of three coordinates and shift them corresponding to base.
    (Two of coordinates MUST be specified)
    '''
    if x is None:
        x = -y-z
    elif y is None:
        y = -x-z
    return HexCoords(base.x+x,base.y+y)


def get_distance_between(hcFrom, hcTo):
    '''
    Returns distance (in cells) between hcFrom and hcTo.
    If hcFrom==hcTo, returns 0.
    '''
    return (abs(hcTo.x-hcFrom.x)+abs(hcTo.y-hcFrom.y)+abs(hcTo.z-hcFrom.z))//2


sign = lambda x: (1, -1)[x < 0]  # useful 'sign' one liner

def get_step_to(hcFrom, hcTo):
    '''
    Returns HexCoords of hcFrom heighbour that is the closest on
    to hcTo.
    (In other words, if we want to get the shortest path from hcFrom to
    hcTo, the result of this method will be the first point of that trajectory)
    '''
    if hcFrom==hcTo:
        return hcTo
    dx = hcTo.x - hcFrom.x
    dy = hcTo.y - hcFrom.y
    dz = hcTo.z - hcFrom.z
    dr = [abs(dx), abs(dy), abs(dz)]
    drMax = max(dr) 
    if drMax==1:
        return hcTo
    if dx==0:
        return make_hex_coords(x=0, y=sign(dy), base=hcFrom)
    if dy==0:
        return make_hex_coords(y=0, x=sign(dx), base=hcFrom)
    if dz==0:
        return make_hex_coords(z=0, x=sign(dx), base=hcFrom)
    maxIndex = dr.index(drMax)
    if maxIndex==0:
        return make_hex_coords(x=sign(dx), y=-sign(dx), base=hcFrom)
    if maxIndex==1:
        return make_hex_coords(y=sign(dy), z=-sign(dy), base=hcFrom)
    return make_hex_coords(z=sign(dz), x=-sign(dz), base=hcFrom)
    

class HexafieldBase(object):
    '''
    Describes hexagonal field.
    _field is set of HexCoords 
    '''
    __slots__ = ['_field']
    
    def __init__(self, field):
        self._field = field
    
    def get_neighbours(self, hexCoords, radius = 1):
        '''
        Returns set of HexCoords of all cells close to hexCoords
        in given radius (excluding hexCoords itself)
        (Remark 'bout excessive loops - timeit measures shows quite similar results for this version and
            for r in range(radius):
                res |= self.get_at_exact_range(hexCoords, r+1)
        one.)
        '''
        res = set()
        for dx in range(-radius, radius+1):
            for dy in range (-radius, radius+1):
                if abs(dx+dy)<=radius and abs(dx)+abs(dy)>0:
                    hc = HexCoords(hexCoords.x+dx, hexCoords.y+dy)
                    if hc in self._field:
                        res.add(hc)
        return res
    
    def get_all_within(self, hexCoords, radius):
        '''
        Returns set of HexCoords of all cells within the given radius
        '''
        res = set()
        for dx in range(-radius, radius+1):
            for dy in range (-radius, radius+1):
                if abs(dx+dy)<=radius:
                    hc = HexCoords(hexCoords.x+dx, hexCoords.y+dy)
                    if hc in self._field:
                        res.add(hc)
        return res
        
    def get_at_exact_range(self, hexCoords, radius = 1):
        '''
        Returns set of HexCoords of all cells located at
        exact radius from hexCoords
        '''
        res = set()
        for y in range(radius):
            hc = make_hex_coords(x=radius, y=-y, base=hexCoords)
            if hc in self._field: res.add(hc)
            hc = make_hex_coords(x=-radius, y=y, base=hexCoords)
            if hc in self._field: res.add(hc)
        for z in range(radius): 
            hc = make_hex_coords(y=radius, z=-z, base=hexCoords)
            if hc in self._field: res.add(hc)
            hc = make_hex_coords(y=-radius, z=z, base=hexCoords)
            if hc in self._field: res.add(hc)
        for x in range(radius): 
            hc = make_hex_coords(z=radius, x=-x, base=hexCoords)
            if hc in self._field: res.add(hc)
            hc = make_hex_coords(z=-radius, x=x, base=hexCoords)
            if hc in self._field: res.add(hc)
        return res
    

class CircleHexafield(HexafieldBase):
    '''
    Describes circle-shaped hexagonal field
    '''
    __slots__ = []
    def __init__(self, fieldRadius = 2):
        field = set()
        for x in range(-fieldRadius, fieldRadius+1):
            for y in range(-fieldRadius, fieldRadius+1):
                if abs(x+y)<=fieldRadius:
                    field.add(HexCoords(x,y))
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
        x = round((left - self.leftHex0)/(1.5*self.hexRadius))
        y = round( (top-self.topHex0+x*self.hexHeight)/(-2.0*self.hexHeight) )
        return HexCoords(x,y)
    
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

    
    unittest.main()
