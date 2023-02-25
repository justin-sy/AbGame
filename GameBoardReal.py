# copyright: Yongjian Feng
import math
import pygame
import sys
from pygame.locals import *
from math import cos, sin, pi, fabs

# pygame:
# https://ryanstutorials.net/pygame-tutorial/pygame-shapes.php


class GameBoardReal:
    STATE_FLYING = 1
    STATE_EXPOSE = 60
    STATE_PENDING = 0

    start_button_x = 10
    start_button_y = 10
    start_button_w = 120
    start_button_h = 20

    def __init__(self, gb_config):
        self.gbConfig = gb_config
        self.win = None
        self.fpsClock = pygame.time.Clock()
        self.counter = self.STATE_PENDING
        self.gfont = None

    def init(self):
        pygame.display.set_caption(self.gbConfig.title)
        self.win = pygame.display.set_mode((self.gbConfig.win_w, self.gbConfig.win_h))
        pygame.font.init()
        self.gfont = pygame.font.SysFont('Comic Sans MS', 20)

    def set_flying(self):
        self.counter = self.STATE_FLYING

    def set_expose(self):
        self.counter = self.STATE_EXPOSE

    def start(self):
        # get into an endless loop
        done = False
        while not done:
            # handle events
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    print("Exit")
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    # user click. check if inside button area
                    if self.start_button_x <= mouse[0] <= self.start_button_x + self.start_button_w and \
                       self.start_button_y <= mouse[1] <= self.start_button_y + self.start_button_h:
                        if self.gbConfig.updater and self.counter == self.STATE_PENDING:
                            print('New Game')
                            self.gbConfig.updater.start_new_game()
                            continue
                    else:
                        dist = GameBoardReal.distance(mouse, (0, self.gbConfig.data.ground_y))
                        if mouse[1] < self.gbConfig.data.ground_y and dist < 100:
                            print('Launching')
                            self.gbConfig.data.launched = True
                            
                            # launching, update
                            # let the updater compute the good scale
                            self.gbConfig.data.v_x = mouse[0]/50.0
                            self.gbConfig.data.v_y = (self.gbConfig.data.ground_y - mouse[1])/50.0
                            self.gbConfig.data.n_x = mouse[0]
                            self.gbConfig.data.n_y = mouse[1]
                            self.set_flying()
                        else: 
                            self.gbConfig.data.launched = False
                        continue
                      

            # call the updater to do some update
            if self.gbConfig.updater:
                self.gbConfig.updater.update(self.gbConfig.data)

            self.counter = self.check_hit_or_miss(self.counter)
            # re-render
            self.draw_background()
            if self.counter > 2:
                # animate exposure effect
                self.counter -= 1
                scale = (self.STATE_EXPOSE - self.counter)/(self.STATE_EXPOSE - 2) + 1
                color_scale = (self.counter - 2)/(self.STATE_EXPOSE - 2)
                self.draw_virus(scale, color_scale)
                if self.counter == 2:
                    self.gbConfig.data.vir_x = -1
                    self.counter = self.STATE_PENDING
            else:
                self.draw_foreground()

            pygame.display.update()
            # tick the timer for next iteration
            self.fpsClock.tick(self.gbConfig.fps)

    def draw_background(self):
        self.win.fill(self.gbConfig.bg_color)

        # draw the start button
        self.draw_start_button()
        # draw launch
        self.draw_launch_area()
        # draw the horizontal line
        y = self.gbConfig.data.ground_y
        pygame.draw.line(self.win, (190, 190, 190), (0, y), (self.gbConfig.data.w, y), 2)

        # draw a tree
        x = self.gbConfig.data.w*0.76
        self.draw_tree(x, 110, 60)
        x = self.gbConfig.data.w*0.85
        self.draw_tree(x, 200, 100)
        x = self.gbConfig.data.w*0.95
        self.draw_tree(x, 150, 80)

    def draw_launch_area(self):
        sz = 100
        pygame.draw.arc(self.win, (0, 0, 0), [-sz/2, self.gbConfig.data.ground_y-sz/2, sz, sz], 0, pi/2, 3)

    def draw_start_button(self):
        # draw start button
        pygame.draw.rect(self.win, (0, 200, 0),
                         [self.start_button_x, self.start_button_y, self.start_button_w, self.start_button_h])
        text = self.gfont.render("Start New Game", False, (0, 0, 0))
        self.win.blit(text, (self.start_button_x, self.start_button_y))

    def draw_tree(self, x, h=100, w=60):
        # always start from ground_y
        # trunk to be half of h
        y = self.gbConfig.data.ground_y
        y1 = y - h/2
        # trunk
        pygame.draw.line(self.win, (0, 125, 0), (x, y), (x, y1), 6)
        # first layer
        y = y1 + 3
        x1 = x - w/2
        x2 = x + w/2
        y1 = y - 0.3*h
        pygame.draw.polygon(self.win, (0, 200, 0), ((x1, y), (x2, y), (x, y1)))
        # second layer
        y = y1 + 3
        x1 = x - 0.3*w
        x2 = x + 0.3*w
        y1 = y - 0.2*h
        pygame.draw.polygon(self.win, (0, 230, 0), ((x1, y), (x2, y), (x, y1)))

    def draw_foreground(self):
        self.draw_virus()
        if self.counter == self.STATE_FLYING:
            self.draw_needle()

    def draw_needle(self):
        x1 = self.gbConfig.data.n_x - 3
        y1 = self.gbConfig.data.n_y
        rect = pygame.Rect(x1, y1, 6, 10)
        pygame.draw.rect(self.win, (0, 0, 0), rect, 2)

        x = self.gbConfig.data.n_x - 1
        y = self.gbConfig.data.n_y + 8
        y1 = y + 10
        pygame.draw.line(self.win, (0, 0, 0), (x, y), (x, y1), 2)

        x = self.gbConfig.data.n_x - 1
        y = self.gbConfig.data.n_y
        y1 = y - 8
        pygame.draw.line(self.win, (0, 0, 0), (x, y), (x, y1), 4)

        y = y1
        x1 = self.gbConfig.data.n_x - 3
        x2 = self.gbConfig.data.n_x + 2
        pygame.draw.line(self.win, (0, 0, 0), (x1, y), (x2, y), 1)

    def draw_virus(self, scale=1, color_scale=1):

        if self.gbConfig.data.vir_x < 0:
            # don't draw. virus position is not set yet.
            return
        g_b = (1 - color_scale)*255
        red1 = (1 - color_scale)*55 + 200
        red2 = (1 - color_scale)*105 + 150

        y = self.gbConfig.data.vir_y
        x = self.gbConfig.data.vir_x
        r = self.gbConfig.data.vir_r*scale
        pygame.draw.circle(self.win, (red1, g_b, g_b), (x, y), r)

        # draw ticks
        delta = 0.1
        for i in range(0, 8):
            angle = i*2*pi/8
            r1 = r + r/8
            x1 = r*cos(angle) + x
            y1 = r*sin(angle) + y

            x2 = r1*cos(angle) + x
            y2 = r1*sin(angle) + y
            pygame.draw.line(self.win, (red2, g_b, g_b), (x1, y1), (x2, y2), 3)

            x3 = r1*cos(angle - delta) + x
            y3 = r1*sin(angle - delta) + y

            x4 = r1*cos(angle + delta) + x
            y4 = r1*sin(angle + delta) + y
            pygame.draw.line(self.win, (red2, g_b, g_b), (x3, y3), (x4, y4), 2)

        # draw more ticks
        r2 = r/2
        for i in range(0, 4):
            angle = i*2*pi/4
            x1 = r2*cos(angle - 2*delta) + x
            y1 = r2*sin(angle - 2*delta) + y

            x2 = r2*cos(angle + 2*delta) + x
            y2 = r2*sin(angle + 2*delta) + y
            pygame.draw.line(self.win, (red2, g_b, g_b), (x1, y1), (x2, y2), 3)

    # private methods
    def check_hit_or_miss(self, counter):
        if counter == self.STATE_FLYING:
            if self.gbConfig.data.n_y >= self.gbConfig.data.ground_y - self.gbConfig.data.vir_r:
                if self.gbConfig.data.n_y < self.gbConfig.data.ground_y:
                    if fabs(self.gbConfig.data.n_x - self.gbConfig.data.vir_x) < self.gbConfig.data.vir_r:
                        return self.STATE_EXPOSE
            elif self.gbConfig.data.n_y > self.gbConfig.data.ground_y or self.gbConfig.data.n_x > self.gbConfig.win_w:
                self.gbConfig.data.n_x = -1
                return self.STATE_PENDING
        return counter

    @staticmethod
    def distance(p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1] - p2[1])**2)