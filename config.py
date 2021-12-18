# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

"""
blockLables is a tuple of the labels for each block of trial types
to be scanned.  There can be identical block where the same trial types 
are scanned multiple times, e.g.
blockLabels = ("[block", "[block", "[block")
the types file will only have one block which is rescanned
or hetorgeneous blocks, e.g.,
blockLabels = ("[block1","[block2","[block3")
The types file will have three blocks each starting with a distinct label, e.g.,
[block1]
"""
#set practiceLabels = [] when you do not want practice trials
practiceLables = ("[practice",)
blockLables = ("[block1","[block2","[block3")
blockRepeat = 2
lineSpacing = 15
fieldSize = (80, 700)
bg = (255,255,255)
fg = (0,0,0)
loopDelay = 40
xDotDistance = 300
yDotDistance = 250
if sys.platform == 'darwin':
    dbuf = True
else:
    dbuf = True

dataFileHeader = (";Col -- 1 Condition 0 = Contrast, 1 = center, 2 = perif, 3 = no lines\n",\
    ";Col 2 -- Top slope\n",\
    ";Col 3 -- Mid slope\n",\
    ";Col 4 -- Bottom Slope (720 signifies no lines)\n",\
    ";Col 5 -- Orientation (not used)\n",\
    ";Col 6 -- Gap (not used)\n",\
    ";Col 7 -- pse in distance in pixels above or below the standard.\n",\
    ";Col 8 -- pse in degrees departure from horizontal.\n",\
    ";Col 9 -- Number of adjustments, i.e., up and down arrows typed.\n")

# file with instructions
instructions = "flank.txt"
trialParms = 'flank.ini'
splash = 'kozzoll.jpg'
