'''
Main GUI window of bacterio
'''

from tkinter import *

import hexafield
from hexafield import HexCoords
import model
import model_params
import state_generator


COL_BG = 'black'
COL_TEXT = 'green'
COL_BASIC = 'green' # for all hexagons except those in sight range 2
COL_BACT = 'dim gray'
COL_PR = 'red'
COL_BACT_PR = 'brown'
FIELD_RADIUS = 10  # field radius in hexagons
NUM_BACT = 15
NUM_PR = 7


class MainWindow(object):
    """
    Represents main application window
    """
    def __init__(self, tk, width=1024, height=768, hexRadius=30):
        '''
        tk is is Tk object to use for main app window
        width and height are properties of canvas where field will be placed
        hexRadius is (suprisingly) radius of single hexagon
        '''
        self.tk = tk
        self.tk.bind('<Escape>', lambda evt: self.tk.destroy())
        maxHexRadius = min( width/(2.0*(2.0*FIELD_RADIUS+1)), height/(2.0*hexafield.SQRT3D2*(2.0*FIELD_RADIUS+1)) )
        self.conv = hexafield.HexCoordConverter( leftHex0=width/2, topHex0=height/2, hexRadius = min(maxHexRadius, hexRadius) )
        self.canvas = Canvas(self.tk, width=width, height=height, bg=COL_BG)
        self.canvas.pack()
        self.model = model.CoreModel(model_params.ModelParams, state_generator.generate_state(FIELD_RADIUS,NUM_BACT,NUM_PR))
        self.draw_field()
        self.displayCoords = self.canvas.create_text(width-150,height-75, fill=COL_TEXT,font='Consolas 14 bold', text="")
        self.canvas.bind("<Motion>", self.on_canvas_mouse_move)
        
    def draw_field(self): 
        self.canvas.delete('field')
        for hc in self.model.currentState.field:
            fill = None
            cellData = self.model.currentState.field[hc]
            if cellData is not None:
                if len(cellData.predators)>0 and len(cellData.bacteria)>0:
                    fill = COL_BACT_PR
                elif len(cellData.predators)>0:
                    fill = COL_PR
                elif len(cellData.bacteria)>0:
                    fill = COL_BACT
            self.canvas.create_polygon(self.conv.get_hex_vertices(hc),
                outline=COL_BASIC, fill=fill, width=2, tag='field')
        self.currHexCoords = None


    def on_canvas_mouse_move(self, event):
        hexCoords = self.conv.plain_to_hex(event.x,event.y)
        if hexCoords!=self.currHexCoords and hexCoords in self.model.currentState.field:
            cellData = self.model.currentState.field[hexCoords]
            self.canvas.itemconfigure(self.displayCoords, text="x=%d, y=%d, z=%d\nBacteria: %d\nPredators: %d" 
                % (hexCoords.x, hexCoords.y, -hexCoords.x-hexCoords.y, len(cellData.bacteria), len(cellData.predators)) )

        
       
if __name__=='__main__':
    root = Tk()
    root.title('Bacterio')
    main = MainWindow(root)
    root.mainloop()

