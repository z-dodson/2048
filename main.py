"""
2048 clone in pygame
Very poorly written code I made a long time ago and added some stuff to
"""

import pygame
import time
import math as maths
import random
from colours import *

SQ_WIDTH = int(80)
SQ_HEIGHT = int(SQ_WIDTH)
GAP = 10
WIDTH_MARGIN = 100
HEIGHT_MARGIN = 60
WIDTH = (GAP+SQ_WIDTH)*4+WIDTH_MARGIN*2
HEIGHT = (SQ_HEIGHT+GAP)*4+HEIGHT_MARGIN*2
M_WIDTH = int(SQ_WIDTH//2)# m refering to marker
M_HEIGHT = int(SQ_HEIGHT//2)
ANIMATION_SPEED = 1

BACKGROUND = (200,200,200)
GRID_DATA = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

# Global Variables
SCORE = 0
ACTIVE_SQUARES = []


class Graphic(pygame.sprite.Sprite):
    def __init__(self,number,x1,x2,y1,y2):
        super.__init__(graphics)
        i = pygame.image.load(f'img/{number}.png').convert()
        self.image = pygame.transform.scale(i,(SQ_WIDTH,SQ_HEIGHT))
        self.dx = (x2 - x1)*SQ_HEIGHT
        self.dy = (y2 - y1)*SQ_WIDTH
    
    def update(self):
        if(self.dy!=0): pass
        elif(self.dx!=0): pass
        else: self.kill()
        
class BackingPiece(pygame.sprite.Sprite):
    def __init__(self, xsq, ysq):
        super().__init__(backing)
        self.ASvalue = f"{xsq}{ysq}"
        self.alpha = 255
        self.xsq = xsq
        self.ysq = ysq
        self.image = pygame.surface.Surface([SQ_WIDTH,SQ_HEIGHT])
        self.image.fill(WHITE)
        self.rect.x = WIDTH_MARGIN+(SQ_WIDTH+GAP)*(self.xsq-1)
        self.rect.y = HEIGHT_MARGIN+(SQ_WIDTH+GAP)*(self.ysq-1)



class Piece(pygame.sprite.Sprite):
    def __init__(self, xsq, ysq):
        super().__init__()
        self.number = 0
        self.ASvalue = f"{xsq}{ysq}"
        self.alpha = 255
        self.xsq = xsq
        self.ysq = ysq
        self.setImg()
        pieces.add(self)
        self.targetx = self.rect.x
        self.targety = self.rect.y

    def updateSqs(self):
        """This should actually oly be used at the start, but i'm keeping it a function in case it useful later"""        
        self.rect.x = WIDTH_MARGIN+(SQ_WIDTH+GAP)*(self.xsq-1)
        self.rect.y = HEIGHT_MARGIN+(SQ_WIDTH+GAP)*(self.ysq-1)
    
    def setNum(self, number=0, new=False):
        if(self.number==0)and new: self.alpha = 0
        self.number= number
        self.setImg()
    
    def setImg(self):
        if(self.number!=0):
            i = pygame.image.load(f'img/{self.number}.png').convert()
            self.image = pygame.transform.scale(i,(SQ_WIDTH,SQ_HEIGHT))
            if not self.ASvalue in ACTIVE_SQUARES: ACTIVE_SQUARES.append(self.ASvalue)
        else:
            self.image = pygame.surface.Surface([SQ_WIDTH,SQ_HEIGHT])
            self.image.fill(WHITE)
            if self.ASvalue in ACTIVE_SQUARES: ACTIVE_SQUARES.remove(self.ASvalue)
        self.rect = self.image.get_rect()
        self.updateSqs()
    
    def update(self):
        if self.alpha!=255:
            self.image.set_alpha(self.alpha)
            self.alpha+=255//(255//ANIMATION_SPEED)
            if self.alpha>255: self.alpha = 255
    #     if self.targetx!=self.rect.x: 
    #         self.rect.x += ((self.rect.x-self.targetx)/abs(self.rect.x-self.targetx))*(ANIMATION_SPEED*self.dx)
    #     elif self.targety!=self.rect.y: 
    #         self.rect.y += ((self.rect.y-self.targety)/abs(self.rect.y-self.targety))*(ANIMATION_SPEED*self.dy)

    # def assignMovement(self, dx, dy):
    #     self.dx = dx
    #     self.dy = dy
    #     self.targetx = self.rect.x+dx
    #     self.targety = self.rect.y-dy

            
    

def generateNewTile():
    a = random.randint(1,4)
    b = random.randint(1,4)
    while(GRID_DATA[a-1][b-1]!=0):
        a = random.randint(1,4)
        b = random.randint(1,4)
    GRID_ITEMS[a-1][b-1].setNum(random.choice((2,2,2,4)), True)
    GRID_DATA[a-1][b-1] = 2
    #ACTIVE_SQUARES.append(f"{a}{b}")
    
    
def thingInMoveFunctions(row,rowref=0,direcReference="X or Y",reverse=False):
    n=0
    if direcReference=="X":
        if reverse: animations= [Animation(item,3-index,rowref,direcReference) for index, item in enumerate(row)if item!=0]
        else: animations= [Animation(item,index,rowref,direcReference) for index, item in enumerate(row)if item!=0]
    elif direcReference=="Y":
        if reverse: animations= [Animation(item,rowref,3-index,direcReference) for index, item in enumerate(row)if item!=0]
        else: animations= [Animation(item,rowref,index,direcReference) for index, item in enumerate(row)if item!=0]
    while 0 in row:
        row.remove(0)
        n+=1
    newRow = []
    if row:
        newRow = [row[0]]
        row.pop(0)
        if reverse: animations[0].setMove(3)
        else: animations[0].setMove(0)
    if row:
        notjoined = True
        i=0# first thing has alleeady been done
        a = 0
        for thing in row: # Block joins
            a+= 1# allways happends
            if thing == newRow[-1] and notjoined:
                global SCORE
                newRow[-1] *= 2
                SCORE += newRow[-1]
                n += 1  # Add another unregistered black space
                notjoined = False
            else: # Block moves to the end
                newRow.append(thing)
                i += 1#move the counter up by one
                notjoined = True
            if reverse: animations[a].setMove(3-i)
            else: animations[a].setMove(i)
    for _ in range(n): newRow.append(0)
    return newRow
    
def convertToColoumnsOrRows(list1):
    list2 = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(4):
        for j in range(4):
            list2[j][i] = list1[i][j]
    return list2

def moveLeft():
    global GRID_DATA
    tempcopy_GRID_DATA = [thing for thing in GRID_DATA]
    new_GRID_DATA = []
    for index,row in enumerate(GRID_DATA): new_GRID_DATA.append(thingInMoveFunctions(row,index,"X"))
    GRID_DATA = new_GRID_DATA
    for i in range(4):
        for j in range(4): GRID_ITEMS[i][j].setNum(GRID_DATA[i][j])
    if(GRID_DATA==tempcopy_GRID_DATA): return False
    return True

def moveUp(): # Just going to 'rotate' the list becuase I really cant  be bothered to do somthing using effort with numbers
    global GRID_DATA
    tempcopy_GRID_DATA = [thing for thing in GRID_DATA]
    new_GRID_DATA = []
    for index,row in enumerate(convertToColoumnsOrRows(GRID_DATA)): new_GRID_DATA.append(thingInMoveFunctions(row,index,"Y"))
    GRID_DATA = convertToColoumnsOrRows(new_GRID_DATA)
    for i in range(4):
        for j in range(4): GRID_ITEMS[i][j].setNum(GRID_DATA[i][j])
    if(GRID_DATA==tempcopy_GRID_DATA): return False
    return True

def reverse(lst): return [ele for ele in reversed(lst)] # this saves me effort

def moveDown(): # Just going to 'rotate' the list becuase I really cant  be bothered to do somthing using effort with numbers
    global GRID_DATA
    tempcopy_GRID_DATA = [thing for thing in GRID_DATA]
    new_GRID_DATA = []
    for index,row in enumerate(convertToColoumnsOrRows(GRID_DATA)): new_GRID_DATA.append(reverse(thingInMoveFunctions(reverse(row),index,"Y",True)))
    GRID_DATA = convertToColoumnsOrRows(new_GRID_DATA)
    for i in range(4):
        for j in range(4): GRID_ITEMS[i][j].setNum(GRID_DATA[i][j])
    if(GRID_DATA==tempcopy_GRID_DATA): return False
    return True

def moveRight():
    global GRID_DATA
    tempcopy_GRID_DATA = [thing for thing in GRID_DATA]
    new_GRID_DATA = []
    for index,row in enumerate(GRID_DATA): new_GRID_DATA.append(reverse(thingInMoveFunctions(reverse(row),index,"X",True)))
    GRID_DATA = new_GRID_DATA
    for i in range(4):
        for j in range(4): GRID_ITEMS[i][j].setNum(GRID_DATA[i][j])
    if(GRID_DATA==tempcopy_GRID_DATA): return False
    return True

class Animation(pygame.sprite.Sprite):
    def __init__(self, value, xcoord, ycoord, direction):
        super().__init__(animations)
        i = pygame.image.load(f'img/{value}.png').convert()
        self.image = pygame.transform.scale(i,(SQ_WIDTH,SQ_HEIGHT))
        self.values = value
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.direction = direction
        # self.image = pygame.Surface((10,10))
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = self.rect.x = WIDTH_MARGIN+(SQ_WIDTH+GAP)*(self.xcoord)
        self.y = self.rect.y = HEIGHT_MARGIN+(SQ_WIDTH+GAP)*(self.ycoord)
        self.newXcoord = 2
        self.newYcoord = 2
    def setMove(self,newCoord):
        if self.direction=="X":
            self.newXcoord = newCoord
            self.newYcoord = self.ycoord
            self.increment = ((self.newXcoord-self.xcoord)*(SQ_WIDTH))/(225/ANIMATION_SPEED)
        elif self.direction=="Y":
            self.newXcoord = self.xcoord
            self.newYcoord = newCoord
            self.increment = ((self.newYcoord-self.ycoord)*(SQ_HEIGHT))/(225/ANIMATION_SPEED)
    def __str__(self): return f">{(self.newXcoord-self.xcoord)} ^{(self.newYcoord-self.ycoord)} "# For debugging #f"Animation Object\nX ({self.xcoord}->{self.newXcoord})\nY ({self.ycoord}->{self.newYcoord})\n*****"#Animation Object\nxcoord={self.xcoord}\tycoord={self.ycoord}\nnewXcoord={self.newXcoord}\tnewYcoord={self.newYcoord}\n*****"
    def update(self):
        if self.direction=="X": 
            self.x += self.increment
            self.rect.x = int(self.x)
        elif self.direction=="Y": 
            self.y += self.increment
            self.rect.y = int(self.y)

def draw():
    pieces.update()
    animations.update()
    scoreText = FONT.render(f"Score: {SCORE}", True, GREY, WHITE)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.x = 30
    scoreTextRect.y = 5
    screen.fill(BACKGROUND)
    backing.draw(screen)
    pieces.draw(screen)
    animations.draw(screen)
    screen.blit(scoreText,scoreTextRect)
    pygame.display.flip()



if __name__=="__main__":
    pygame.init()
    pygame.font.init()
    FONT = pygame.font.SysFont("Arial", 30)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    backing = pygame.sprite.Group()
    pieces = pygame.sprite.Group()
    graphics = pygame.sprite.Group()
    animations = pygame.sprite.Group()
    
    screen.fill(BACKGROUND)
    GRID_ITEMS = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(1,5):#columns
        for j in range(1,5):#rows as in list, it appears bottom row has been lost
            GRID_ITEMS[j-1][i-1] = Piece(i,j) #Square((WIDTH_MARGIN+j*(SQ_WIDTH+GAP)),(HEIGHT_MARGIN+i*(SQ_HEIGHT+GAP)),white)
    pieces.draw(screen)
    pygame.display.update()
    clock = pygame.time.Clock()
    done = False
    done = False
    SCORE = 0
    generateNewTile()
    draw()
    while not done:
        clock.tick(30)
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:#X
                    clicked = True
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT: clicked = moveRight()
                    if event.key == pygame.K_LEFT: clicked = moveLeft()
                    if event.key == pygame.K_UP: clicked = moveUp()
                    if event.key == pygame.K_DOWN: clicked = moveDown()
        if done: break
        for piece in pieces: piece.setNum()
        generateNewTile()
        for _ in range(int(255//ANIMATION_SPEED)): draw()
        for a in animations: a.kill()
        for i in range(4):
            for j in range(4): GRID_ITEMS[i][j].setNum(GRID_DATA[i][j])
        draw()
        animations = pygame.sprite.Group()
        pygame.display.flip()
    time.sleep(0.5)
    pygame.quit()
    exit()