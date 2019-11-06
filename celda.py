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

    def setFicha(self, valor):
        '''DEPRECATED.'''
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

    def seleccionarFicha(self):
        '''DEPRECATED'''
        self.__seleccionada = True

    def seleccionarFicha2(self):
        '''Marca la ficha correspondiente a\n
        esta celda como "seleccionada"'''
        self.__ficha2.setSeleccionada(True)

    def deseleccionarFicha(self):
        '''DepRECATED'''
        self.__seleccionada = False

    def deseleccionarFicha2(self):
        '''Pone en False la bandera\n
        "seleccionada" de la ficha'''
        self.__ficha2.setSeleccionada(False)

    def getColorFicha(self):
        '''En el momento de devolver el color de la ficha,
        retorna el color original si No está seleccionada,
        retorna el color oscuro si está seleccionada'''
        if(self.__seleccionada):
            return self.__fichaColorSeleccionada
        elif(self.__alineada):
            return self.__fichaColorAlineada
        else:
            return self.__fichaColor

    def getColorFicha2(self):
        '''Devuelve el color de la ficha'''
        return self.__ficha2.getColor()

    def getFicha2(self):
        return self.__ficha2
        
    def getFicha(self):
        return self.__ficha
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