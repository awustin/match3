import os
import pygame
from pygame import transform
import random as ran
import math

PROJECT_FOLDER = os.path.dirname(os.path.abspath(os.path.curdir))
EFFECTS_FILE = os.path.join(PROJECT_FOLDER, 'assets/images')
MAX_STEPS = 250
# --- DIZZY SPARKS THAT GO UP ^*¨^*¨^*¨^*¨*
SPARK_WEAK = pygame.image.load(f'{EFFECTS_FILE}/small_spark.png')
SP_MAX = 1/5
SP_FACTOR = 0.96
ACC_WEAK = pygame.Vector2(0, -1/100000)
ACC_WEAK_FACTOR = 0.3


class AlignmentSparkles():
    def __init__(self):
        self.__run = False
        self.__end = False
        self.__init_effect()
        self.__image_weak = SPARK_WEAK
        self.__step = 0
        self.__particles_groups = []

    def __init_effect(self):
        global SPARK_WEAK
        SPARK_WEAK.convert()

    def run_particles(self):
        self.__run = True
        self.__end = False

    def is_running(self):
        return self.__run

    def has_ended(self):
        return self.__end

    def get_image(self):
        return self.__image

    def __ran_radial_vec(self):
        ran_alfa = ran.random()*2*math.pi
        x = math.cos(ran_alfa)
        y = math.sin(ran_alfa)
        return pygame.Vector2(x, y)

    def __decide_random_type(self):
        return ran.randint(0, 1)

    def __acc_weak(self, step):
        return ACC_WEAK*(1 - 2*ACC_WEAK_FACTOR)

    def __reduce_size(self, step):
        s = 1 - step/300
        if s <= 0:
            return step/400
        return 1.2*s

    def generate_particles(self, origins):
        'Pass a list with all the origins of particles for sparkling effect'
        for i in range(len(origins)):
            self.__particles_groups.append({})
            self.__particles_groups[i]['count'] = ran.randint(10, 20)
            self.__particles_groups[i]['group'] = []
            for j in range(self.__particles_groups[i]['count']):
                particle = {}
                particle['pos'] = origins[i]
                particle['size'] = 1
                particle['speed'] = self.__ran_radial_vec() * SP_MAX
                particle['type'] = self.__decide_random_type()
                self.__particles_groups[i]['group'].append(particle)

    def __draw_sparkles_up(self, display):
        step = self.__step
        for i in range(len(self.__particles_groups)):
            for particle in self.__particles_groups[i]['group']:
                if particle['type'] == 0:
                    acceleration = self.__acc_weak(step)
                    particle['pos'] = particle['pos'] + \
                        particle['speed']*step + \
                        acceleration*step**2
                    particle['speed'] = particle['speed'] + \
                        acceleration*step
                    particle['speed'] *= SP_FACTOR
                    particle['size'] = self.__reduce_size(step)
                    rect = pygame.Rect(SPARK_WEAK.get_rect())
                    rect.center = particle['pos']
                    rect.width = rect.width * particle['size']
                    rect.height = rect.height * particle['size']
                    image = transform.scale(SPARK_WEAK,
                                            (rect.width, rect.height)
                                            )
                    display.blit(image, rect)

    def update(self, display):
        if self.__end:
            self.__particles_groups = []
            return
        if self.__run:
            self.__draw_sparkles_up(display)
            self.__step += 1
            if self.__step == MAX_STEPS:
                self.__run = False
                self.__end = True
        else:
            self.__step = 0
