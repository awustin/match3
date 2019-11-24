# Clase ficha:
# Agrupa el tipo de ficha.
# Agrupa los estados de una ficha:
# Ninguno, alineada, seleccionada
# Además su animación: gravedad
import pygame
from tipoficha import TipoFicha
from customEnums import Colores
import math

GRAVEDAD = 2


class Ficha(pygame.sprite.Sprite):
    def __init__(self, idTipo=0, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.__seleccionada = False
        self.__intercambia = False
        self.__tipo = TipoFicha(idTipo)
        self.image = self.__tipo.getImage()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.t = 0
        self.t_rebote = 0
        self.v_inicial = 0
        self.y_inicial = self.rect.centery
        self.y_final = self.y_inicial + 100
        self.equilibrio = self.rect.centery
        self.__cae = False
        self.__lugaresQueCae = 0
        self.__celdaDestino = None
        self.__celdaOrigen = None
        self.__color = self.setColor()

#  //
#  Métodos get-set
#  //

    def getSeleccionada(self):
        return self.__seleccionada

    def setSeleccionada(self, valor):
        '''Asigna valor booleano\n
        y setea el color correspondiente'''
        self.__seleccionada = valor
        self.setColor()

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
        self.setColor()
    
    def setX(self, x):
        self.rect.x = x

    def setY(self, y):
        self.rect.y = y

    def setCae(self, valor):
        self.__cae = valor
    
    def estaCayendo(self):
        return self.__cae

    def setLugaresQueCae(self, valor):
        self.__lugaresQueCae = valor

    def lugaresQueCae(self):
        return self.__lugaresQueCae

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

    def setColor(self):
        '''Asigna el color a la ficha\n
        teniendo en cuenta si está seleccionada,\n
        alineada, o es No_especificada'''
        if(self.__seleccionada):
            self.__color = Colores.SELECCION.value
            return Colores.SELECCION.value
        else:
            self.__color = self.__tipo.getColor().value
            return self.__tipo.getColor().value

    def getColor(self):
        '''Devuelve el color de la ficha'''
        self.setColor()
        return self.__color

    def equals(self, otraFicha):
        return self.__tipo.getId() == otraFicha.getTipoInt()

    def update(self, ventana):
        '''Caida: hasta una posición final'''
        if(self.estaCayendo() and self.rect.centery < self.y_final):
            self.grav(self.t)
            self.t += 1
            self.equilibrio = self.rect.centery
        elif(self.__seleccionada):
            pass
            # Animacion de seleccionada
        else:
            self.t = 0
            self.t_rebote = 0
            self.v_inicial = 0
            self.y_inicial = self.rect.centery
            self.equilibrio = self.rect.centery
            self.__cae = False
        ventana.blit(self.image, self.rect)

    def grav(self, t):
        y = self.y_inicial + self.v_inicial*t + 0.5*GRAVEDAD*t
        self.rect.centery = y
    
    def rebote(self, t):
        y = self.equilibrio + (math.sin(0.01*2*t))*7*GRAVEDAD
        self.rect.centery = y