# Handler
from classes.calculador import Calculador


class Handler(object):

    def __init__(self, tamanio):
        print("Handler")
        self.__calculador = Calculador(tamanio)

    def requestFichasRan(self, n):
        ''' Arma matriz de fichas aleatorias y devuelve dicha matriz.
        n es la dimension de la matriz cuadrada'''
        self.__calculador.setFichasRan(n)
        return self.__calculador.getFichas()

    def requestFichas(self):
        return self.__calculador.getFichas()

    def requestFicha(self, x, y):
        # Pide la ficha para la posicion x, y
        # Devuelve una response
        ficha = self.__calculador.getFichaXY(x, y)
        return ficha

    def limpiarSeleccion(self):
        '''Vacia la lista de fichas seleccionadas'''
        self.__calculador.limpiarFichasSeleccionadas()

    def seleccionFichasYEstado(self, x, y):
        '''Devuelve un diccionario 'estadoFicha' que posee: \n
        'seleccionada': Si la ficha (x, y) quedó en la lista de seleccion \n
        'swap': Si la ficha se intercambia con otra \n
        Este método dispara la lógica de selección de fichas en el \n
        calculador'''
        estadoFicha = {'seleccionada': False, 'swap': False}
        self.__calculador.logicaSeleccionFichas(x, y, estadoFicha)
        return estadoFicha

    def requestMatches(self):
        '''Pide al calculador que verifique si hay
        alineaciones'''
        return self.__calculador.buscarMatches()
