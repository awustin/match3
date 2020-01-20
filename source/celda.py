# Celda
from pygame import Rect
from cellContent import Chip


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

    def setFicha(self, cell_class=0, ficha=None):
        '''Instancia y/o asigna una ficha a la celda.\n
        "token_class" es la clase de la ficha.\n
        Si no se pasa una clase, se asigna\n
        NO_ESPECIFICADO'''
        if(ficha is None):
            ficha = Chip(cell_class)
            self.__ficha = ficha
        else:
            self.__ficha = ficha
        centro = self.get_center_pos()
        self.__ficha.set_center_pos(*centro)

    def seleccionarFicha(self):
        '''Marca la ficha correspondiente a\n
        esta celda como "seleccionada"'''
        if(self.__ficha.get_class() != -2):
            self.__ficha.set_selected(True)

    def deseleccionarFicha(self):
        '''Pone en False la bandera\n
        "seleccionada" de la ficha'''
        if(self.__ficha.get_class() != -2):
            self.__ficha.set_selected(False)

    def get_cell_content(self):
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

    def get_center_pos(self):
        return self.__rect.center

    def set_center_pos(self, x, y):
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
            raise Exception(
                  f'La celda {self.getCoord()} no tiene ninguna ficha')
        else:
            ficha = self.get_cell_content()
            celda.setFicha(ficha=ficha)
            self.__ficha = None

    def distanciaY(self, celda):
        '''Calcula la distancia vertical (en pixeles)
        entre los centros de esta celda y la celda que se
        pasa como argumento'''
        distancia = self.get_center_pos()[0] - celda.get_center_pos()[0]
        return abs(distancia)
