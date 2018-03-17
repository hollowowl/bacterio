![Logo](logo.png)

# **Bacterio** - simulating simple hypothetical protozoa biosystem

Consider a Petri dish fullfilled with some growth medium and two types of protozoa: one is suppoted by growth medium (later referred as _bacteria_) while the other feeds on the first one (later referred as _predators_). As far as there are plenty of medium bacteria are always well-fed unlike predators who need to hunt bacteria to survive and breed. Lucky for them bacteria are 'blind' - they don't aware of predators.

_**Disclaimer:**_ it's very unlikely that presented simulation model could be applied for any real protozoa biosystem. The main purpose of this project is to develop fluctuating but balanced non-deterministic system.  
(And yes, this is just another [Zero-player game](https://en.wikipedia.org/wiki/Zero-player_game))


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
`r` - enter *play* mode (proceed step after step with a brief delay); *play* will stop if [halt conditions](#halt-conditions) met  
`<Space>` - proceed one step (also exit *play* mode)  
`z` or `<Mouse-1>` - place bacteria on cell under cursor  
`x` or `<Mouse-3>` - place predator on cell under cursor  
`c` or `<Mouse-2>` - clear cell under cursor  
`<Ctrl>+c` - clear the entire field  
`<Ctrl>+s` - save current state to file  
`<Ctrl>+o` - open saved state  
`<Esc>` - exit  


## Model description

### Basics  
(TODO:)

### Halt conditions
Currently there are two conditions which could cause *play* mode to stop:  
+ there are no more predators left on the field;  
+ there are no more bacteria left on the field.  

## Configuration

### Configuring GUI colors (palette)
Colors are loaded from [palette.ini](palette.ini) file. You may change them by using Tk color names (RGB like #000000 or [symbolic](https://www.tcl.tk/man/tcl8.5/TkCmd/colors.htm) names). Some palletes are stored in [palettes](palletes) directory. To use one of them replace [palette.ini](palette.ini).

### Configuring initial field parameters
Initial field parameters are loaded from `FIELD` category in [config.ini](config.ini) file.  
`stateFile` - forces to load initial field state from given file ignoring the rest of `FIELD` section  
`radius` - board (_Petri dish_) radius (cells)
`initBacteria` - number of bacteria should be randomly placed on field during initialization  
`initPredators` - number of predators should be randomly placed on field during initialization  

### Configuring model parameters
Model parameters are loaded from `MODEL` category in [config.ini](config.ini) file.  
The following model parameters currently supported:  
for *bacteria*  
`P_BACT_DIVIDE` - probability that bacteria will divide on two bacteria (both in the same cell) unless there are >= `BACT_OVERCROWD` bacteria in given cell  
`P_BACT_STAY` -  probability that bacteria will stand still (in case if it not divided)  
`BACT_OVERCROWD` -  number of maximum number of bacteria within BACT_OVERCROWD_RADIUS (if more or equal, bacteria will not divide)  
`BACT_OVERCROWD_RADIUS`  
`BACT_VELOCITY` - bacteria's velocity (cells per move)  
  
for *predators*  
`PR_INIT_ENERGY` - initial predator's energy  
`PR_MAX_ENERGY` - value of energy when predator stops hunting (until loose energy below this value)  
`PR_DIVIDE_ENERGY` - minimal energy value at which predator's divide is possible. Offsprings will have `(E-PR_DIVIDE_COST)//2` energy  
`PR_DIVIDE_COST` - energy cost of predator's division  
`PR_TURN_COST` -  energy cost of each predator's turn (except division or feed)  
`PR_FEED_VALUE` - energy gained by predator after successful hunting  
`PR_SIGHT` - predator's sight range  
`P_PR_DIVIDE` - probability of predator's division (if its energy>=PR_DIVIDE_ENERGY)  
`P_PR_STAY` - probability that predator remain still if he is fed up (energy>=PR_MAX_ENERGY)  
`PR_OVERCROWD` - number of maximum number of predators within PR_OVERCROWD_RADIUS (if more or equal, predator will not divide)  
`PR_OVERCROWD_RADIUS`  
  

### Configuring miscellaneous parameters
Miscellaneous application parameters are loaded from [misc.ini](misc.ini) file.  
`width` - field width (in px)  
`height` - field height (in px)  
`writeTrace` - if `true` trace will be writen after each play; `traceFilePrefix` should be specified in that case  
`traceFilePrefix` - prefix of trace file (suffix is datetime in format *yyyymmdd-HH-MM-SS* and *.btf* extension)  
`stepDelay` - minimum delay between steps in *play* mode in milliseconds (real delay is bigger and depends on OS, harware, field and model parameters)  


## License

[MIT](LICENSE)
