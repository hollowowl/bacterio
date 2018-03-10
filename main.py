'''
Main GUI window of bacterio
'''

from tkinter import *

import hexafield
from hexafield import HexCoords
import model
import model_params
import state_generator
import state
import palette
import config
from tracewriter import TraceWriter


DEFAULT_PALETTE_FILE = 'palette.ini'
DEFAULT_CONFIG_FILE = 'config.ini'

class MainWindow(object):
    """
    Represents main application window
    """
    def __init__(self, tk):
        '''
        tk is is Tk object to use for main app window
        '''
        self.tk = tk
        conf = config.load_config(DEFAULT_CONFIG_FILE)
        maxHexRadius = min( conf.miscParams.width/(2.0*(2.0*conf.fieldParams.radius+1)), conf.miscParams.height/(2.0*hexafield.SQRT3D2*(2.0*conf.fieldParams.radius+1)) )
        self.conv = hexafield.HexCoordConverter( leftHex0=conf.miscParams.width/2, topHex0=conf.miscParams.height/2, hexRadius = maxHexRadius )
        self.palette = palette.load_palette(DEFAULT_PALETTE_FILE)
        self.canvas = Canvas(self.tk, width=conf.miscParams.width, height=conf.miscParams.height, bg=self.palette.background)
        self.canvas.pack()
        self.model = model.RapidBacteriaModel(conf.modelParams, state_generator.generate_state(conf.fieldParams.radius,conf.fieldParams.initBacteria,conf.fieldParams.initPredators,conf.modelParams))
        self.displayCoords = self.canvas.create_text(conf.miscParams.width-200,conf.miscParams.height-75, anchor=W, fill=self.palette.text,font='Consolas 14 bold', text="")
        self.displayTotal = self.canvas.create_text(15,conf.miscParams.height-75, anchor=W, fill=self.palette.text,font='Consolas 14 bold', text="")
        self.init_board_state()
        self.canvas.bind("<Motion>", self.on_canvas_mouse_move)
        self.init_menu()
        if conf.miscParams.writeTrace:
            self.traceWriter = TraceWriter(conf)
            self.traceWriter.write(self.currentStep, self.numBacteria, self.numPredators)
        else:
            self.traceWriter = None
        self.stepDelay = conf.miscParams.stepDelay
    
    def init_board_state(self):
        self.currentStep = 0
        self.haltReason = ''
        self.numBacteria = self.model.count_bacteria()
        self.numPredators = self.model.count_predators()
        self.draw_field()
        self.currHexCoords = None
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
        mBoard = Menu(mRoot)
        mBoard.add_command(label="Clear", underline=0, command=self.clear_board, accelerator="Ctrl+C")
        self.tk.bind('<Control-c>', lambda evt: self.clear_board())
        mRoot.add_cascade(label="Board", underline=0, menu=mBoard)
        self.tk.bind('z', lambda evt: self.add_bacteria())
        self.tk.bind('<Button-1>', lambda evt: self.add_bacteria())
        self.tk.bind('x', lambda evt: self.add_predator())
        self.tk.bind('<Button-3>', lambda evt: self.add_predator())
        self.tk.bind('c', lambda evt: self.clear_cell())
        self.tk.bind('<Button-2>', lambda evt: self.clear_cell())
        
    
    def draw_field(self): 
        self.canvas.delete('field')
        for hc in self.model.field._field:
            fill = ''
            if hc in self.model.bacteriaPositions:
                if hc in self.model.predatorPositions:
                    fill = self.palette.both
                else:
                    fill = self.palette.bacteria
            elif hc in self.model.predatorPositions:
                fill = self.palette.predator
            self.canvas.create_polygon(self.conv.get_hex_vertices(hc),
                outline=self.palette.grid, fill=fill, width=2, tag='field')
        self.canvas.itemconfigure(self.displayTotal, text="Step %d\nBacteria: %d\nPredators: %d\n%s" 
                % (self.currentStep, self.numBacteria, self.numPredators, self.haltReason) )

    def on_canvas_mouse_move(self, event):
        hexCoords = self.conv.plain_to_hex(event.x,event.y)
        if hexCoords!=self.currHexCoords:
            if hexCoords in self.model.field._field:
                self.currHexCoords = hexCoords
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
            else:
                self.currHexCoords = None
                self.canvas.itemconfigure(self.displayCoords, text='')
                
    
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
        self.currentStep+=1
        self.numBacteria = self.model.count_bacteria()
        self.numPredators = self.model.count_predators()
        if self.traceWriter is not None:
            self.traceWriter.write(self.currentStep, self.numBacteria, self.numPredators)
        if self.check_for_halt():
            self.play = False
        self.draw_field()
        if self.play:
            self.tk.after(self.stepDelay,self.step)
    
    def check_for_halt(self):
        if self.numPredators==0:
            self.haltReason = 'No more predators left'
            return True
        if self.numBacteria==0:
            self.haltReason = 'No more bacteria left'
            return True
        return False
    
    def open_state(self):
        self.model.parse_state(state.load_state_dlg())
        self.init_board_state()
        
    def save_state(self):
        state.save_state_dlg(state.BacterioState(self.model.field, self.model.bacteriaPositions, self.model.predatorPositions))
    
    
    def proceed_cell_change(self):
        self.haltReason = ''
        self.draw_field()
        
    def add_bacteria(self):
        if self.currHexCoords is None:
            return
        self.model.add_bacteria(self.currHexCoords)
        self.numBacteria += 1
        self.proceed_cell_change()
    
    def add_predator(self):
        if self.currHexCoords is None:
            return
        self.model.add_predator(self.currHexCoords)
        self.numPredators += 1
        self.proceed_cell_change()
    
    def clear_cell(self):
        if self.currHexCoords is None:
            return
        self.model.clear_cell(self.currHexCoords)
        self.numBacteria = self.model.count_bacteria()
        self.numPredators = self.model.count_predators()
        self.proceed_cell_change()
    
    def clear_board(self):
        self.model.clear_all()
        self.numBacteria = 0
        self.numPredators = 0
        self.proceed_cell_change()
       
       
if __name__=='__main__':
    root = Tk()
    root.title('Bacterio')
    main = MainWindow(root)
    root.mainloop()

