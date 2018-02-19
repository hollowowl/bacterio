'''
Describes core model of bacterio 
'''

from hexafield import HexCoords 
from cell_data import CellData, Predator, Bacteria

class CoreModel(object):
    '''
    Describes core (the simpliest one) model of bacterio
    '''
    
    def __init__(self, modelParams, initialState):
        '''
        modelParams is ModelParams, 
        initialState is HexafieldBase with placed bacteria and predators
        (each value in HexafieldBase.field should be CellData or None)
        '''
        self.modelParams = modelParams
        self.parse_initial_state(initialState)
    
    
    def parse_initial_state(self, initialState):
        '''
        Parses initialState (HexafieldBase with placed bacteria and predators)
        and forms 'bacteriaPositions' and 'predatorPositions' sets along with 'currentState'
        '''
        self.bacteriaPositions = set()
        self.predatorPositions = set()
        self.currentState = initialState
        for hc in initialState.field:
            cellData = initialState.field[hc]
            if isinstance(cellData, CellData):
                if len(cellData.bacteria)>0:
                    self.bacteriaPositions.add(hc)
                if len(cellData.predators)>0:
                    self.predatorPositions.add(hc)
            else:
                self.currentState.field[hc] = CellData()
            
