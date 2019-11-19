# Handler
from classes.calculador import Calculador
from ficha import Ficha


class Handler(object):

    def __init__(self, tamanio):
        print("Handler")
        self.__fichas = []
        self.__calculador = Calculador(tamanio)
        
    def requestFichasRan(self, n):
        ''' Arma matriz de fichas aleatorias y devuelve dicha matriz.
        n es la dimension de la matriz cuadrada'''
        self.__calculador.setFichasRan(n)
        return self.__calculador.getFichas()

    def requestFichas(self, n=0):
        '''Pide al calculador la matriz (int) de fichas\n
        Instancia una Ficha por cada elemento,\n
        si cambió la ficha\n
        Devuelve una matriz de Fichas'''
        enteros = self.__calculador.getFichas()
        if(len(enteros) == 0):
            # Es la primera vez que se carga la matriz de fichas
            # Se asigna a "enterosAnterior"
            # Se instancia cada ficha
            enteros = self.requestFichasRan(n)
            self.__enterosAnterior = enteros
            fichas = []
            for row in range(len(enteros)):
                fichas.append([])
                for col in range(len(enteros[row])):
                    if(enteros[row][col] != -1):
                        idTipo = enteros[row][col]
                        ficha = Ficha(idTipo=idTipo)
                    else:
                        ficha = None
                    fichas[row].append(ficha)
            self.__fichas = fichas
            return self.__fichas
        else:
            # El calculador ya tiene fichas (enteros) cargadas
            # El handler ya tiene matriz de fichas
            # En un nuevo arreglo, se copia el mismo objeto
            # A menos que haya un cambio.
            # En ese caso, se instancia uno nuevo
            fichasAnterior = self.__fichas
            fichasNuevas = []
            for row in range(len(enteros)):
                fichasNuevas.append([])
                for col in range(len(enteros[row])):
                    if(fichasAnterior[row][col] is None):
                        '''Habia una ficha eliminada (nula)'''
                        if(enteros[row][col] == -1):
                            '''La ficha ya está eliminada'''
                            ficha = fichasAnterior[row][col]
                        else:
                            '''La ficha se crea en el lugar de una eliminada'''
                            tipoNuevo = enteros[row][col]
                            ficha = Ficha(tipoNuevo)
                    else:
                        '''Había una ficha no nula'''
                        if(enteros[row][col] == -1):
                            '''La ficha existente se va a eliminar (-1)'''
                            ficha = None
                        else:
                            '''La ficha no se elimina'''
                            tipoAnterior = fichasAnterior[row][col].getTipoInt()
                            if(tipoAnterior == enteros[row][col]):
                                '''La ficha coincide con el entero que trae'''
                                ficha = fichasAnterior[row][col]
                            else:
                                '''La ficha no coincide con el entero que trae'''
                                tipoNuevo = enteros[row][col]
                                ficha = Ficha(tipoNuevo)
                    fichasNuevas[row].append(ficha)
            self.__fichas = fichasNuevas
            return self.__fichas

    def limpiarSeleccion(self):
        '''Vacia la lista de fichas seleccionadas'''
        self.__calculador.limpiarFichasSeleccionadas()

    def seleccionFichasYEstado(self, x, y):
        '''Devuelve un diccionario 'estadoFicha' que posee: \n
        'seleccionada': Si la ficha (x, y) quedó en la lista de seleccion \n
        'swap': Si la ficha se intercambia con otra \n
        'anterior': Si hay q deseleccionar la primera ficha \n
        que se seleccionó, se pasa por esta clave
        Este método dispara la lógica de selección de fichas en el \n
        calculador'''
        estadoFicha = {'seleccionada': False, 'swap': False, 'anterior': None}
        self.__calculador.logicaSeleccionFichas(x, y, estadoFicha)
        return estadoFicha

    def buscarAlineaciones(self):
        '''Pide al calculador que busque alineaciones.
        Retorna False si no encuentra.'''
        return self.__calculador.logicaAlineacionFichas()

    def anularFichasAlineadas(self):
        '''Pide al calculador que ponga en -1 todas las
        fichas alienadas. Devuelve False si no se anulo nada.'''
        return self.__calculador.logicaEliminacionFichas()

    def logicaReemplazoFichas(self):
        '''Pide al calculador que reemplace las fichas que
        están en -1'''
        self.__calculador.logicaReemplazoFichas()

    def reiniciarCalculador(self):
        self.__calculador.limpiarFichasSeleccionadas()
        self.__calculador.vaciarMatrizFichasEnteros()

    def enviarConfiguracionTablero(self, fichas):
        self.__calculador.setFichas(fichas)

    def requestRellenoColumna(self, col):
        columnaFichas = []
        columna = self.__calculador.rellenoFichasPorColumna(col)
        for i in columna:
            if(i == -1 or i is None):
                ficha = None
            else:
                ficha = Ficha(i)
            columnaFichas.append(ficha)
        return columnaFichas

