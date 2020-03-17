import pygame
import pygame.gfxdraw

MAX_STEPS = 30


class AligmentPowerRatio():
    def __init__(self):
        self.__run = False
        self.__end = False
        self.__origins = []
        self.__step = 0

    def run_power_ratio(self, origins):
        self.__origins = origins
        self.__run = True
        self.__end = False

    def is_running(self):
        return self.__run

    def has_ended(self):
        return self.__end

    def __ratius(self, step):
        return int(1 + step*1.5)

    def __width(self, step, r):
        w = r*(1 - step/30)*0.1
        return int(w)

    def __draw_power_ratio(self, display):
        step = self.__step
        for origin in self.__origins:
            ratius = self.__ratius(step)
            pygame.gfxdraw.aacircle(display, origin[0], origin[1],
                                    ratius, pygame.Color(100, 250, 0))

    def update(self, display):
        if self.__end:
            self.__particles_groups = []
            return
        if self.__run:
            self.__draw_power_ratio(display)
            self.__step += 1
            if self.__step == MAX_STEPS:
                self.__run = False
                self.__end = True
        else:
            self.__step = 0
