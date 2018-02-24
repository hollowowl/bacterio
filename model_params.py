'''
Stores core model's parameters:
(Bacteria)
P_BACT_DIVIDE - probability that bacteria will divide on two bacteria (both in the same cell) unless there are >= BACT_OVERCROWD bacteria in given cell
P_BACT_STAY - probability that bacteria will stand still (in case if it not divided)
BACT_OVERCROWD - number of maximum number of bacteria within one cell (if more or equal, bacteria will not divide)
(Predator)
PR_INIT_ENERGY - initial predator's energy
PR_MAX_ENERGY - value of energy when predator stops hunting (until loose energy below this value)
PR_DIVIDE_ENERGY - minimal energy value at which predator's divide is possible. Offsprings will have (E-PR_DIVIDE_COST)//2 energy
PR_DIVIDE_COST - energy cost of predator's division
PR_TURN_COST - energy cost of each predator's turn (except division or feed)
PR_FEED_VALUE - energy gained by predator after successful hunting
PR_SIGHT = predator's sight range
P_PR_DIVIDE - probability of predator's division (if its energy>=PR_DIVIDE_ENERGY)
P_PR_STAY - probability that predator remain still if he is fed up (energy>=PR_MAX_ENERGY)
PR_OVERCROWD - number of maximum number of predators within one cell (if more or equal, predator will not divide)
'''

from collections import namedtuple

from decimal import Decimal

ModelParams = namedtuple('ModelParams', ['P_BACT_DIVIDE', 
                                        'P_BACT_STAY',
                                        'BACT_OVERCROWD',
                                        'PR_INIT_ENERGY',
                                        'PR_MAX_ENERGY',
                                        'PR_DIVIDE_ENERGY',
                                        'PR_DIVIDE_COST',
                                        'PR_TURN_COST',
                                        'PR_FEED_VALUE',
                                        'PR_SIGHT',
                                        'P_PR_DIVIDE',
                                        'P_PR_STAY',
                                        'PR_OVERCROWD'])


def default_model_params():
    return ModelParams(
            P_BACT_DIVIDE=Decimal('0.1'), 
            P_BACT_STAY=Decimal('0.2'),
            BACT_OVERCROWD=2,
            PR_INIT_ENERGY=20,
            PR_MAX_ENERGY=30,
            PR_DIVIDE_ENERGY=25,
            PR_DIVIDE_COST=0,
            PR_TURN_COST=1,
            PR_FEED_VALUE=10,
            PR_SIGHT=2,
            P_PR_DIVIDE=Decimal('0.05'),
            P_PR_STAY=Decimal('0.8'),
            PR_OVERCROWD=2)
            
