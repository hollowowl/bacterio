'''
Describes bacterio's configuration - board, model and other parameters
'''

from collections import namedtuple
import configparser

import model_params

Config = namedtuple('Config', ['fieldParams', 'modelParams', 'miscParams'])
FieldParams = namedtuple('FieldParams', ['radius', 'initBacteria', 'initPredators'])
MiscParams = namedtuple('MiscParams', ['height', 'width', 'writeTrace', 'traceFilePrefix'])

def default_field_params():
    return FieldParams(
            radius = 6,
            initBacteria = 100,
            initPredators = 40)
    
            
def default_misc_params():
    return MiscParams(
            height = 768,
            width = 1024,
            writeTrace = False,
            traceFilePrefix = None)


def default_config():
    return Config(
            fieldParams = default_field_params(),
            modelParams = model_params.default_model_params(),
            miscParams = default_misc_params())


def load_config(fileName):
    '''
    Tries to load config from given .INI file.
    If failes returns default_config()
    '''
    config = configparser.ConfigParser()
    config.read(fileName)
    if config.sections() == []:
        return default_config()
    sectionField = config['FIELD']
    sectionModel = config['MODEL']
    sectionMisc = config['MISC']
    return Config(
        fieldParams = FieldParams (
                    radius = sectionField.getint('radius'),
                    initBacteria = sectionField.getint('initBacteria'),
                    initPredators = sectionField.getint('initPredators')),
        modelParams = model_params.load_model_params(sectionModel),
        miscParams = MiscParams(
                    height = sectionMisc.getint('height'),
                    width = sectionMisc.getint('width'),
                    writeTrace = sectionMisc.getboolean('writeTrace'),
                    traceFilePrefix = sectionMisc['traceFilePrefix']))
