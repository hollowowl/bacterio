'''
Describes the state of a single cell on a field
'''

class Bacteria(object):
    '''
    Stores parameters of a single bacteria
    '''
    __slots__ = ()
    
    def __init__(self):
        pass


class Predator(object):
    '''
    Stores parameters of a single predator.
    Predator loses energy each turn. When energy if <=0, predator dies.
    '''
    __slots__ = ('energy')
    
    def __init__(self, energy):
        self.energy = energy
