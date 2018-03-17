![Logo](logo.png)

# **Bacterio** - simulating simple hypothetical protozoa biosystem

Consider a Petri dish fullfilled with some growth medium and two types of protozoa: one is suppoted by growth medium (later referred as _bacteria_) while the other feeds on the first one (later referred as _predators_). As far as there are plenty of medium bacteria are always well-fed unlike predators those need to hunt bacteria to survive and breed. Lucky for them bacteria are 'blind' - they don't aware of predators.

_**Disclaimer:**_ it's very unlikely that presented simulation model could be applied for any real protozoa biosystem. The main purpose of this project is to develop fluctuating but balanced non-deterministic system.


## Getting started

### Prerequisites
+ [Python 3+](https://www.python.org/downloads/) (tested with  3.6.3)
+ [TkInter](https://docs.python.org/3/library/tkinter.html) support (you may check it running `python -m tkinter`)

### Installing and running

Just clone (or fork) this repo, `cd` to its folder and run  
```
python main.py
```

### Controls
`r` - enter *play* mode (proceed step after step with a brief delay); *play* will stop if *halt conditions* met  
`<Space>` - proceed one step (also exit *play* mode)  
`z` or `<Mouse-1>` - place bacteria on cell under cursor  
`x` or `<Mouse-3>` - place predator on cell under cursor  
`c` or `<Mouse-2>` - clear cell under cursor  
`<Ctrl>+s` - save current state to file  
`<Ctrl>+o` - open saved state  
`<Esc>` - exit  

### Halt conditions
Currently there are two conditions which could cause *play* mode to stop:
+ there are no more predators left on the field;
+ there are no more bacteria left on the field.

## Configuration

### Configuring GUI colors (palette)
Colors are loaded from `palette.ini` file. You may change them by using Tk color names (RGB like #000000 or [symbolic](https://www.tcl.tk/man/tcl8.5/TkCmd/colors.htm) names). Some palletes are stored in `palettes` directory. To use one of them replace `palette.ini`.

### Configuring initial field parameters
Initial field parameters are loaded from `FIELD` category in `config.ini` file.
(TODO:)

### Configuring model parameters
Model parameters are loaded from `MODEL` category in `config.ini` file.
(TODO:)

### Configuring miscellaneous parameters
Miscellaneous application parameters are loaded from `misc.ini` file.
(TODO:)


## License

[MIT](LICENSE)
