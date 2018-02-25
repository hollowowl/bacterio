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
FIELD_RADIUS = 20  # field radius in hexagons
NUM_BACT = 30
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
        maxHexRadius = min( width/(2.0*(2.0*FIELD_RADIUS+1)), height/(2.0*hexafield.SQRT3D2*(2.0*FIELD_RADIUS+1)) )
        self.conv = hexafield.HexCoordConverter( leftHex0=width/2, topHex0=height/2, hexRadius = min(maxHexRadius, hexRadius) )
        self.canvas = Canvas(self.tk, width=width, height=height, bg=COL_BG)
        self.canvas.pack()
        self.model = model.CoreModel(model_params.default_model_params(), state_generator.generate_state(FIELD_RADIUS,NUM_BACT,NUM_PR))
        self.displayCoords = self.canvas.create_text(width-200,height-75, anchor=W, fill=COL_TEXT,font='Consolas 14 bold', text="")
        self.displayTotal = self.canvas.create_text(15,height-75, anchor=W, fill=COL_TEXT,font='Consolas 14 bold', text="")
        self.draw_field()
        self.canvas.bind("<Motion>", self.on_canvas_mouse_move)
        self.init_menu()
        self.play = False
    
    def init_menu(self):
        """
        Initialize menu and bind hotkeys
        """
        mRoot = Menu(self.tk)
        self.tk.config(menu=mRoot)
        mFile = Menu(mRoot)
        mFile.add_command(label="Open state", underline=0, command=self.open_state, accelerator="Ctrl+O")
        self.tk.bind('<Control-o>', lambda evt: self.open_state())
        mFile.add_command(label="Save state", underline=0, command=self.save_state, accelerator="Ctrl+S")
        self.tk.bind('<Control-s>', lambda evt: self.save_state())
        mFile.add_separator()
        mFile.add_command(label="Exit", underline=1, command=self.tk.destroy, accelerator="Esc")
        self.tk.bind('<Escape>', lambda evt: self.tk.destroy())
        mRoot.add_cascade(label="File", underline=0, menu=mFile)
        mProcess = Menu(mRoot)
        mProcess.add_command(label="Step/Stop play", underline=0, command=self.stop_play_or_step, accelerator="Space")
        self.tk.bind('<space>', lambda evt: self.stop_play_or_step())
        mProcess.add_command(label="Play...", underline=0, command=self.start_play, accelerator="R")
        self.tk.bind('r', lambda evt: self.start_play())
        mRoot.add_cascade(label="Process", underline=0, menu=mProcess)
    
    def draw_field(self): 
        self.canvas.delete('field')
        for hc in self.model.field._field:
            fill = None
            if hc in self.model.bacteriaPositions:
                if hc in self.model.predatorPositions:
                    fill = COL_BACT_PR
                else:
                    fill = COL_BACT
            elif hc in self.model.predatorPositions:
                fill = COL_PR 
            self.canvas.create_polygon(self.conv.get_hex_vertices(hc),
                outline=COL_BASIC, fill=fill, width=2, tag='field')
        self.currHexCoords = None
        self.canvas.itemconfigure(self.displayTotal, text="Total\nBacteria: %d\nPredators: %d" 
                % (self.model.count_bacteria(), self.model.count_predators()) )

    def on_canvas_mouse_move(self, event):
        hexCoords = self.conv.plain_to_hex(event.x,event.y)
        if hexCoords!=self.currHexCoords and hexCoords in self.model.field._field:
            numBacteria = 0
            if hexCoords in self.model.bacteriaPositions:
                numBacteria = len(self.model.bacteriaPositions[hexCoords])
            numPredators = 0
            prEnergy = ''
            if hexCoords in self.model.predatorPositions:
                numPredators = len(self.model.predatorPositions[hexCoords])
                prEnergy = str([x.energy for x in self.model.predatorPositions[hexCoords]])
            self.canvas.itemconfigure(self.displayCoords, text="x=%d, y=%d, z=%d\nBacteria: %d\nPredators: %d\n%s" 
                % (hexCoords.x, hexCoords.y, -hexCoords.x-hexCoords.y, numBacteria, numPredators, prEnergy) )
    
    def stop_play_or_step(self):
        if self.play:
            self.play = False
        else:
            self.step()
        
    def start_play(self):
        self.play = True
        self.step()
        
    def step(self):
        self.model.step()
        self.draw_field()
        if self.play:
            self.tk.after(25,self.step)
    
    def open_state(self):
        pass
        
    def save_state(self):
        pass
       
if __name__=='__main__':
    root = Tk()
    root.title('Bacterio')
    main = MainWindow(root)
    root.mainloop()

