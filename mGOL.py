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

# for multiprocessing
import concurrent.futures



# some variables for general setup
# sizes of the world:
sizeX = 200 // 1
sizeY = 100 // 1

# display resolution
width = 1280 
height = 720 
# height = int((sizeY / sizeX) * width) + 100 

# size for the drawed rectangle
size = int(min(width / sizeX, (height - 50) / sizeY))

# centering display
offsetX = int((width - size*sizeX) / 2) 
offsetY = int((height - size*sizeY) / 2) 

# generating the start status of the world
world_now = np.random.randint(2, size=(sizeY, sizeX),dtype=int)
generation = 0
# print('Initial world state:')
# print(world_now)

# getting the size of the world array
R, C = world_now.shape

# now lets go thru the world array
# and proceed with the GOL algorithm
# sum 2 or 3 - keep alive if alive
# sum 3 - born if death

# function for splitting the world array into sub portions
def getranges(array, dR=1, dC=1):
    '''this function is about figuring out sets of tuples
    to split the array for multiprocess needs
    Inputs:
    array - the 2D np array of the world
    dR - divisions in rows
    dC - divisions in columns
    Output:
    List of prepared set of tuples
    '''
    Rows, Cols = array.shape

    rows_per_step = Rows // dR 
    cols_per_step = Cols // dC
    areas = dR * dC

    output = []

    for c in range(dC):
        startC = c * cols_per_step
        endC = min((c + 1) * cols_per_step, Cols- 1) 
        for r in range(dR):
            startR = r * rows_per_step
            endR = min((r + 1) * rows_per_step, Rows - 1)

            line = ((startC, endC), (startR, endR))
            
            output.append(line)
    
    return output

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

def gen(area = None):
    '''This is the Game Of Life single generation function.
    Input:
    area - the tuple of ranges in C and R: ((C1,C2),(R1,R2))
    Output:
    numpy array of the world status after single generation'''
    global generation, world_now
    
    # lets keep the current state as next one
    world_next = np.array(world_now)
    # print(area)
    if not area:
        Crange = range(C)
        Rrange = range(R)
    else:
        Crange = range(area[0][0],area[0][1]+1)
        Rrange = range(area[1][0],area[1][1]+1)

    # lets normalize world_now
    world_now_norm = np.array(world_now)
    world_now_norm[world_now_norm > 0] = 1

    # making empty array for world update after gen

    clean_world = np.zeros((len(Rrange),len(Crange)),dtype=int)

    
    # man from range: range(start, stop, step)
    # lets analyze
    for x in Crange:
        for y in Rrange:
            suma = int(subarraysum(world_now_norm, x, y))
            current = world_next[y,x]

            if current and 2 <= suma <= 3:  # we survive
                world_next[y,x] = min(255, world_next[y,x]+1)
            elif not current and suma == 3:  # we get born
                world_next[y,x] = 1
            else:  # we die
                world_next[y,x] = 0

            clean_world[y-min(Rrange),x-min(Crange)] = int(world_next[y,x])
    # we bring back the world status to world now
    # world_now = np.array(world_next)
    generation += 1
    return clean_world
    # print(f'World of {generation}:')
    # print(world_now)


def main():
    global world_now,generation
    pygame.init()

    DISPLAY=pygame.display.set_mode((width,height),0,32)

    BCK=(128,128,128)
    BLUE=(0,0,255)

    active = True
    setOnMouse = False
    mouseValue = 1
    drawstep = 1
    step = 0
    makestep = False
    multi = False
    averspeed = []

    ranges = getranges(world_now, 10, 10)
    print(ranges)

    while True:
        step += 1
        NOW = dt.now()

        if not active:
            BCK = (25,25,25)
        elif multi:
            BCK = (128,2,2)
        else:
            BCK = (128,128,128)

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
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
                    makestep = True

                elif event.key == pygame.K_r:
                    active = False
                    world_now = np.zeros((R,C))

                elif event.key in [pygame.K_s, pygame.K_g]:
                    active = not active
                    
                elif event.key in [pygame.K_m]:
                    multi = not multi
                
        
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
                        color = (max(255-world_now[y,x],0),max(255-int(world_now[y,x]/2),0),min(world_now[y,x],255))
                    pygame.draw.rect(DISPLAY,color,(offsetX + size*x+1, offsetY + size*y+1,size-1,size-1))
    
        if makestep:
            active = True

        if active:
            world_next = np.zeros((R,C))
            if not multi:
                for r in ranges:
                    A = gen(r)
                    c,d,a,b = r[0][0], r[0][1], r[1][0], r[1][1]
                    world_next[a:b+1,c:d+1] = A
                    generation += 1
            else:
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    results = executor.map(gen, ranges)
                    
                    for ix, res in enumerate(results):
                        A = res
                        r = ranges[ix]
                        c,d,a,b = r[0][0], r[0][1], r[1][0], r[1][1]
                        world_next[a:b+1,c:d+1] = A
                        generation += 1

            world_now = world_next

            if makestep:
                active = False
                makestep = False

        pygame.display.update()
        NOW = (dt.now() - NOW).total_seconds()
        averspeed.append(1/NOW)
        avFreq = 1/NOW
        if len(averspeed) >= 10:
            avFreq = sum(averspeed) / 10
            averspeed = []

        print(f'Gen freq: {(1 / NOW):10.4f} gen/s; averFreq: {avFreq}', end='\r',flush=True)



main()
