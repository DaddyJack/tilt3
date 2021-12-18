#!/usr/bin/env python
from pyepl.locals import *
import random
import os, pygame
from pygame.locals import *



#functions to create our resources
def load(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image#, image.get_rect()
def makeField(degree, size, lineSep):
    imSize = [1500, 1500]
    image = pygame.Surface(imSize)
    image.fill([0, 0, 0])
    for y in range(1, imSize[1], lineSep):
            pygame.draw.line(image, [255,255,255], [0, y], [imSize[0], y])
    colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)
    slant = pygame.transform.rotate(image, degree)

    chopRect = pygame.Rect( (600 + random.randint(0, 30), 600), size)

    cslant = pygame.Surface(size)
    cslant = cslant.convert()
    cslant.fill((0, 0, 0))
    cslant.blit(slant, (0,0), chopRect)
    return Image(cslant)


class Field(pygame.sprite.Sprite):
	"""This class is for the players ship"""
	field_of_lines = False
	def __init__(self, angle, loc, size):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		
		if Field.field_of_lines == False:
			Field.field_of_lines = make_image_lines()
		slant = pygame.transform.rotate(Field.field_of_lines, angle)

		chopRect = pygame.Rect( (600 + random.randint(0, 30), 600), size)

		cslant = pygame.Surface(size)
		cslant = cslant.convert()
		cslant.fill((0, 0, 0))
		cslant.blit(slant, (0,0), chopRect)
		self.image = cslant
		self.rect = cslant.get_rect()
		scr_width, scr_height = pygame.display.get_surface().get_size()
		self.rect.center = loc

#		 print "width and height", pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()
def makeDot():
    imSize = [10, 10]
    image = pygame.Surface(imSize)

    image.fill([0, 0, 0])
    pygame.draw.circle(image,[255,255,255],(5,5),4,0)
    
    return Image(image)

    
class Dot(pygame.sprite.Sprite):
    """This class is for the players ship"""
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        imSize = [10, 10]
        image = pygame.Surface(imSize)
        image.fill([0, 0, 0])

        pygame.draw.circle(image, [255, 255, 255], (5, 5), 4, 0)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = loc
        self.y_dir = 0
    def update(self):
        self.rect.move_ip((0, self.y_dir))
            
def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
    """
    # Fill background
    exp = Experiment(use_eeg = False, fullscreen = False)

    exp.parseArgs()
    exp.setup()
    exp.setBreak()

    video = VideoTrack("video")
    kt = KeyTrack("key")
    bc = ButtonChooser(Key('Z'), Key('/'))
    pc = PresentationClock()
    video.clear("black")

    config = exp.getConfig()
    
    top = makeField(75, (150, 300), config.lineSep)
    mid = makeField(105, (150, 300), config.lineSep)
    bottom = makeField(75, (150, 300), config.lineSep)
    dot = makeDot()
    top.load()
    bottom.load()
    mid.load()
    dot.load()
    shown1 = video.showProportional(top, .5, .25)
    
    shown2 = video.show(mid, 400, 400)
    shown3 = video.show(bottom, 400, 600)
    dotshown = video.showProportional(dot, .5,.5)
    video.showProportional(Text('Duh'), .5, .5)
    video.updateScreen(pc)
    pc.delay(4000)
    video.unshow(shown1)
    video.updateScreen(pc)
    pc.delay(1000)


   
#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
