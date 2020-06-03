'''
Generates initial state for bacterio model
'''

import random

from app.hexafield import CircleHexafield
from app.creatures import Predator, Bacteria
from app.state import BacterioState
from app.model_params import default_model_params

def generate_state(fieldRadius, numBacteria, numPredators, modelParams = default_model_params()):
    '''
    Generates initial state on CircleHexafield with given fieldRadius.
    Each object placed on different cell. If there are more objects (numBacteria+numPredators) than
    cells, function fills the entire field than returns.
    Returns state.BacterioState
    '''
    field = CircleHexafield(fieldRadius)
    bacteriaPositions = dict()
    predatorPositions = dict()
    unoccupiedCells = [ x for x in field._field ]
    for i in range(numBacteria):
        hc = random.choice(unoccupiedCells)
        bacteriaPositions[hc] = [Bacteria()]
        unoccupiedCells.remove(hc)
        if len(unoccupiedCells)==0:
            return BacterioState(field, bacteriaPositions, predatorPositions)
        
    for i in range(numPredators):
        hc = random.choice(unoccupiedCells)
        predatorPositions[hc] = [Predator(modelParams.PR_INIT_ENERGY)]
        unoccupiedCells.remove(hc)
        if len(unoccupiedCells)==0:
            return BacterioState(field, bacteriaPositions, predatorPositions)
 
    return BacterioState(field, bacteriaPositions, predatorPositions)
