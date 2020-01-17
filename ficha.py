# Clase ficha:
# Agrupa los estados de una ficha:
# Ninguno, alineada, seleccionada
# Además su animación: gravedad y sprite
import pygame
import spritesData

GRAVEDAD = 1.2
V_INTERCAMBIO = 7


class Ficha(pygame.sprite.Sprite):
    __frames = []
    __num_frames = 0
    __current_frame = 0
    __current_step = 0
    __anim_speed = 0

    def __init__(self, token_class=0):
        pygame.sprite.Sprite.__init__(self)
        self.__class = token_class
        self.__load_sprite()
        self.__init_physics()
        self.set_seleccionada(False)
#  //
#  Inicialización
#  //

    def __load_sprite(self):
        if self.__class == 0:
            self.__class = 'default'
        self.__frames = spritesData.get_animation_frames(key=self.__class)
        self.__num_frames = spritesData.get_num_frames(key=self.__class)
        self.__anim_speed = spritesData.get_anim_speed(key=self.__class)
        self.image = self.__frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def __init_physics(self):
        self.t = 0
        self.v_inicial = 0
        self.y_inicial = self.rect.centery
        self.y_final = self.y_inicial + 100
        self.__celdaDestino = None
        self.__celdaOrigen = None

#  //
#  Métodos get-set
#  //

    def get_class(self):
        '''Devuelve el numero entero que identifica\n
        a la clase de la ficha'''
        return self.__class

    def setVelocidadInicial(self, velocidad):
        '''En pixeles por frame'''
        if(self.estaCayendo()):
            print(f'La ficha está cayendo.'
                  'No se puede cambiar la velocidad inicial')
        else:
            int(velocidad)
            self.v_inicial = velocidad

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

    def setCeldaDestino(self, celda):
        self.__celdaDestino = celda

    def getCeldaDestino(self):
        return self.__celdaDestino

    def setCeldaOrigen(self, celda):
        self.__celdaOrigen = celda

    def getCeldaOrigen(self):
        return self.__celdaOrigen

# //
# Métodos para manipular el estado de la ficha
# //
    def estaSeleccionada(self):
        return self.__seleccionada

    def set_seleccionada(self, valor):
        '''Si valor es True, pone en True la bandera
        de "seleccionada" y las demás banderas en False.\n
        Si valor es False, pone todas en False'''
        if(valor):
            self.__seleccionada = valor
            self.__cae = False
            self.__intercambia = False
        else:
            self.__seleccionada = False
            self.__cae = False
            self.__intercambia = False

    def estaCayendo(self):
        return self.__cae

    def setCae(self, valor):
        '''Si valor es True, pone en True la bandera
        de "cae" y las demás banderas en False.\n
        Si valor es False, pone todas en False'''
        if(valor):
            self.__seleccionada = False
            self.__cae = valor
            self.__intercambia = False
        else:
            self.__seleccionada = False
            self.__cae = False
            self.__intercambia = False

    def estaIntercambiando(self):
        return self.__intercambia

    def setIntercambio(self, valor):
        '''Si valor es True, pone en True la bandera
        de "intercambia" y las demás banderas en False.\n
        Si valor es False, pone todas en False'''
        if(valor):
            self.__seleccionada = False
            self.__cae = False
            self.__intercambia = valor
        else:
            self.__seleccionada = False
            self.__cae = False
            self.__intercambia = False

    def equals(self, other):
        return self.__class == other.get_class()

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
                          *self.__celdaOrigen.getPosicionCentro())
                self.p2 = pygame.math.Vector2(
                          *self.__celdaDestino.getPosicionCentro())
            self.movCuadratico(self.t)
            self.t += 1
        else:
            self.t = 0
            self.v_inicial = 0
            self.y_inicial = self.rect.centery
            self.__cae = False
            self.__intercambia = False
            self.__seleccionada = False
        self.nextFrame()
        ventana.blit(self.image, self.rect)

    def grav(self, t):
        y = self.y_inicial + self.v_inicial*t + 0.5*GRAVEDAD*t
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

    def nextFrame(self):
        '''Avanza en el spritesheet'''
        self.__current_step = self.__current_step + self.__anim_speed
        pointer = int(self.__current_step)
        if(pointer == self.__num_frames):
            self.__current_step = 0
            pointer = 0
        self.__current_frame = pointer
        self.image = self.__frames[self.__current_frame]
