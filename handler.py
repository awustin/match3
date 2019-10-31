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
        return self.__calculador.getFichas()

    def limpiarSeleccion(self):
        self.__calculador.limpiarFichasSeleccionadas()

    # clickSeleccionXY: recibe los indices de la cuadricula
    def clickSeleccionXY(self, x, y):
        estadoFicha = {'seleccionada': False, 'swap': False}
        self.__calculador.logicaSeleccionFichas(x, y, estadoFicha)
        return estadoFicha

    def estaSeleccionada(self, x, y):
        seleccionada = self.__calculador.estaEnLaSeleccion(x, y)
        return seleccionada

    # Pide al calculador que verifique si hay matches
    def requestMatches(self):
        self.__calculador.buscarMatches()