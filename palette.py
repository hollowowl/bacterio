'''
Describes bacterio's pallete
'''

from collections import namedtuple

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
