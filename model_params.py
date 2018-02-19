'''
Stores core model's parameters
'''

class ModelParams(object):
    '''
    Stores core model's parameters:
    (Bacteria)
    P_BACT_DIVIDE - probability that bacteria will divide on two bacteria (both in the same cell) 
    P_BACT_STAY - probability that bacteria will stand still (in case if it not divided)
    '''
    __slots__ = ['P_BACT_DIVIDE', 'P_BACT_STAY']
    
    def __init__(self, P_BACT_DIVIDE=0.01, P_BACT_STAY=0.2):
        self.P_BACT_DIVIDE = P_BACT_DIVIDE
        self.P_BACT_STAY = P_BACT_STAY

