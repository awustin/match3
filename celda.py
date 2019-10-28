# Celda
from pygame import Rect


class Celda(object):

    def __init__(self, x, y, color=(10, 10, 10)):
        self.__rect = Rect(0, 0, x, y)
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
        if(self.__seleccionada):
            return self.__fichaColorSeleccionada
        else:
            return self.__fichaColor

    def setColor(self, color):
        self.__color = color

    def getColor(self):
        return self.__color

    def setColorSeleccionada(self, color):
        self.__colorSeleccionada = color

    def getColorSeleccionada(self):
        return self.__colorSeleccionada

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

    def esClickeada(self, x0, y0):
        x = x0 - self.getOffsetAbs()[0]
        y = y0 - self.getOffsetAbs()[1]
        return self.__rect.collidepoint(x, y)

    def setFicha(self, valor):
        self.__ficha = valor
        if(self.__ficha == 1):
            self.__fichaColor = (255, 0, 0)
        elif(self.__ficha == 2):
            self.__fichaColor = (0, 255, 0)
        elif(self.__ficha == 3):
            self.__fichaColor = (0, 0, 255)
        elif(self.__ficha == 4):
            self.__fichaColor = (255, 255, 0)

    def getFicha(self):
        return self.__ficha
