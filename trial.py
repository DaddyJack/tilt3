# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import config
import random
import field
import sys
import math

class Trial:
    """
    initializes, gives, and saves data for a trial
    """
    def __init__(self, args):
        """
        set parameters and zero response data
        """
        self.trial_type = int(args[0])
        self.top_degree = int(args[1])
        self.mid_degree = int(args[2])
        self.bottom_degree = int(args[3])
        self.orientation = int(args[4])
        self.gap = int(args[5])
        self.n_adjust = 0
        self.pse = 0.0
        self.standard = 0

    def give(self, screen, background):
        """
        give a trial
        """

        background.fill(config.fg)
        colorKey = [0, 0, 2]
        screen.set_colorkey(colorKey, RLEACCEL)
        background.set_colorkey(colorKey, RLEACCEL)
        ovRect = background.get_rect().inflate(-2,-2)
        ovRect.move_ip(-1,-1)
        pygame.draw.ellipse(background, config.bg, ovRect, 0)
        screen.blit(background, (0,0))

        # Make sprites that are the fields of lines
        fCenter = screen.get_rect().center
        fields = pygame.sprite.Group()
        # + 90 degrees to make relative to vertical
        # offset on x dimension for vertical
        if self.top_degree < 710:
            top = field.Field(self.top_degree + 90, (fCenter[0] - config.fieldSize[0], fCenter[1]), config.fieldSize, config.lineSpacing)
            fields.add(top)
        if self.mid_degree < 710:
            mid = field.Field(self.mid_degree + 90, (fCenter[0], fCenter[1]), config.fieldSize, config.lineSpacing)
            fields.add(mid)
        if self.bottom_degree < 710:
            bottom = field.Field(self.bottom_degree +90, (fCenter[0] + config.fieldSize[0], fCenter[1]), config.fieldSize, config.lineSpacing)
            fields.add(bottom)
    # Change to vertical xstart not ystart
        if random.randint(0, 1) == 0:
            xstart = fCenter[0] + random.randint(10, 25)
        else:
            xstart = fCenter[0] - random.randint(10, 25)
        # Make sprites that are the dots to allign
        # Change to vertical
        stan = field.Dot((fCenter[0], fCenter[1] - config.yDotDistance / 2))
        var = field.Dot((xstart , fCenter[1] + config.yDotDistance / 2))
        dots = pygame.sprite.Group(stan, var)
        screen.blit(background, (0, 0))
        running = 1
        cnt = 0
        pygame.event.clear()

        while running:
            pygame.time.delay(config.loopDelay)
            if config.dbuf == True:
                screen.blit(background, (0, 0))
            else:
                fields.clear(screen, background)
                dots.clear(screen, background)

            fields.update()
            dots.update()

            fields.draw(screen)
            dots.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                # print event
                pygame.time.wait(20)
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_q:
                        running = 0
                        sys.exit(1)
                    elif event.key == K_LEFT:
                        cnt = cnt + 1
                        var.x_dir = -1
                    elif event.key == K_RIGHT:
                        var.x_dir = 1
                        cnt = cnt + 1
                    elif event.key == K_RETURN:
                        running = 0
                elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        var.x_dir = 0
                    elif event.key == K_RIGHT:
                        var.x_dir = 0

        self.pse = (var.rect.centerx - fCenter[0])
        self.n_adjust = cnt
        screen.blit(background, (0,0))
        pygame.display.update()

    def printOut(self):
        return "{} {} {} {} {} {} {} {} {}\n".format(self.trial_type, self.top_degree, \
            self.mid_degree, self.bottom_degree, self.orientation, self.gap, self.pse, \
                math.degrees(math.atan2(self.pse,config.yDotDistance)), self.n_adjust)
