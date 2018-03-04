'''
Describes a single bacterio state - field with creatures' positions
'''

import pickle
from tkinter import filedialog

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


def save_state(state, fileName):
    '''
    Pickles BacterionState using given file
    '''
    with open(fileName, 'wb') as f:
        pickle.dump(state,f)
    

def load_state(fileName):
    '''
    Unpickles BacterioState from given file.
    Returns BacterionState
    '''
    with open(fileName, 'rb') as f:
        return pickle.load(f)


def save_state_dlg(state):
    '''
    Calls 'Save File' dialog then pickles BacterioState
    '''
    fileName = filedialog.asksaveasfilename(title = "Select file",filetypes = (("Bacterio state files","*.bsf"),("all files","*.*")))
    if fileName=='':
        return
    if len(fileName.split('.'))==1:
        fileName = fileName+".bsf"
    save_state(state, fileName)
    

def load_state_dlg():
    '''
    Calls 'Open File' dialog then unpickles BacterioState.
    Returns BacterionState
    '''
    fileName = filedialog.askopenfilename(title = "Select file",filetypes = (("Bacterio state files","*.bsf"),("all files","*.*")))
    if fileName=='': 
        return None
    return load_state(fileName)


if __name__=='__main__':
    import unittest
    import os
    
    class TestStatePickling(unittest.TestCase):
        def test(self):
            state = BacterioState(CircleHexafield(3), {(1,1):1}, {(2,2):2, (3,3):3})
            tmpFile = 'tmp.bsf'
            save_state(state, tmpFile)
            state1 = load_state(tmpFile)
            self.assertEqual(state.field._field,state1.field._field)
            self.assertEqual(state.bacteriaPositions,state1.bacteriaPositions)
            self.assertEqual(state.predatorPositions,state1.predatorPositions)
            os.remove(tmpFile)
            
            
    unittest.main()
