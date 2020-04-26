# Calculador
from random import random
from model.alineacion import Alineacion


class Calculador(object):
    def __init__(self, tamanio):
        self.__init = True
        self.__fichas = []
        self.__alineaciones = Alineacion()
        # fichasSeleccionadas: maximo dos simultaneamente

    def setFichas(self, fichas):
        self.__fichas = fichas

    def getFichas(self):
        return self.__fichas

    def generarFichaRan(self):
        '''Genera un entero entre 1 y 4'''
        ran = random()
        if(ran > 0 and ran <= 0.25):
            return 1
        elif(ran > 0.25 and ran <= 0.5):
            return 2
        elif(ran > 0.5 and ran <= 0.75):
            return 3
        else:
            return 4

    def setFichasVacias(self, n):
        '''Arma una matriz nxn de 0'''
        for row in range(n):
            self.__fichas.append([])
            for col in range(n):
                self.__fichas[row].append(0)

    def checkeoDeIguales(self, ficha, row, col):
        '''Chequea que no halla alineaciones de 3 y
        cambia si lo hay. Argumentos:\n
        ficha: entero\n
        row: fila\n
        col: columna\n'''
        if(row <= 1 and col <= 1):
            '''No se hace ningun chequeo en 0,0 0,1 1,0 y 1,1'''
            return ficha
        if(row <= 1 and col > 1):
            '''Chequea que no haya alineaciones horizontales'''
            while(self.__fichas[row][col - 1] == ficha and
                  self.__fichas[row][col - 2] == ficha):
                ficha = self.generarFichaRan()
        elif(row > 1 and col <= 1):
            '''Chequea que no haya alineaciones verticales'''
            while(self.__fichas[row - 1][col] == ficha and
                  self.__fichas[row - 2][col] == ficha):
                ficha = self.generarFichaRan()
        elif(row > 1 and col > 1):
            '''Chequea que no haya alineaciones ni verticales
            ni horizontales'''
            while((self.__fichas[row - 1][col] == ficha and
                  self.__fichas[row - 2][col] == ficha) or
                  (self.__fichas[row][col - 1] == ficha and
                  self.__fichas[row][col - 2] == ficha)):
                ficha = self.generarFichaRan()
        return ficha

    def set_unbreakables(self):
        '''This will set unbreakable blocks in the matrix'''
        if(self.__fichas == []):
            return
        # Read from a file or generate randoms
        # For test I will put a block in position 0,0
        self.__fichas[0][0] = -2

    def setFichasRan(self, n):
        '''Arma una matriz nxn de numeros aleatorios entre 1 y 4'''
        for row in range(n):
            self.__fichas.append([])
            for col in range(n):
                ficha = self.generarFichaRan()
                ficha = self.checkeoDeIguales(ficha, row, col)
                self.__fichas[row].append(ficha)

    def agregarFilaFichasRan(self, n):
        '''A la matriz que ya existe, le agrega una fila de numeros
        aleatorios entre 1 y 4'''
        if(len(self.__fichas) >= 8):
            print("Ya hay 8 filas en la matriz de fichas")
        else:
            fila = []
            for col in range(n):
                ficha = self.generarFichaRan()
                fila.append(ficha)
            self.__fichas.append(fila)
        return fila

    def __equals_first_selected(self, x, y):
        x0 = self.__alineaciones.get_selected(0)[0]
        y0 = self.__alineaciones.get_selected(0)[1]
        return self.__fichas[x0][y0] == self.__fichas[x][y]
    
    def __first_selected_class(self):
        x0 = self.__alineaciones.get_selected(0)[0]
        y0 = self.__alineaciones.get_selected(0)[1]
        return self.__fichas[x0][y0]

    def __temp_swapped(self, x0, y0, x1, y1):
        temp_array = list(self.__fichas)
        temp_array = self.__swap(x0, y0, x1, y1, temp_array)
        return temp_array

    def __adjacent_alignments(self, x1, y1):
        x0 = self.__alineaciones.get_selected(0)[0]
        y0 = self.__alineaciones.get_selected(0)[1]
        temp_array = self.__temp_swapped(x0, y0, x1, y1)
        count = self.__alineaciones.search_adjacent(x1, y1, temp_array)
        if count[0] < 3 and count[1] < 3:
            return False
        return True

    def __is_legal_movement(self, x, y, status):
        if self.__equals_first_selected(x, y):
            return False
        return self.__adjacent_alignments(x, y)

    def __second_selected(self, x, y, status):
        if not self.__is_legal_movement(x, y, status):
            status['seleccionada'] = False
            status['anterior'] = self.__alineaciones.get_selected(0)
            self.__alineaciones.clear_selected()
        else:
            self.__chips_swap(*self.__alineaciones.get_selected(0), *(x, y))
            status['swap'] = True
            status['anterior'] = self.__alineaciones.get_selected(0)

    def __first_selected(self, x, y, status):
        self.__alineaciones.agregarASeleccion((x, y))
        status['seleccionada'] = True

    def logicaSeleccionFichas(self, x, y, estado):
        '''Se fija en la lista de fichas seleccionadas y setea
        el valor de la ficha actual. Argumentos:\n
        x: es la fila actual\n
        y: es la columna actual\n
        estado: es un diccionario {seleccionada: False, swap: False}\n'''
        alineacion = self.__alineaciones
        if not alineacion.haySeleccionadas():
            self.__first_selected(x, y, estado)
        elif alineacion.hayUnaSeleccionada():
            self.__second_selected(x, y, estado)
        else:
            estado['seleccionada'] = False
            alineacion.limpiarSeleccion()

    def limpiarFichasSeleccionadas(self):
        alineacion = self.__alineaciones
        alineacion.limpiarSeleccion()

    def vaciarMatrizFichasEnteros(self):
        self.__fichas.clear()
        self.__fichas = []

    def __chips_swap(self, x0, y0, x1, y1):
        self.__fichas = self.__swap(x0, y0, x1, y1, self.__fichas)

    def __swap(self, x0, y0, x1, y1, array):
        aux = array[x0][y0]
        array[x0][y0] = array[x1][y1]
        array[x1][y1] = aux
        return array

    def logicaEliminacionFichas(self):
        '''Pone en -1 todos los lugares donde
        se encontraron alineaciones'''
        seAnularon = False
        alineaciones = self.__alineaciones
        if(alineaciones.hayHorizontales()):
            seAnularon = True
            for alineacion in alineaciones.getHorizontales():
                for ficha in alineacion:
                    x = ficha[0]
                    y = ficha[1]
                    self.__fichas[x][y] = -1
        if(alineaciones.hayVerticales()):
            seAnularon = True
            for alineacion in alineaciones.getVerticales():
                for ficha in alineacion:
                    x = ficha[0]
                    y = ficha[1]
                    self.__fichas[x][y] = -1
        return seAnularon

    def logicaAlineacionFichas(self):
        '''Se encarga de:\n
        Buscar alineaciones horizontales,\n
        Buscar alineaciones verticales,\n
        Poner en -1 las fichas alineadas.\n'''
        self.__alineaciones.buscarHorizontales(self.__fichas, 3)
        self.__alineaciones.buscarVerticales(self.__fichas, 3)
        return self.__alineaciones.getAlineaciones()

    def filaFichasNuevas(self, fila):
        '''Actualiza su matriz de fichas a medida que va
        generando filas nuevas'''
        nuevaFila = []
        for col in range(len(self.__fichas[fila])):
            if(self.__fichas[fila][col] == -1):
                ficha = self.generarFichaRan()
                nuevaFila.append(ficha)
                self.__fichas[fila][col] = ficha
            else:
                nuevaFila.append(-1)
        return nuevaFila
