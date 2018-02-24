'''
Describes core model of bacterio 
'''

import random

from hexafield import HexCoords
from creatures import Predator, Bacteria
from rand_p import rand_p


class CoreModel(object):
    '''
    Describes core (the simpliest one) model of bacterio.
    'field' is HexafieldBase instance,
    'modelParams' is ModelParams instance,
    'bacteriaPositions' and 'predatorPositions' are dicts with keys HexCoords and values lists of Bacteria and Predator
    '''
    __slots__ = ['modelParams', 'field', 'bacteriaPositions', 'predatorPositions']
    
    def __init__(self, modelParams, state):
        '''
        modelParams is ModelParams,
        state is state.BacretioState that will be parsed as initial state
        '''
        self.modelParams = modelParams
        self.parse_state(state)
        
    def parse_state(self, state):
        '''
        state is state.BacretioState
        '''
        self.field = state.field
        self.bacteriaPositions = state.bacteriaPositions
        self.predatorPositions = state.predatorPositions
    
    def step(self):
        '''
        Makes one turn and updates 'bacteriaPositions' and 'predatorPositions'
        '''
        newBacteriaPositions = dict()
        for hc in self.bacteriaPositions:
            for bact in self.bacteriaPositions[hc]:
                if rand_p(self.modelParams.P_BACT_DIVIDE)==1:
                    if not hc in newBacteriaPositions:
                        newBacteriaPositions[hc] = []
                    newBacteriaPositions[hc].append(Bacteria())
                    newBacteriaPositions[hc].append(Bacteria())
                elif rand_p(self.modelParams.P_BACT_STAY)==1:
                    if not hc in newBacteriaPositions:
                        newBacteriaPositions[hc] = []
                    newBacteriaPositions[hc].append(bact)
                else:
                    newPos = random.choice(list(self.field.get_neighbours(hc)))
                    if not newPos in newBacteriaPositions:
                        newBacteriaPositions[newPos] = []
                    newBacteriaPositions[newPos].append(bact)
        self.bacteriaPositions = newBacteriaPositions
        
    def count_bacteria(self):
        '''
        Returns total amount of bacteria
        '''
        res = 0
        for hc in self.bacteriaPositions:
            res += len(self.bacteriaPositions[hc])
        return res
    
    def count_predators(self):
        '''
        Returns total amount of predators
        '''
        res = 0
        for hc in self.predatorPositions:
            res += len(self.predatorPositions[hc])
        return res
    
    
                
            
