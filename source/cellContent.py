import pygame
import controllers.spritesData as spritesData
import controllers.scoreData as scoreData

GRAVITY = 5
SWAP_SPEED = 7


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ---- CellContent Class ------------------------------------------ #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class CellContent(pygame.sprite.Sprite):
    def __init__(self, cell_class):
        pygame.sprite.Sprite.__init__(self)
        self.__load_cell_class(cell_class)
        self.__init_animation_parameters()
        self.__load_sprite()
        self.__init_physics()

#  //
#  Initialization
#  //
    def __load_cell_class(self, cell_class):
        if cell_class == 0:
            self.__class = 'default'
        else:
            self.__class = cell_class
        return

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
        self._dropped = False
        self.t = 0
        self.v_initial = 0
        self.y_initial = self.rect.centery
        self.y_final = self.y_initial + 100
        self._origin_cell = None
        self._target_cell = None

#  //
#  Get - Set Methods
#  //
    def get_class(self):
        return self.__class

    def set_initial_speed(self, speed):
        if(not self.is_falling()):
            int(speed)
            self.v_initial = speed

    def set_target_position(self, y_final):
        if(not self.is_falling()):
            self.y_final = y_final

    def set_center_pos(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def get_center_pos(self):
        return self.rect.center

    def set_target_cell(self, cell):
        self._target_cell = cell

    def get_target_cell(self):
        return self._target_cell

    def set_origin_cell(self, cell):
        self._origin_cell = cell

    def get_origin_cell(self):
        return self._origin_cell

#  //
#  Status methods
#  //
    def is_falling(self):
        return self._dropped

    def set_dropped(self, value):
        self._dropped = value

    def equals(self, other):
        return self.__class == other.get_class()

#  //
#  Physics methods
#  //
    def __gravity(self, t):
        y = self.y_initial + self.v_initial*t + 0.5*GRAVITY*t
        self.rect.centery = y

    def __cuadratic_glide(self, t):
        '''Gets module and direction'''
        delta = self.p2 - self.p1
        if(delta == (0, 0)):
            self.set_swapping(False)
            return
        if(delta.x != 0):
            direcc = pygame.math.Vector2(delta.x/abs(delta.x),
                                         delta.y/abs(delta.x))
        else:
            direcc = pygame.math.Vector2(0, delta.y/abs(delta.y))
        swap_vector = SWAP_SPEED * direcc
        t_swap = 2 * delta.magnitude() / swap_vector.magnitude()
        acceleration_swap = (-swap_vector) / t_swap
        p = self.p1 + swap_vector * t + acceleration_swap * 0.5 * t**2
        if(t == int(t_swap)):
            self.set_swapping(False)
        self.rect.centerx = p.x
        self.rect.centery = p.y

#  //
#  Update methods
#  //
    def dropped_update(self):
        if(self.is_falling() and self.rect.centery < self.y_final):
            self.__gravity(self.t)
            self.t += 1

    def selected_update(self):
        if(self.is_selected()):
            pass

    def swapping_update(self):
        if(self.is_swapping()):
            if(self.t == 0):
                self.p1 = pygame.math.Vector2(
                          *self._origin_cell.get_center_pos())
                self.p2 = pygame.math.Vector2(
                          *self._target_cell.get_center_pos())
            self.__cuadratic_glide(self.t)
            self.t += 1

    def reset_physics(self):
        self.t = 0
        self.v_initial = 0
        self.y_initial = self.rect.centery
        self._dropped = False

    def __nextFrame(self):
        self.__current_step = self.__current_step + self.__anim_speed
        pointer = int(self.__current_step)
        if(pointer == self.__num_frames):
            self.__current_step = 0
            pointer = 0
        self.__current_frame = pointer
        self.image = self.__frames[self.__current_frame]

    def update(self):
        self.__nextFrame()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ---- Chip Class ------------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Chip(CellContent):
    def __init__(self, cell_class=0):
        super().__init__(cell_class)
        self.__load_flavor_values()
        self.set_selected(False)

# //
# Status methods
# //
    def is_selected(self):
        return self.__selected

    def is_swapping(self):
        return self.__swap

    def set_selected(self, flag):
        self.__selected = flag
        self._dropped = False
        self.__swap = False

    def set_dropped(self, flag):
        self.__selected = False
        self._dropped = flag
        self.__swap = False

    def set_swapping(self, flag):
        self.__selected = False
        self._dropped = False
        self.__swap = flag

# //
# Scoring methods
# //
    def __load_flavor_values(self):
        self.__base_value = scoreData.get_base_value(key=super().get_class())
        self.__fruity = scoreData.get_fruity(key=super().get_class())
        self.__bitter = scoreData.get_bitter(key=super().get_class())
        self.__rotten = scoreData.get_rotten(key=super().get_class())

    def get_base_value(self):
        return self.__base_value

    def get_fruity(self):
        return self.__fruity

    def get_bitter(self):
        return self.__bitter

    def get_rotten(self):
        return self.__rotten

# //
# Update
# //
    def update(self, display):
        is_swapping = self.is_swapping()
        is_selected = self.is_selected()
        is_falling = self.is_falling()
        self.dropped_update()
        self.selected_update()
        self.swapping_update()
        if(not is_swapping and
           not is_selected and
           (not is_falling or self.rect.centery >= self.y_final)):
            self.reset_physics()
            self.__swap = False
            self.__selected = False
        super().update()
        display.blit(self.image, self.rect)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ---- UnbreakableBlock Class ------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class UnbreakableBlock(CellContent):

    def __init__(self):
        super().__init__(cell_class=-2)

#  //
#  Position
#  //
    def get_center_pos(self):
        return self.rect.center

#  //
#  Update
#  //
    def update(self, display):
        is_falling = self.is_falling()
        self.dropped_update()
        if(not is_falling or self.rect.centery >= self.y_final):
            self.reset_physics()
        super().update()
        display.blit(self.image, self.rect)
