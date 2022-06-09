#ALL COLOR CONSTANT VLAUES
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,225,0)
YELLOW = (225,225,0)
PINK = (225,0,225)
LIGHT_BLUE = (0,225,225)
DARK_GREEN = (0,100,0)
GREY = (200,200,200)
DARK_GREY = (100,100,100)
BROWN =  (165,42,42)

def COLOUR_INFO():
    print("no")

def randomColour():
    from random import choice as r
    return r([RED,GREEN,YELLOW,BROWN])
