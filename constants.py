import pygame

# Screen window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Title
TITLE = "Wumpus World"

# Object images
PIT_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/pit.png"
WUMPUS_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/wumpus.png"
CHEST_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/chest.png"
BREEZE_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/breeze.png"
STENCH_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/stench.png"

# Agent images
AGENT_RIGHT_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/agent-right.png"
AGENT_LEFT_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/agent-left.png"
AGENT_UP_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/agent-up.png"
AGENT_DOWN_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/agent-down.png"

# Arrow images
ARROW_RIGHT_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/arrow-right.png"
ARROW_LEFT_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/arrow-left.png"
ARROW_UP_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/arrow-up.png"
ARROW_DOWN_IMG = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/arrow-down.png"

# Font style
FONT_STYLE = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/font/mrsmonster.ttf"

# Inputs
MAP_1 = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/inputs/map_1.txt"
MAP_2 = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/inputs/map_1.txt"
MAP_3 = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/inputs/map_1.txt"
MAP_4 = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/inputs/map_1.txt"
MAP_5 = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/inputs/map_1.txt"

# Other metrics
CELL_SIZE = 67

# Success/Failed image
SUCCESS_IMAGE = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/success.png"
FAILED_IMAGE = "/Users/apple/Documents/UniversityDocument/Nam3/AI/Project 2/Logical-Agent/assets/images/failed.png"

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