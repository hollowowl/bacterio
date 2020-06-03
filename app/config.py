'''
Describes bacterio's configuration - board, model and other parameters
'''

from collections import namedtuple
import configparser

import app.model_params as model_params

Rules = namedtuple('Rules', ['fieldParams', 'modelParams'])
FieldParams = namedtuple('FieldParams', ['stateFile', 'radius', 'initBacteria', 'initPredators'])
MiscParams = namedtuple('MiscParams', ['height', 'width', 'writeTrace', 'traceFilePrefix', 'stepDelay'])

def default_field_params():
    return FieldParams(
            stateFile = None,
            radius = 15,
            initBacteria = 200,
            initPredators = 20)
    
            
def default_misc_params():
    return MiscParams(
            height = 768,
            width = 1024,
            writeTrace = False,
            traceFilePrefix = None,
            stepDelay = 25)


def default_rules():
    return Rules(
            fieldParams = default_field_params(),
            modelParams = model_params.default_model_params())


def load_rules(fileName):
    '''
    Tries to load config from given .INI file.
    If failes returns default_config()
    '''
    config = configparser.ConfigParser()
    config.read(fileName)
    if config.sections() == []:
        return default_rules()
    sectionField = config['FIELD']
    sectionModel = config['MODEL']
    return Rules(
        fieldParams = FieldParams (
                    stateFile = sectionField.get('stateFile', fallback=None),
                    radius = sectionField.getint('radius', fallback=2),
                    initBacteria = sectionField.getint('initBacteria', fallback=0),
                    initPredators = sectionField.getint('initPredators', fallback=0)),
        modelParams = model_params.load_model_params(sectionModel))


def load_misc_params(fileName):
    '''
    Tries to load miscellaneous application parameters from given .INI file.
    If failes returns default_config()
    '''
    config = configparser.ConfigParser()
    config.read(fileName)
    if config.sections() == []:
        return default_misc_params()
    sectionMisc = config['MISC']
    return MiscParams(
        height = sectionMisc.getint('height'),
        width = sectionMisc.getint('width'),
        writeTrace = sectionMisc.getboolean('writeTrace'),
        traceFilePrefix = sectionMisc['traceFilePrefix'],
        stepDelay = sectionMisc.getint('stepDelay'))
