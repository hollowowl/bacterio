'''
Describes a single bacterio state - field with creatures' positions
'''

from hexafield import CircleHexafield

class BacterioState(object):
    '''
    Describes a single bacterio state - field with creatures' positions
    'field' is HexafieldBase instance
    'bacteriaPositions' and 'predatorPositions' are dicts with keys HexCoords and values lists of Bacteria and Predator
    '''
    __slots__= ('field', 'bacteriaPositions', 'predatorPositions')
    
    def __init__(self, field=CircleHexafield(), bacteriaPositions=dict(), predatorPositions=dict()):
        self.field = field
        self.bacteriaPositions = bacteriaPositions
        self.predatorPositions = predatorPositions


