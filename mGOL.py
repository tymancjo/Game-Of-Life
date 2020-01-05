# This is my quick project idea
# A Game Of Life implementation
# Done just for fun andPython training
# the general idea comes form classic:
# https://pl.wikipedia.org/wiki/Gra_w_%C5%BCycie

# plan to work it out as pythonic as possible :)
# this file is intended to be multi process version  

# one: play around with numpy arrays to understood it deeply
# pygame: used for the visual presentation of the system

# let's import the numpy library
import numpy as np

# and stuff for drawing
import pygame, sys
from pygame.locals import *
from datetime import datetime as dt



# pre start stuff
NOW = dt.now()


# some variables for general setup
# sizes of the world:
sizeX = 128 // 3
sizeY = 60 // 3

# display resolution
width = 1280 
height = 720 
# height = int((sizeY / sizeX) * width) + 100 

# size for the drawed rectangle
size = int(min(width / sizeX, height / sizeY))

# centering display
offsetX = int((width - size*sizeX) / 2) 
offsetY = int((height - size*sizeY) / 2) 

# generating the start status of the world
world_now = np.random.randint(2, size=(sizeY, sizeX))
generation = 0
# print('Initial world state:')
# print(world_now)

# getting the size of the world array
R, C = world_now.shape

# now lets go thru the world array
# and proceed with the GOL algorithm
# sum 2 or 3 - keep alive if alive
# sum 3 - born if death

# defined functions
def subarraysum(array, x, y):
    '''This is summing the value around given place in array 
    for the game of life algorithm 
    Inputs:
    array - 2D the array we are working on
    x,y - col, row coordinates of theanalyzed point
    return:
    sum of point neighbors 
    '''
    # limiting to the array size 
    r, c = array.shape
    x = min(max(x,0),c - 1)
    y = min(max(y,0),r - 1)
    return sum(sum(array[max(y-1,0):min(y+2,r), max(x-1,0):min(x+2,c)])) - array[y,x]

def gen(world_now):
    '''This is the Game Of Life single generation function.
    Input:
    world_now - the 2D numpy array of the current world status
    Output:
    numpy array of the world status after single generation'''
    
    global generation
    # lets keep the current state as next one
    world_next = np.array(world_now)

    # lets normalize world_now
    world_now = np.nan_to_num(world_now / world_now)

    # lets analyze
    for x in range(C):
        for y in range(R):
            suma = subarraysum(world_now, x, y)
            current = world_next[y,x]

            if current and 2 <= suma <= 3:  # we survive
                world_next[y,x] = min(255, world_next[y,x]+1)
            elif not current and suma == 3:  # we get born
                world_next[y,x] = 1
            else:  # we die
                world_next[y,x] = 0

    # we bring back the world status to world now
    world_now = np.array(world_next)
    generation += 1
    return world_now
    # print(f'World of {generation}:')
    # print(world_now)


def main():
    global world_now,NOW
    pygame.init()

    DISPLAY=pygame.display.set_mode((width,height),0,32)

    BCK=(128,128,128)
    BLUE=(0,0,255)

    active = True
    setOnMouse = False
    mouseValue = 1
    drawstep = 1
    step = 0

    while True:
        step += 1

        if not active:
            BCK = (25,25,25)
        else:
            BCK = (128,128,128)

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                NOW = (dt.now() - NOW).total_seconds()
                print(f'Genertions: {generation}, in {NOW}, so: {generation / NOW} gen/s')
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                mx, my = event.pos
                mc = int((mx - offsetX)/(size)) 
                mr = int((my - offsetY)/(size)) 
                if 0 <= mc < C and 0 <= mr < R:
                    setOnMouse= True
                    pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
                    if pressed1:
                        mouseValue = 1
                    else:
                        mouseValue = 0
                    
                elif mr >= R:
                    active = not active
                    
                else:
                    if not active:
                        world_now = np.zeros((R,C))
            elif event.type == pygame.MOUSEBUTTONUP:
                setOnMouse = False

            elif event.type == pygame.KEYDOWN:
                if not active and event.key == pygame.K_SPACE:
                    world_now = gen(world_now)

                elif event.key == pygame.K_r:
                    world_now = np.zeros((R,C))
                    active= False

                elif event.key in [pygame.K_s, pygame.K_g]:
                    active = not active

                
        
        if setOnMouse:
            mmx, mmy = pygame.mouse.get_pos()
            mmc = max(0,min(C-1,int((mmx - offsetX)/(size)))) 
            mmr = max(0,min(R-1,int((mmy - offsetY)/(size)))) 
            
            world_now[mmr, mmc] = mouseValue
            
        if not (step % drawstep):
            step = 0 
            DISPLAY.fill((BCK))
            for x in range(C):
                for y in range(R):
                    color = (166,166,166)
                    if world_now[y,x]:
                        color = (255-world_now[y,x],255-int(world_now[y,x]/2),world_now[y,x])
                    pygame.draw.rect(DISPLAY,color,(offsetX + size*x+1, offsetY + size*y+1,size-1,size-1))
    
        if active:
            world_now = gen(world_now)
        pygame.display.update()


main()
