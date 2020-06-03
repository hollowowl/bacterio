import unittest
import os

from app.state_generator import generate_state
from app.state import BacterioState, save_state, load_state
from app.hexafield import CircleHexafield

def calculate_occupied_cells(state):
    return len(state.bacteriaPositions)+len(state.predatorPositions)

def calculate_bacteria(state):
    return len(state.bacteriaPositions)
       
def calculate_predator(state):
    return len(state.predatorPositions)


BACTERIO_OPTIONAL_TESTS = int(os.getenv('BACTERIO_OPTIONAL_TESTS', '0'))


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


@unittest.skipUnless(BACTERIO_OPTIONAL_TESTS, "Not designed to be a regular test - creates tmp file")
class TestStatePickling(unittest.TestCase):
    def test(self):
        state = BacterioState(CircleHexafield(3), {(1,1):1}, {(2,2):2, (3,3):3})
        tmpFile = 'saved_states/test_state_pickling.bsf'
        save_state(state, tmpFile)
        state1 = load_state(tmpFile)
        self.assertEqual(state.field._field,state1.field._field)
        self.assertEqual(state.bacteriaPositions,state1.bacteriaPositions)
        self.assertEqual(state.predatorPositions,state1.predatorPositions)
        os.remove(tmpFile)
