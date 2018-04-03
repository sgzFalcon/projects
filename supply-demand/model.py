import pygame
import random

random.seed(1235)

class Agent:
    def interactWith(self, other):
        if self.apple == 0 and other.apple == 1: 
            # maybe buy from other
            bid = self.price*(1-self.factor)
            trade(bid, self, other, bid >= other.price*(1+other.factor))
            if bid < other.price*(1+self.factor):
                self.factor /= 1.5
            else:
               self.factor = 0.9
        elif self.apple == 1 and other.apple == 0: 
            # maybe sell to other
            ask = self.price*(1+self.factor)
            trade(ask, other, self, ask <= other.price*(1-other.factor))
            if ask >= other.price*(1-self.factor):
                self.factor /= 1.5
            else:
               self.factor = 0.9 

    def __init__(self, initialApples, reservationPrice):
        self.apple = initialApples
        self.price = reservationPrice
        self.factor = 0.9

def trade(price, buyer, seller, success):
    global iter
    iter += 1
    if success:
        line(green, buyer.price, seller.price)
        dot(green, price, 7)
        buyer.apple += 1
        seller.apple -= 1
        print("price: ", round(price, 3), 
              " seller: ", seller.price, 
              " buyer: ", buyer.price)
    else:
        dot(gray, price)
    dot(blue, buyer.price)
    dot(red, seller.price)
    pygame.display.flip()

def dot(color, price, r=4):
    pygame.draw.circle(screen, color, (getX(),getY(price)), r)

def line(color, p0, p1):
    x = getX()
    pygame.draw.line(screen, color, (x,getY(p0)), (x,getY(p1)), 2)

def getX():
    return round(iter*W/(nIter+1.))

def getY(price):
    # note (0,0) is TOP left of window
    return round(H - H*price/(maxPrice+1.))

W = 1200; H = 500; nIter = 500; maxPrice = 24

# initialize graphics window:

pygame.init()
screen = pygame.display.set_mode([W, H])
pygame.display.set_caption("Supply and Demand")
white = [255, 255, 255]; gray = [128, 128, 128]
red = [255, 0, 0]; blue = [0, 0, 255]
green = [0, 200, 0]; yellow = [255, 255, 0]
screen.fill(white)
pygame.draw.rect(screen, yellow, (0,getY(6),W,getY(4.5)-getY(6)))
pygame.display.flip()

# initialize agents:

seq = [] # one-dimensional list of Agents

for p in [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]:
    seq.append(Agent(0, p)) # buyers
for p in [0.2, 0.5, 1.5, 2.5, 4.5, 8.5, 16]:
    seq.append(Agent(1, p)) # sellers

# main loop:

iter = 0
done = False
clock = pygame.time.Clock()
N = len(seq)
while done==False:
    if iter <= nIter:
        a = seq[random.randint(0,N-1)]
        b = seq[random.randint(0,N-1)]
        a.interactWith(b)
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
pygame.quit()