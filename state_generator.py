'''
Generates initial state for bacterio model
'''

import random

import hexafield
from hexafield import CircleHexafield
from creatures import Predator, Bacteria
from state import BacterioState

def generate_state(fieldRadius, numBacteria, numPredators):
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
        predatorPositions[hc] = [Predator()]
        unoccupiedCells.remove(hc)
        if len(unoccupiedCells)==0:
            return BacterioState(field, bacteriaPositions, predatorPositions)
 
    return BacterioState(field, bacteriaPositions, predatorPositions)


if __name__=='__main__':
    import unittest
    
    def calculate_occupied_cells(state):
        return len(state.bacteriaPositions)+len(state.predatorPositions)
    
    def calculate_bacteria(state):
        return len(state.bacteriaPositions)
           
    def calculate_predator(state):
        return len(state.predatorPositions)


    
    class TestGenerateState(unittest.TestCase):
        
        def test_empty(self):
            state = generate_state(3,0,0)
            self.assertEqual(calculate_occupied_cells(state),0)
            self.assertEqual(calculate_bacteria(state),0)
            self.assertEqual(calculate_predator(state),0)
            
        def test_simple(self):
            state = generate_state(10,5,3)
            self.assertEqual(calculate_occupied_cells(state),8)
            self.assertEqual(calculate_bacteria(state),5)
            self.assertEqual(calculate_predator(state),3)
      
        def test_overflow(self):
            state = generate_state(1,5,3)
            self.assertEqual(calculate_occupied_cells(state),7)
            self.assertEqual(calculate_bacteria(state),5)
            self.assertEqual(calculate_predator(state),2)
        
        def test_overflow2(self):
            state = generate_state(1,15,3)
            self.assertEqual(calculate_occupied_cells(state),7)
            self.assertEqual(calculate_bacteria(state),7)
            self.assertEqual(calculate_predator(state),0)

    
    unittest.main()
