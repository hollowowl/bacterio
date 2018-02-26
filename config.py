'''
Describes bacterio's configuration - board, model and other parameters
'''

from collections import namedtuple
import configparser

import model_params

Config = namedtuple('Config', ['fieldParams', 'modelParams', 'miscParams'])
FieldParams = namedtuple('FieldParams', ['radius', 'initBacteria', 'initPredators'])
MiscParams = namedtuple('MiscParams', ['height', 'width'])
