# Clase ficha:
# Agrupa los estados de una ficha:
# Ninguno, alineada, seleccionada
# Además su animación: gravedad y sprite
import pygame
import spritesData

GRAVITY = 1.2
V_INTERCAMBIO = 7


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ---- CellContent Class ------------------------------------------ #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class CellContent(pygame.sprite.Sprite):
    def __init__(self, cell_class):
        pygame.sprite.Sprite.__init__(self)
        self._load_cell_class(cell_class)
        self._init_animation_parameters()
        self._load_sprite()
        self._init_physics()

#  //
#  Initialization
#  //
    def _load_cell_class(self, cell_class):
        if cell_class == 0:
            self.__class = 'default'
        else:
            self.__class = cell_class
        return

    def _init_animation_parameters(self):
        self.__frames = []
        self.__num_frames = 0
        self.__current_frame = 0
        self.__current_step = 0
        self.__anim_speed = 0

    def _load_sprite(self):
        self.__frames = spritesData.get_animation_frames(key=self.__class)
        self.__num_frames = spritesData.get_num_frames(key=self.__class)
        self.__anim_speed = spritesData.get_anim_speed(key=self.__class)
        self.image = self.__frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def _init_physics(self):
        self._cae = False
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

    def setVelocidadInicial(self, velocidad):
        '''En pixeles por frame'''
        if(self.estaCayendo()):
            print(f'La ficha está cayendo.'
                  'No se puede cambiar la velocidad inicial')
        else:
            int(velocidad)
            self.v_initial = velocidad

    def setPosicionFinalCaida(self, y_final):
        if(self.estaCayendo()):
            print(f'La ficha está cayendo.'
                  'No se puede cambiar la posicion final')
        else:
            self.y_final = y_final

    def setPosicionCentro(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def getPosicionCentro(self):
        return self.rect.center

    def set_target_cell(self, celda):
        self._target_cell = celda

    def getCeldaDestino(self):
        return self._target_cell

    def set_origin_cell(self, celda):
        self._origin_cell = celda

    def getCeldaOrigen(self):
        return self._origin_cell

#  //
#  Status methods
#  //
    def is_falling(self):
        return self._cae

    def estaCayendo(self):
        return self._cae

    def setCae(self, value):
        self.__falling = value

    def equals(self, other):
        return self.__class == other.get_class()

#  //
#  Update method
#  //

    def __nextFrame(self):
        '''Avanza en el spritesheet'''
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
        self.set_seleccionada(False)

# //
# Status methods
# //
    def estaSeleccionada(self):
        return self.__seleccionada

    def set_seleccionada(self, valor):
        '''Si valor es True, pone en True la bandera
        de "seleccionada" y las demás banderas en False.\n
        Si valor es False, pone todas en False'''
        if(valor):
            self.__seleccionada = valor
            self._cae = False
            self.__intercambia = False
        else:
            self.__seleccionada = False
            self._cae = False
            self.__intercambia = False

    def setCae(self, valor):
        '''Si valor es True, pone en True la bandera
        de "cae" y las demás banderas en False.\n
        Si valor es False, pone todas en False'''
        if(valor):
            self.__seleccionada = False
            self._cae = valor
            self.__intercambia = False
        else:
            self.__seleccionada = False
            self._cae = False
            self.__intercambia = False

    def estaIntercambiando(self):
        return self.__intercambia

    def setIntercambio(self, valor):
        '''Si valor es True, pone en True la bandera
        de "intercambia" y las demás banderas en False.\n
        Si valor es False, pone todas en False'''
        if(valor):
            self.__seleccionada = False
            self._cae = False
            self.__intercambia = valor
        else:
            self.__seleccionada = False
            self._cae = False
            self.__intercambia = False

    def update(self, ventana):
        if(self.estaCayendo() and self.rect.centery < self.y_final):
            '''Caida: hasta una posición final'''
            self.grav(self.t)
            self.t += 1
        elif(self.estaSeleccionada()):
            '''Seleccionada'''
            pass
            # Animacion de seleccionada
        elif(self.estaIntercambiando()):
            '''Intercambio: se mueve hacia otra celda'''
            if(self.t == 0):
                self.p1 = pygame.math.Vector2(
                          *self._origin_cell.getPosicionCentro())
                self.p2 = pygame.math.Vector2(
                          *self._target_cell.getPosicionCentro())
            self.movCuadratico(self.t)
            self.t += 1
        else:
            self.t = 0
            self.v_initial = 0
            self.y_initial = self.rect.centery
            self._cae = False
            self.__intercambia = False
            self.__seleccionada = False
        super().update()
        ventana.blit(self.image, self.rect)

    def grav(self, t):
        y = self.y_initial + self.v_initial*t + 0.5*GRAVITY*t
        self.rect.centery = y

    def movCuadratico(self, t):
        '''Obtengo direccion y modulo de v_intercambio'''
        delta = self.p2 - self.p1
        if(delta == (0, 0)):
            self.setIntercambio(False)
            return
        if(delta.x != 0):
            direcc = pygame.math.Vector2(delta.x/abs(delta.x),
                                         delta.y/abs(delta.x))
        else:
            direcc = pygame.math.Vector2(0, delta.y/abs(delta.y))
        v_intercambio = V_INTERCAMBIO * direcc
        # Obtengo t_intercambio
        t_intercambio = 2 * delta.magnitude() / v_intercambio.magnitude()
        # Obtengo aceleracion
        a_intercambio = (-v_intercambio) / t_intercambio
        # Obtengo posicion
        p = self.p1 + v_intercambio * t + a_intercambio * 0.5 * t**2
        if(t == int(t_intercambio)):
            self.setIntercambio(False)
        self.rect.centerx = p.x
        self.rect.centery = p.y


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ---- UnbreakableBlock Class ------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class UnbreakableBlock(CellContent):

    def __init__(self):
        super().__init__(cell_class=-2)
        self.__falling = False

#  //
#  Position
#  //
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
    def __gravity(self, t):
        y = self.y_initial + self.v_initial*t + 0.5*GRAVITY*t
        self.rect.centery = y

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
        super().update()
        display.blit(self.image, self.rect)
