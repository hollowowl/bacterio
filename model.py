'''
Describes core model of bacterio 
'''

import random

import hexafield
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
    __slots__ = ('modelParams', 'field', 'bacteriaPositions', 'predatorPositions')
    
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
        self.step_predators()
        self.step_bacteria()
    
    def step_predators(self):
        newPredatorPositions = dict()
        for hc in self.predatorPositions:
            notOvercrowded = self.check_predators_overcrowd(hc)
            for pr in self.predatorPositions[hc]:
                if notOvercrowded and pr.energy>=self.modelParams.PR_DIVIDE_ENERGY and rand_p(self.modelParams.P_PR_DIVIDE)==1:
                    # DIVIDE
                    if not hc in newPredatorPositions:
                        newPredatorPositions[hc] = []
                    offspringEnergy = (pr.energy-self.modelParams.PR_DIVIDE_COST)//2
                    newPredatorPositions[hc].append(Predator(offspringEnergy))
                    newPredatorPositions[hc].append(Predator(offspringEnergy))
                elif pr.energy>=self.modelParams.PR_MAX_ENERGY:
                    # WELL FED
                    if rand_p(self.modelParams.P_PR_STAY)==1:
                        if not hc in newPredatorPositions:
                            newPredatorPositions[hc] = []
                        newPredatorPositions[hc].append(pr)
                    else:
                        newPos = random.choice(self.field.get_neighbours(hc))
                        if not newPos in newPredatorPositions:
                            newPredatorPositions[newPos] = []
                        newPredatorPositions[newPos].append(pr)
                    pr.energy-=self.modelParams.PR_TURN_COST
                else:
                    # HUNGRY
                    pr.energy-=self.modelParams.PR_TURN_COST
                    if pr.energy>0:
                        closestBact = self.find_closest_bacteria(hc)
                        if closestBact is not None:
                            newPos = hexafield.get_step_to(hc, closestBact)
                            if not newPos in newPredatorPositions:
                                newPredatorPositions[newPos] = []
                            newPredatorPositions[newPos].append(pr)
                            if newPos in self.bacteriaPositions:
                                self.bacteriaPositions[newPos].pop()
                                if len(self.bacteriaPositions[newPos])==0:
                                    self.bacteriaPositions.pop(newPos)
                                pr.energy+=self.modelParams.PR_FEED_VALUE
                        else: #if closestBact is None
                            newPos = random.choice(self.field.get_neighbours(hc))
                            if not newPos in newPredatorPositions:
                                newPredatorPositions[newPos] = []
                            newPredatorPositions[newPos].append(pr)
        self.predatorPositions = newPredatorPositions

    def step_bacteria(self):
        newBacteriaPositions = dict()
        for hc in self.bacteriaPositions:
            notOvercrowded = self.check_bacteria_overcrowd(hc)
            for bact in self.bacteriaPositions[hc]:
                if notOvercrowded and rand_p(self.modelParams.P_BACT_DIVIDE)==1:
                    if not hc in newBacteriaPositions:
                        newBacteriaPositions[hc] = []
                    newBacteriaPositions[hc].append(Bacteria())
                    newBacteriaPositions[hc].append(Bacteria())
                elif rand_p(self.modelParams.P_BACT_STAY)==1:
                    if not hc in newBacteriaPositions:
                        newBacteriaPositions[hc] = []
                    newBacteriaPositions[hc].append(bact)
                else:
                    newPos = random.choice(self.field.get_neighbours(hc))
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
    
    
    def check_bacteria_overcrowd(self, hexCoords):
        '''
        Checks if number of bacteria near hexCoords in radius BACT_OVERCROWD_RADIUS less than BACT_OVERCROWD
        '''
        if self.modelParams.BACT_OVERCROWD<=0:
            return True
        res = 0
        coords = self.field.get_all_within(hexCoords, self.modelParams.BACT_OVERCROWD_RADIUS)
        for hc in coords:
            if hc in self.bacteriaPositions:
                res+=len(self.bacteriaPositions[hc])
        return res<self.modelParams.BACT_OVERCROWD
    
    def check_predators_overcrowd(self, hexCoords):
        '''
        Checks if number of bacteria near hexCoords in radius PR_OVERCROWD_RADIUS less than PR_OVERCROWD
        '''
        if self.modelParams.PR_OVERCROWD<=0:
            return True
        res = 0
        coords = self.field.get_all_within(hexCoords, self.modelParams.PR_OVERCROWD_RADIUS)
        for hc in coords:
            if hc in self.predatorPositions:
                res+=len(self.predatorPositions[hc])
        return res<self.modelParams.PR_OVERCROWD
    
    def find_closest_bacteria(self, hexCoords):
        '''
        Returns position of the closest bacteria within maxRange (or None)
        '''
        if hexCoords in self.bacteriaPositions:
            return hexCoords
        for r in range(1, self.modelParams.PR_SIGHT+1):
            cells = self.field.get_at_exact_range(hexCoords, r)
            possiblePos = []
            for hc in cells:
                if hc in self.bacteriaPositions:
                    possiblePos.append(hc)
            if len(possiblePos)>0:
                return random.choice(possiblePos)
        return None
    
    def add_bacteria(self, hexCoords):
        '''
        Adds bacteria to given cell
        '''
        if not hexCoords in self.bacteriaPositions:
            self.bacteriaPositions[hexCoords] = []
        self.bacteriaPositions[hexCoords].append(Bacteria())
    
    def add_predator(self, hexCoords):
        '''
        Adds predator to given cell
        '''
        if not hexCoords in self.predatorPositions:
            self.predatorPositions[hexCoords] = []
        self.predatorPositions[hexCoords].append(Predator(self.modelParams.PR_INIT_ENERGY))
        
    def clear_cell(self, hexCoords):
        '''
        Removes all creatures from given cell
        '''
        if hexCoords in self.bacteriaPositions:
            self.bacteriaPositions.pop(hexCoords)
        if hexCoords in self.predatorPositions:
            self.predatorPositions.pop(hexCoords)


class RapidBacteriaModel(CoreModel):
    '''
    Describes model with rapid moving bacteria. Each turn they divide or move for two cells
    '''
    __slots__ = ()
    
    def __init__(self, modelParams, state):
        CoreModel.__init__(self, modelParams, state)
    
    def step_bacteria(self):
        newBacteriaPositions = dict()
        for hc in self.bacteriaPositions:
            notOvercrowded = self.check_bacteria_overcrowd(hc)
            for bact in self.bacteriaPositions[hc]:
                if notOvercrowded and rand_p(self.modelParams.P_BACT_DIVIDE)==1:
                    if not hc in newBacteriaPositions:
                        newBacteriaPositions[hc] = []
                    newBacteriaPositions[hc].append(Bacteria())
                    newBacteriaPositions[hc].append(Bacteria())
                elif rand_p(self.modelParams.P_BACT_STAY)==1:
                    if not hc in newBacteriaPositions:
                        newBacteriaPositions[hc] = []
                    newBacteriaPositions[hc].append(bact)
                else:
                    newPos = random.choice(self.field.get_at_exact_range(hc,self.modelParams.BACT_VELOCITY))
                    if not newPos in newBacteriaPositions:
                        newBacteriaPositions[newPos] = []
                    newBacteriaPositions[newPos].append(bact)
        self.bacteriaPositions = newBacteriaPositions
    
