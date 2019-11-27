# Clase ficha:
# Agrupa el tipo de ficha.
# Agrupa los estados de una ficha:
# Ninguno, alineada, seleccionada
# Además su animación: gravedad
import pygame
from tipoficha import TipoFicha

GRAVEDAD = 2
V_INTERCAMBIO = 6


class Ficha(pygame.sprite.Sprite):
    def __init__(self, idTipo=0, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.__seleccionada = False
        self.__cae = False
        self.__intercambia = False
        self.__tipo = TipoFicha(idTipo)
        self.image = self.__tipo.getImage()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.t = 0
        self.v_inicial = 0
        self.y_inicial = self.rect.centery
        self.y_final = self.y_inicial + 100
        self.__celdaDestino = None
        self.__celdaOrigen = None

#  //
#  Métodos get-set
#  //

    def getTipo(self):
        return self.__tipo

    def getTipoInt(self):
        '''Devuelve el numero entero que identifica\n
        al tipo de ficha'''
        return self.__tipo.getId()

    def setTipo(self, tipo):
        '''Asigna el tipo\n
        y setea el color correspondiente'''
        self.__tipo = tipo

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

    def setSeleccionada(self, valor):
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

    def equals(self, otraFicha):
        return self.__tipo.getId() == otraFicha.getTipoInt()

    def update(self, ventana):
        '''Caida: hasta una posición final'''
        if(self.estaCayendo() and self.rect.centery < self.y_final):
            self.grav(self.t)
            self.t += 1
        elif(self.estaSeleccionada()):
            pass
            # Animacion de seleccionada
        elif(self.estaIntercambiando()):
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
        ventana.blit(self.image, self.rect)

    def grav(self, t):
        y = self.y_inicial + self.v_inicial*t + 0.5*GRAVEDAD*t
        self.rect.centery = y

    def movCuadratico(self, t):
        # Obtengo direccion y modulo de v_intercambio
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
