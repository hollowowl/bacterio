'''
Stores core model's parameters:
(Bacteria)
P_BACT_DIVIDE - probability that bacteria will divide on two bacteria (both in the same cell) unless there are >= BACT_OVERCROWD bacteria in given cell
P_BACT_STAY - probability that bacteria will stand still (in case if it not divided)
BACT_OVERCROWD - number of maximum number of bacteria within BACT_OVERCROWD_RADIUS (if more or equal, bacteria will not divide)
BACT_OVERCROWD_RADIUS - ...
(Predator)
PR_INIT_ENERGY - initial predator's energy
PR_MAX_ENERGY - value of energy when predator stops hunting (until loose energy below this value)
PR_DIVIDE_ENERGY - minimal energy value at which predator's divide is possible. Offsprings will have (E-PR_DIVIDE_COST)//2 energy
PR_DIVIDE_COST - energy cost of predator's division
PR_TURN_COST - energy cost of each predator's turn (except division or feed)
PR_FEED_VALUE - energy gained by predator after successful hunting
PR_SIGHT - predator's sight range
P_PR_DIVIDE - probability of predator's division (if its energy>=PR_DIVIDE_ENERGY)
P_PR_STAY - probability that predator remain still if he is fed up (energy>=PR_MAX_ENERGY)
PR_OVERCROWD - number of maximum number of predators within PR_OVERCROWD_RADIUS (if more or equal, predator will not divide)
PR_OVERCROWD_RADIUS - ...
'''

from collections import namedtuple

from decimal import Decimal

ModelParams = namedtuple('ModelParams', ['P_BACT_DIVIDE', 
                                        'P_BACT_STAY',
                                        'BACT_OVERCROWD',
                                        'BACT_OVERCROWD_RADIUS',
                                        'BACT_VELOCITY',
                                        'PR_INIT_ENERGY',
                                        'PR_MAX_ENERGY',
                                        'PR_DIVIDE_ENERGY',
                                        'PR_DIVIDE_COST',
                                        'PR_TURN_COST',
                                        'PR_FEED_VALUE',
                                        'PR_SIGHT',
                                        'P_PR_DIVIDE',
                                        'P_PR_STAY',
                                        'PR_OVERCROWD',
                                        'PR_OVERCROWD_RADIUS'])


def default_model_params():
    return ModelParams(
            P_BACT_DIVIDE=Decimal('0.1'), 
            P_BACT_STAY=Decimal('0.05'),
            BACT_OVERCROWD=2,
            BACT_OVERCROWD_RADIUS=1,
            BACT_VELOCITY = 1,
            PR_INIT_ENERGY=10,
            PR_MAX_ENERGY=15,
            PR_DIVIDE_ENERGY=12,
            PR_DIVIDE_COST=0,
            PR_TURN_COST=1,
            PR_FEED_VALUE=5,
            PR_SIGHT=4,
            P_PR_DIVIDE=Decimal('0.5'),
            P_PR_STAY=Decimal('0.8'),
            PR_OVERCROWD=2,
            PR_OVERCROWD_RADIUS=6)


def load_model_params(configSection):
    '''
    Loads modelParams from given section of INI file (parsed with configparser.ConfigParser)
    '''
    return ModelParams(
            P_BACT_DIVIDE=Decimal(configSection['P_BACT_DIVIDE']), 
            P_BACT_STAY=Decimal(configSection['P_BACT_DIVIDE']),
            BACT_OVERCROWD=configSection.getint('BACT_OVERCROWD'),
            BACT_OVERCROWD_RADIUS=configSection.getint('BACT_OVERCROWD_RADIUS'),
            BACT_VELOCITY=configSection.getint('BACT_VELOCITY'),
            PR_INIT_ENERGY=configSection.getint('PR_INIT_ENERGY'),
            PR_MAX_ENERGY=configSection.getint('PR_MAX_ENERGY'),
            PR_DIVIDE_ENERGY=configSection.getint('PR_DIVIDE_ENERGY'),
            PR_DIVIDE_COST=configSection.getint('PR_DIVIDE_COST'),
            PR_TURN_COST=configSection.getint('PR_TURN_COST'),
            PR_FEED_VALUE=configSection.getint('PR_FEED_VALUE'),
            PR_SIGHT=configSection.getint('PR_SIGHT'),
            P_PR_DIVIDE=Decimal(configSection['P_PR_DIVIDE']),
            P_PR_STAY=Decimal(configSection['P_PR_STAY']),
            PR_OVERCROWD=configSection.getint('PR_OVERCROWD'),
            PR_OVERCROWD_RADIUS=configSection.getint('PR_OVERCROWD_RADIUS'))
    
