# Celda
from pygame import Rect
from ficha import Ficha


class Celda(object):

    def __init__(self, x, y, posx=0, posy=0, color=(10, 10, 10)):
        self.__rect = Rect(posx, posy, x, y)
        self.__seleccionada = False
        self.__alineada = False
        self.__color = color
        self.__colorSeleccionada = color
        self.__ficha2 = None
        self.__ficha = 0
        self.__fichaColor = color
        self.__fichaColorSeleccionada = (10, 10, 10)
        self.__fichaColorAlineada = (200, 200, 50)
# //
# Metodos sobre las fichas
# //

    def setFicha2(self, idTipo=0, ficha=None):
        '''Instancia y/o asigna una ficha a la celda.\n
        "tipo" es el id entero del Tipo.\n
        Si no se pasa un tipo, se asigna\n
        NO_ESPECIFICADO'''
        if(ficha is None):
            ficha = Ficha(idTipo)
            self.__ficha2 = ficha
        else:
            self.__ficha2 = ficha

    def seleccionarFicha2(self):
        '''Marca la ficha correspondiente a\n
        esta celda como "seleccionada"'''
        self.__ficha2.setSeleccionada(True)

    def deseleccionarFicha2(self):
        '''Pone en False la bandera\n
        "seleccionada" de la ficha'''
        self.__ficha2.setSeleccionada(False)

    def setFichaAlineada(self, valor):
        '''Marca la ficha de esta celda como\n
        alineada (True) o no alineada (False)'''
        self.__ficha2.setAlineada(valor)

    def getColorFicha2(self):
        '''Devuelve el color de la ficha'''
        return self.__ficha2.getColor()

    def getFicha2(self):
        return self.__ficha2
        
# //
# Métodos sobre la celda
# //

    def setColorCelda(self, color):
        self.__color = color

    def getColorCelda(self):
        return self.__color

    def getRect(self):
        return self.__rect

    def getPosicionCentro(self):
        return self.__rect.center

    def setPosicionCentro(self, x, y):
        self.__rect.center = (x, y)

    def esClickeada(self, x, y):
        '''Devuelve True si el Rect correspondiente
        a esta celda fue clickeado (si collidepoint
        de pygame retorna True)'''
        return self.__rect.collidepoint(x, y)