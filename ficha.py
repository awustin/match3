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
        self.__alineada = False
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

    def getAlineada(self):
        return self.__alineada

    def setAlineada(self, valor):
        '''Asigna valor booleano\n
        y setea el color correspondiente'''
        if(valor):
            self.setColor()
        self.__alineada = valor
    
    def setX(self, x):
        self.rect.x = x

    def setY(self, y):
        self.rect.y = y

    def setCae(self, valor, y_final=100, v_inicial=0):
        if(valor):
            self.setPosicionFinalCaida(y_final)
            self.setVelocidadInicial(v_inicial)
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

# //
# Métodos para manipular el estado de la ficha
# //

    def setColor(self):
        '''Asigna el color a la ficha\n
        teniendo en cuenta si está seleccionada,\n
        alineada, o es No_especificada'''
        if(self.__alineada):
            self.__color = Colores.ALINEACION.value
            return Colores.ALINEACION.value
        elif(self.__seleccionada):
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
        if(self.estaCayendo() and self.rect.centery <= self.y_final):
            self.grav(self.t)
            self.t += 1
            self.equilibrio = self.rect.centery
            ventana.blit(self.image, self.rect)
        elif(self.estaCayendo() and self.rect.centery > self.y_final):
            if(self.t_rebote < 314/2):
                self.rebote(self.t_rebote)
                self.t_rebote += 1
            else:
                self.__cae = False
                self.rect.centery = self.equilibrio
            ventana.blit(self.image, self.rect)
        else:
            self.t = 0
            self.t_rebote = 0
            self.v_inicial = 0
            self.y_inicial = self.rect.centery
            self.equilibrio = self.rect.centery
        ventana.blit(self.image, self.rect)

    def grav(self, t):
        y = self.y_inicial + self.v_inicial*t + 0.5*GRAVEDAD*t
        self.rect.centery = y
    
    def rebote(self, t):
        y = self.equilibrio + (math.sin(0.01*2*t))*7*GRAVEDAD
        print(y)
        self.rect.centery = y
        pass
