'''
Describes the state of a single cell on a field
'''

class Bacteria(object):
    '''
    Stores parameters of a single bacteria
    '''
    __slots__ = []
    
    def __init__(self):
        pass


class Predator(object):
    '''
    Stores parameters of a single predator
    '''
    __slots__ = []
    
    def __init__(self):
        pass


class CellData(object):
    '''
    Stores data of a single cell on a field
    '''
    __slots__ = ['predators', 'bacteria']
    
    def __init__(self, predators=[], bacteria=[]):
        self.predators = predators
        self.bacteria = bacteria
