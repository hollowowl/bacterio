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


sign = lambda x: (1, -1)[x < 0]

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
        Returns list of HexCoords of all cells close to hexCoords
        in given radius (excluding hexCoords itself)
        '''
        res = []
        for dx in range(-radius, radius+1):
            for dy in range(max(-radius,-dx-radius), min(radius,radius-dx)+1):
                if dx!=0 or dy!=0:
                    hc = HexCoords(hexCoords.x+dx, hexCoords.y+dy)
                    if hc in self._field:
                        res.append(hc)
        return res
    
    def get_all_within(self, hexCoords, radius):
        '''
        Returns list of HexCoords of all cells within the given radius
        '''
        res = []
        for dx in range(-radius, radius+1):
            for dy in range(max(-radius,-dx-radius), min(radius,radius-dx)+1):
                hc = HexCoords(hexCoords.x+dx, hexCoords.y+dy)
                if hc in self._field:
                    res.append(hc)
        return res
        
    def get_at_exact_range(self, hexCoords, radius = 1):
        '''
        Returns list of HexCoords of all cells located at
        exact radius from hexCoords
        '''
        res = []
        for y in range(radius):
            hc = make_hex_coords(x=radius, y=-y, base=hexCoords)
            if hc in self._field: res.append(hc)
            hc = make_hex_coords(x=-radius, y=y, base=hexCoords)
            if hc in self._field: res.append(hc)
        for z in range(radius): 
            hc = make_hex_coords(y=radius, z=-z, base=hexCoords)
            if hc in self._field: res.append(hc)
            hc = make_hex_coords(y=-radius, z=z, base=hexCoords)
            if hc in self._field: res.append(hc)
        for x in range(radius): 
            hc = make_hex_coords(z=radius, x=-x, base=hexCoords)
            if hc in self._field: res.append(hc)
            hc = make_hex_coords(z=-radius, x=x, base=hexCoords)
            if hc in self._field: res.append(hc)
        return res
    
    def get_max_coord_value(self):
        '''
        Returns the maximum absolute coordinate value over all cells
        '''
        result = 0
        for cell in self._field:
            if abs(cell.x) > result:
                result = abs(cell.x)
            if abs(cell.y) > result:
                resutl = abs(cell.y)
            if abs(cell.z) > result:
                result = cell.z
        return result


class CircleHexafield(HexafieldBase):
    '''
    Describes circle-shaped hexagonal field
    '''
    __slots__ = []
    def __init__(self, fieldRadius = 2):
        field = set()
        for x in range(-fieldRadius, fieldRadius+1):
            for y in range(max(-fieldRadius,-x-fieldRadius), min(fieldRadius,fieldRadius-x)+1):
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
