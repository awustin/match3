# Celda
from pygame import Rect


class Celda(object):

    def __init__(self, x, y, color=(10, 10, 10)):
        self.__rect = Rect(0, 0, x, y)
        self.__color = color
        self.__offset = (0, 0)

    def setColor(self, color):
        self.__color = color

    def getColor(self):
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

    def esClickeada(self, x0, y0):
        x = x0 - self.getOffsetAbs()[0]
        y = y0 - self.getOffsetAbs()[1]
        return self.__rect.collidepoint(x, y)
        