# Celda
from pygame import Rect
from ficha import Ficha


class Celda(object):

    def __init__(self, x, y, posx=0, posy=0, color=(10, 10, 10)):
        self.__rect = Rect(posx, posy, x, y)
        self.__color = color
        self.__coord = ()
        self.__ficha = None
        self.__sueltaFicha = False
# //
# Get - Set
# //

    def setCoord(self, x, y):
        '''Setea el indice que ocupa la celda 
        en el tablero. Esta informacion es
        util para la logica de pasaje de fichas'''
        self.__coord = (x, y)
    
    def getCoord(self):
        '''Devuelve el indice que ocupa la celda
        en el tablero'''
        return self.__coord

    def sueltaFicha(self):
        '''Devuelve True si esta haciendo un pasaje
        de fichas'''
        return self.__sueltaFicha
    
    def setSueltaFicha(self, valor):
        self.__sueltaFicha = valor

# //
# Metodos sobre las fichas
# //

    def setFicha(self, idTipo=0, ficha=None):
        '''Instancia y/o asigna una ficha a la celda.\n
        "tipo" es el id entero del Tipo.\n
        Si no se pasa un tipo, se asigna\n
        NO_ESPECIFICADO'''
        if(ficha is None):
            ficha = Ficha(idTipo)
            self.__ficha = ficha
        else:
            self.__ficha = ficha
        centro = self.getPosicionCentro()
        self.__ficha.setPosicionCentro(*centro)

    def seleccionarFicha(self):
        '''Marca la ficha correspondiente a\n
        esta celda como "seleccionada"'''
        self.__ficha.setSeleccionada(True)

    def deseleccionarFicha(self):
        '''Pone en False la bandera\n
        "seleccionada" de la ficha'''
        self.__ficha.setSeleccionada(False)

    def setFichaAlineada(self, valor):
        '''Marca la ficha de esta celda como\n
        alineada (True) o no alineada (False)'''
        self.__ficha.setAlineada(valor)

    def getColorFicha(self):
        '''Devuelve el color de la ficha'''
        return self.__ficha.getColor()

    def getFicha(self):
        return self.__ficha

    def hayFicha(self):
        return self.__ficha is not None

    def borrarFicha(self):
        self.__ficha = None

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

    def pasarFicha(self, celda):
        '''Pasa su ficha a la celda que se pasa
        como argumento.'''
        if(self.__ficha is None):
            raise Exception(f'La celda {self.getCoord()} no tiene ninguna ficha')
        else:
            ficha = self.getFicha()
            celda.setFicha(ficha=ficha)
            self.__ficha = None

    def distanciaY(self, celda):
        '''Calcula la distancia vertical (en pixeles)
        entre los centros de esta celda y la celda que se
        pasa como argumento'''
        distancia = self.getPosicionCentro()[0] - celda.getPosicionCentro()[0]
        return abs(distancia)
