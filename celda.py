# Celda
from pygame import Rect
from pygame import Surface


class Celda(object):

    def __init__(self, x, y, posx=0, posy=0, color=(10, 10, 10)):
        self.__rect = Rect(posx, posy, x, y)
        self.__color = color
        self.__colorSeleccionada = color
        self.__seleccionada = False
        self.__offset = (0, 0)
        self.__ficha = 0
        self.__fichaColor = color
        self.__fichaColorSeleccionada = (10, 10, 10)

    def getSeleccionada(self):
        return self.__seleccionada

    def seleccionarFicha(self):
        self.__seleccionada = True

    def deseleccionarFicha(self):
        self.__seleccionada = False

    def switchSeleccionar(self):
        if(self.__seleccionada):
            self.deseleccionarFicha()
        else:
            self.seleccionarFicha()

    def getColorFicha(self):
        '''En el momento de devolver el color de la ficha,
        retorna el color original si No está seleccionada,
        retorna el color oscuro si está seleccionada'''
        if(self.__seleccionada):
            return self.__fichaColorSeleccionada
        else:
            return self.__fichaColor

    def setColorCelda(self, color):
        self.__color = color

    def getColorCelda(self):
        return self.__color

    def getRect(self):
        return self.__rect

    def getOffsetAbs(self):
        return self.__offset

    def setOffsetAbs(self, x, y):
        self.__offset = (x, y)

    def getPosicionCentro(self):
        return self.__rect.center

    def setPosicionCentro(self, x, y):
        self.__rect.center = (x, y)

    def esClickeada(self, x, y):
        '''Devuelve True si el Rect correspondiente
        a esta celda fue clickeado (si collidepoint
        de pygame retorna True)'''
        return self.__rect.collidepoint(x, y)

    def setFicha(self, valor):
        self.__ficha = valor
        if(self.__ficha == 1):
            self.__fichaColor = (255, 100, 50)
        elif(self.__ficha == 2):
            self.__fichaColor = (120, 255, 50)
        elif(self.__ficha == 3):
            self.__fichaColor = (120, 100, 255)
        elif(self.__ficha == 4):
            self.__fichaColor = (255, 255, 50)
        else:
            self.__fichaColor = (255, 255, 255)

    def getFicha(self):
        return self.__ficha
