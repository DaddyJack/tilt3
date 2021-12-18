#!/usr/bin/env python

#Import Modules
import config
import random
import os, pygame
from pygame.locals import *

"""sprites used in the expeiment.  Field produces a rectangle of slanted lines.
Dot produces circles with a transparent background, Mask produces a tilted Mask.
load_image and make_image_lines are helper functions.
"""
def load_image(name, colorkey=None):
    """
    reads image files, e.g., jpeg or bmp, into an image object
    """
    #fullname = os.path.join('data', name)
    fullname = name
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
                colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image#, image.get_rect()
def make_image_lines(lineSpacing):
    #   creates an image with evenly spaced (by linSpacing) horizontal lines.
    imSize = [2000, 2000]
    image = pygame.Surface(imSize)
    image.fill(config.bg)
    for y in range(1, imSize[1], lineSpacing):
        pygame.draw.line(image, config.fg, [0, y], [imSize[0], y], 2)
    colorkey = (0,0,2)
    image.set_colorkey(colorkey, RLEACCEL)   
    return image
class Field(pygame.sprite.Sprite):
    """Field builds a grid of lines at a slant at "loc" position on the display
    """
    field_of_lines = False
    def __init__(self, angle, loc, size, lineSpacing):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        
        if Field.field_of_lines == False:
            Field.field_of_lines = make_image_lines(lineSpacing)
        slant = pygame.transform.rotate(Field.field_of_lines, angle)
        sr = slant.get_rect()
        fudge = random.randint(0, 30)
        chopRect = pygame.Rect((sr.centerx - size[0]/2 + fudge, sr.centery - size[1]/2), size)
        cslant = pygame.Surface(size)
        cslant.blit(slant, (0,0), chopRect)
        self.image = cslant
        self.rect = self.image.get_rect()
        self.rect.center = loc

class Dot(pygame.sprite.Sprite):
    """This class displays an alignment dot, which is moveable in the y axis"""
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        imSize = [10, 10]
        image = pygame.Surface(imSize)
        colorKey = [0, 0, 2]
        image.set_colorkey(colorKey, RLEACCEL)
        image.fill(colorKey)
        pygame.draw.circle(image, config.fg, ( 5, 5), 4, 0)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = loc
#       self.y_dir = 0
        self.x_dir = 0
    def update(self):
            self.rect.move_ip((self.x_dir, 0))
class Mask(pygame.sprite.Sprite):
    """Mask will mask out part of the grid of lines to display a rotated frame"""
    def __init__(self, loc, sizeOuter, sizeInner = 0, center = True):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.loc = loc
        image = pygame.Surface(sizeOuter)
        colorkey = [0,0,2]
        image.set_colorkey(colorkey, RLEACCEL)
        centerImage = image.get_rect().center
        if center == True:
        
            image.fill(colorkey)
            image = image.convert()
            boxLoc = (centerImage[0] - (sizeInner[0] / 2), centerImage[1] -(sizeInner[1] / 2))
            pygame.draw.rect(image, config.bg, (boxLoc, sizeInner))
        else:
            image.fill(config.bg)
            boxLoc = (centerImage[0] - (sizeInner[0] / 2), centerImage[1] -(sizeInner[1] / 2))            
            pygame.draw.rect(image, colorkey, (boxLoc, sizeInner))
        self.masterImage = image
        self.rect = image.get_rect()
        self.rect.center = loc
        self.y_dir = 0
        self.angle = 0.0
        self.image = pygame.transform.rotate(self.masterImage, self.angle)
    def update(self, dir, absolute=False):
        if absolute == False:
            newAngle = self.angle + dir
        else:
            newAngle = dir
        if newAngle != self.angle:
            self.angle = newAngle
            self.image = pygame.transform.rotate(self.masterImage, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = self.loc
     
def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    random.seed()
    pygame.init()
    screen = pygame.display.set_mode((1024, 768), FULLSCREEN)

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    colorKey = [0, 0, 2]
    screen.set_colorkey(colorKey, RLEACCEL)
    background.set_colorkey(colorKey, RLEACCEL)
    pygame.time.delay(1000)
    screen.blit(background, (0, 0))
    x = 0
    for i in range(100):
        x += 1
    left = Field(75, (512-150, 384), (150, 300), 30)
    mid = Field(105, (512, 384), (150, 300), 30)
    right = Field(75, (512+150, 384), (150, 300), 30)
    fields = pygame.sprite.Group(left,mid, right)
    fields.draw(screen)
    pygame.display.flip()

    pygame.time.delay(10000)



#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
