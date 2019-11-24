# Clase ficha:
# Agrupa el tipo de ficha.
# Agrupa los estados de una ficha:
# Ninguno, alineada, seleccionada
# Además su animación: gravedad
import pygame
from tipoficha import TipoFicha

GRAVEDAD = 2


class Ficha(pygame.sprite.Sprite):
    def __init__(self, idTipo=0, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.__seleccionada = False
        self.__intercambia = False
        self.__cae = False
        self.__tipo = TipoFicha(idTipo)
        self.image = self.__tipo.getImage()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.t = 0
        self.v_inicial = 0
        self.y_inicial = self.rect.centery
        self.y_final = self.y_inicial + 100
        self.equilibrio = self.rect.centery
        self.__celdaDestino = None
        self.__celdaOrigen = None

#  //
#  Métodos get-set
#  //

    def getSeleccionada(self):
        return self.__seleccionada

    def setSeleccionada(self, valor):
        '''Asigna valor booleano\n
        y setea el color correspondiente'''
        self.__seleccionada = valor

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

    def setCae(self, valor):
        self.__cae = valor
    
    def estaCayendo(self):
        return self.__cae

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
        self.equilibrio = y

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

    def equals(self, otraFicha):
        return self.__tipo.getId() == otraFicha.getTipoInt()

    def update(self, ventana):
        '''Caida: hasta una posición final'''
        if(self.estaCayendo() and self.rect.centery < self.y_final):
            self.grav(self.t)
            self.t += 1
        elif(self.__seleccionada):
            pass
            # Animacion de seleccionada
        else:
            self.t = 0
            self.v_inicial = 0
            self.y_inicial = self.rect.centery
            self.__cae = False
        ventana.blit(self.image, self.rect)

    def grav(self, t):
        y = self.y_inicial + self.v_inicial*t + 0.5*GRAVEDAD*t
        self.rect.centery = y