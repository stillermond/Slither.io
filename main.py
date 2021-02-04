#slither game
#written by Dr. Mo, 1/20/2021 Nathaniel DeLeon
import pygame #imports pygame libary
import math #needed for square root function
import random


pygame.init()#initializes Pygame
pygame.display.set_caption("Slither")#sets the window title
screen = pygame.display.set_mode((400,400))#creates game screen
clock = pygame.time.Clock() # Start game clock

#Game varibles
doExit = False

#player variables
xPos = 200
yPos = 200
Vx = 1
Vy = 1

oldX = 200
oldY = 200

xPos2 = 200
yPos2 = 200
Vx2 = 1
Vy2 = 1

oldX2 = 200
oldY2 = 200

class TailSeg:
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
    def update(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
    def draw(self):
        pygame.draw.circle(screen, (200, 0 , 0), (self.xpos, self.ypos),12)
    def collide(self, x, y):
        if math.sqrt((x-self.xpos)*(x-self.xpos)+(y-self.ypos)*(y-self.ypos)) < 6:
            return True

#Class pellet ------
class pellet:
    def __init__(self, xpos, ypos, red, green, blue, radius):
        self.xpos = xpos
        self.ypos = ypos
        self.red = red
        self.green = green
        self.blue = blue
        self.radius = radius
    def draw(self):
        pygame.draw.circle(screen,(self.red,self.green,self.blue),(self.xpos,self.ypos),self.radius)
    def collide (self, x, y):
        if math.sqrt((x-self.xpos)*(x-self.xpos)+(y-self.ypos)*(y-self.ypos)) < self.radius + 6:
            self.xpos = random.randrange(0,400)
            self.ypos = random.randrange(0,400)
            self.red = random.randrange(0,255)
            self.blue = random.randrange(0,255)
            self.green = random.randrange(0,255)
            self.radius = random.randrange(0,30)
            return True
#End of class pellet ------

counter = 0

pelletBag = list()#creates a list data structure
tail = list()
tail2 = list()
for i in range(10):
    pelletBag.append(pellet(random.randrange(0,400), random.randrange(0,400), random.randrange(0,255),random.randrange(0,255),random.randrange(0,255),random.randrange(0,30)))

#Gameloop --------
while not doExit:
    
#event/input section -----
    clock.tick(60)
    
    for event in pygame.event.get(): #Grabs any events (Mouse movement, keyboard, ect)
        if event.type == pygame.QUIT: #Lets you quit the game from the gamescreen
            doExit = True
        if event.type == pygame.MOUSEMOTION:
            mousePos = event.pos
            if mousePos[0] > xPos:
                Vx = 1
            else:
                Vx = -1
                
            if mousePos[1] > yPos:
                Vy = 1
            else:
                Vy = -1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        xPos2 -= 1
    if keys[pygame.K_RIGHT]:
        xPos2 += 1
    if keys[pygame.K_UP]:
        yPos2 -= 1
    if keys[pygame.K_DOWN]:
        yPos2 += 1   
           
    counter+=1 #Update counter
    if counter == 20: #Create a delay so the segments follow behind
        counter = 0 #Hold onto old player positon from 20 ticks ago
        oldX = xPos
        oldY = yPos
        oldX2 = xPos2
        oldY2 = yPos2
        
        if(len(tail)>2):
            for i in range(len(tail)):
                tail[len(tail)-i-1].xpos = tail[len(tail)-i-2].xpos
                tail[len(tail)-i-1].ypos = tail[len(tail)-i-2].ypos
        if(len(tail2)>2):
            for i in range(len(tail2)):
                tail2[len(tail2)-i-1].xpos = tail2[len(tail2)-i-2].xpos
                tail2[len(tail2)-i-1].ypos = tail2[len(tail2)-i-2].ypos
        if(len(tail)>0):
            tail[0].update(oldX, oldY)
        if(len(tail2)>0):
            tail2[0].update(oldX2, oldY2)

#physics section ----
        #update circle position
    xPos += Vx
    yPos += Vy
    for i in range(10):
        if pelletBag[i].collide(xPos, yPos) == True:
            tail.append(TailSeg(oldX, oldY))
        if pelletBag[i].collide(xPos2, yPos2) == True:
            tail2.append(TailSeg(oldX2, oldY2))
    if xPos > 392 or yPos > 392:
        doExit = True
    if xPos2 > 392 or yPos2 > 392:
        doExit = True
    for i in range(len(tail2)):
        if tail2[i].collide(xPos, yPos) == True:
            print("p1 hit p2's tail!")
            doExit = True
    for i in range(len(tail)):
        if tail[i].collide(xPos2, yPos2) == True:
            print("p2 hit p1's tail!")
            doExit = True
        
#render section ----
    screen.fill((255,255,255)) #wipe screen
    for i in range(10):
        pelletBag[i].draw()
    for i in range(len(tail)):
        tail[i].draw()
    for i in range(len(tail2)):
        tail2[i].draw()
    pygame.draw.circle(screen,(200,0,200), (xPos, yPos), 12)
    pygame.draw.circle(screen,(100,30,10), (xPos2, yPos2), 12)
    pygame.display.flip()
   
    
#End of game loop ----

pygame.quit()
