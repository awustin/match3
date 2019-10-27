# Handler
from classes.calculador import Calculador


class Handler(object):

    def __init__(self, tamanio):
        print("Handler")
        self.__calculador = Calculador(tamanio)

    def requestFicha(self, x, y):
        # Pide la ficha para la posicion x, y
        # Devuelve una response
        ficha = self.__calculador.getFichaXY(x, y)
        return ficha

    def requestFichas(self):
        self.__calculador.getFichas()

    def clickXY(self, x, y):
        self.__calculador.setClickXY(x, y)
