'''
Describes bacterio's pallete
'''

from collections import namedtuple
import configparser

Palette = namedtuple('Palette', ['background',
                                'text',
                                'grid',
                                'bacteria',
                                'predator',
                                'both'])


def default_palette():
    return Palette(
        background = 'black',
        text = 'green',
        grid = 'green',
        bacteria = 'dim gray',
        predator = 'red',
        both = 'brown')


def load_palette(fileName):
    '''
    Tries to load palette from given .INI file.
    If fails, return default_config()
    '''
    config = configparser.ConfigParser()
    config.read(fileName)
    if config.sections() == []:
        return default_palette()
    sectionColors = config['COLORS']
    return Palette(
        background = sectionColors['background'],
        text = sectionColors['text'],
        grid = sectionColors['grid'],
        bacteria = sectionColors['bacteria'],
        predator = sectionColors['predator'],
        both = sectionColors['both'])
