# Block Class
# Unbreakable
import pygame
import spritesData

GRAVITY = 5


class Block(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._is_broken = False


class Unbreakable(Block):

    def __init__(self):
        super(Block, self).__init__()
        self.__class = -2
        self.__init_animation_parameters()
        self.__load_sprite()
        self.__init_physics()
        self.__falling = False

#  //
#  Inicialization
#  //
    def __init_animation_parameters(self):
        self.__frames = []
        self.__num_frames = 0
        self.__current_frame = 0
        self.__current_step = 0
        self.__anim_speed = 0

    def __load_sprite(self):
        self.__frames = spritesData.get_animation_frames(key=self.__class)
        self.__num_frames = spritesData.get_num_frames(key=self.__class)
        self.__anim_speed = spritesData.get_anim_speed(key=self.__class)
        self.image = self.__frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def __init_physics(self):
        self.t = 0
        self.v_initial = 0
        self.y_initial = self.rect.centery
        self.y_final = self.y_initial + 100
        self.__origin_cell = None
        self.__target_cell = None
#  //
#  Status
#  //

    def set_falls(self):
        self.__falling = True

    def is_falling(self):
        return self.__falling

    def estaCayendo(self):
        return self.__falling

    def setCae(self, value):
        self.__falling = value

    def get_class(self):
        return self.__class
#  //
#  Position
#  //

    def setCeldaOrigen(self, cell):
        self.__origin_cell = cell

    def getCeldaOrigen(self):
        return self.__origin_cell

    def setCeldaDestino(self, cell):
        self.__target_cell = cell

    def getCeldaDestino(self):
        return self.__target_cell

    def setPosicionCentro(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def getPosicionCentro(self):
        return self.rect.center

    def setPosicionFinalCaida(self, y_final):
        if(not self.is_falling()):
            self.y_final = y_final

    def setVelocidadInicial(self, speed):
        if(not self.is_falling()):
            int(speed)
            self.v_initial = speed
#  //
#  Update
#  //

    def update(self, display):
        if(self.__falling and self.rect.centery < self.y_final):
            '''Falling: to a final position'''
            self.__gravity(self.t)
            self.t += 1
        else:
            self.t = 0
            self.v_initial = 0
            self.y_initial = self.rect.centery
            self.__falling = False
        self.__next_frame()
        display.blit(self.image, self.rect)

    def __gravity(self, t):
        y = self.y_initial + self.v_initial*t + 0.5*GRAVITY*t
        self.rect.centery = y

    def __next_frame(self):
        self.__current_step = self.__current_step + self.__anim_speed
        pointer = int(self.__current_step)
        if(pointer == self.__num_frames):
            self.__current_step = 0
            pointer = 0
        self.__current_frame = pointer
        self.image = self.__frames[self.__current_frame]
