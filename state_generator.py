'''
Generates initial state for bacterio model
'''

import random

import hexafield
from hexafield import CircleHexafield
from cell_data import CellData, Predator, Bacteria

def generate_state(fieldRadius, numBacteria, numPredators):
    '''
    Generates initial state on CircleHexafield with given fieldRadius.
    Each object placed on different cell. If there are more objects (numBacteria+numPredators) than
    cells, function fills the entire field than returns.
    Returns CircleHexafield with CellData as field's values
    '''
    state = CircleHexafield(fieldRadius)
    unoccupiedCells = [ x for x in state.field.keys() ]
    for i in range(numBacteria):
        cellData = CellData(bacteria = [Bacteria()])
        hc = random.choice(unoccupiedCells)
        state.field[hc] = cellData
        unoccupiedCells.remove(hc)
        if len(unoccupiedCells)==0:
            return state
        
    for i in range(numPredators):
        cellData = CellData(predators = [Predator()])
        hc = random.choice(unoccupiedCells)
        state.field[hc] = cellData
        unoccupiedCells.remove(hc)
        if len(unoccupiedCells)==0:
            return state
 
    return state


if __name__=='__main__':
    import unittest
    
    def calculate_occupied_cells(state):
        res = 0
        for hc in state.field:
            if isinstance(state.field[hc], CellData):
                res+=1
        return res
    
    def calculate_bacteria(state):
        res = 0
        for hc in state.field:
            if isinstance(state.field[hc], CellData):
                res+=len(state.field[hc].bacteria)
        return res
           
    def calculate_predator(state):
        res = 0
        for hc in state.field:
            if isinstance(state.field[hc], CellData):
                res+=len(state.field[hc].predators)
        return res

    
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
