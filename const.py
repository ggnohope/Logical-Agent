import pygame

# Screen window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Title
TITLE = "Wumpus World"

# Object images
PIT_IMG = "./assets/images/pit.png"
WUMPUS_IMG = "./assets/images/wumpus.png"
CHEST_IMG = "./assets/images/chest.png"
BREEZE_IMG = "./assets/images/breeze.png"
STENCH_IMG = "./assets/images/stench.png"

# Agent images
AGENT_RIGHT_IMG = "./assets/images/agent-right.png"
AGENT_LEFT_IMG = "./assets/images/agent-left.png"
AGENT_UP_IMG = "./assets/images/agent-up.png"
AGENT_DOWN_IMG = "./assets/images/agent-down.png"

# Arrow images
ARROW_RIGHT_IMG = "./assets/images/arrow-right.png"
ARROW_LEFT_IMG = "./assets/images/arrow-left.png"
ARROW_UP_IMG = "./assets/images/arrow-up.png"
ARROW_DOWN_IMG = "./assets/images/arrow-down.png"

# Font style
FONT_STYLE = "./assets/font/Valorax-lg25V.otf"

# Inputs
MAP_1 = "./assets/inputs/map_1.txt"
MAP_2 = "./assets/inputs/map_1.txt"
MAP_3 = "./assets/inputs/map_1.txt"
MAP_4 = "./assets/inputs/map_1.txt"
MAP_5 = "./assets/inputs/map_1.txt"

# Other metrics
CELL_SIZE = 70

# Success/Failed image
SUCCESS_IMAGE = "./assets/images/success.png"
FAILED_IMAGE = "./assets/images/failed.png"

# speed
SPEED = 500

#####  Button Settings #####
MAIN_BUTTON_Y_POS = 550

# Dimensions of Main-Menu Buttons
MAIN_BUTTON_LENGTH = 250
MAIN_BUTTON_HEIGHT = 45

# Dimensions/Settings of Grid-Menu Buttons
START_END_BUTTON_HEIGHT = 335
BUTTON_SPACER = 20
GRID_BUTTON_LENGTH = 200
GRID_BUTTON_HEIGHT = 50

##### Colour Settings #####
WHITE = (255,255,255)
AQUAMARINE = (127,255,212)
BLACK = (0,0,0)
ALICE = (240,248,255)
STEELBLUE = (110,123,139)
MINT = (189,252,201)
SPRINGGREEN = (0,255,127)
TOMATO = (255,99,71)
ROYALBLUE = (72,118,255)
TAN = (255,165,79)
RED = (255,0,0)
VIOLETRED = (255,130,171)
TURQUOISE = (30,144,255)

##### Grid Settings #####
# GS MEANS Grid-Start
GS_X = 264
GS_Y = 24
# GE MEANS Grid-End
GE_X = 1512
GE_Y = 744