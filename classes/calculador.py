# Calculador
from random import random
from classes.alineacion import Alineacion


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

    def logicaSeleccionFichas(self, x, y, estado):
        '''Se fija en la lista de fichas seleccionadas y setea
        el valor de la ficha actual. Argumentos:\n
        x: es la fila actual\n
        y: es la columna actual\n
        estado: es un diccionario {seleccionada: False, swap: False}\n'''
        alineacion = self.__alineaciones
        if(not alineacion.haySeleccionadas()):
            '''Es la primera seleccion'''
            alineacion.agregarASeleccion((x, y))
            estado['seleccionada'] = True
        elif(alineacion.hayUnaSeleccionada()):
            '''Es la segunda selección'''
            primerItem = alineacion.getSeleccionadas()[0]
            x0 = primerItem[0]
            y0 = primerItem[1]
            if(primerItem == (x, y) or
               self.__fichas[x0][y0] == self.__fichas[x][y]):
                '''Se elije la misma ficha'''
                print("Se selecciono la misma")
                estado['seleccionada'] = False
                estado['anterior'] = primerItem
                alineacion.limpiarSeleccion()
            else:
                print("Swapping: [%d, %d] con [%d, %d]" % (x, y, *primerItem))
                self.swapFichas(*primerItem, *(x, y))
                estado['swap'] = True
        else:
            print("Hay mas de 2 fichas seleccionadas")
            estado['seleccionada'] = False
            alineacion.limpiarSeleccion()

    def limpiarFichasSeleccionadas(self):
        alineacion = self.__alineaciones
        alineacion.limpiarSeleccion()

    def vaciarMatrizFichasEnteros(self):
        self.__fichas.clear()
        self.__fichas = []

    def swapFichas(self, x1, y1, x2, y2):
        fichas = self.__fichas
        aux = fichas[x1][y1]
        fichas[x1][y1] = fichas[x2][y2]
        fichas[x2][y2] = aux

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
        Poner en -1 las fichas alineadas.\n
        Devuelve False si no hay alineaciones'''
        hayMatches = False
        alineacionesH = self.__alineaciones.buscarHorizontales(self.__fichas, 3)
        alineacionesV = self.__alineaciones.buscarVerticales(self.__fichas, 3)
        if(alineacionesH != [] or alineacionesV != []):
            hayMatches = True
        return hayMatches

    def logicaReemplazoFichas(self):
        '''Se encarga de colocar nuevos números en
        donde hay -1'''
        for row in range(len(self.__fichas)):
            for col in range(len(self.__fichas[row])):
                if(self.__fichas[row][col] == -1):
                    self.__fichas[row][col] = self.generarFichaRan()

    def rellenoFichasPorColumna(self, col):
        columna = []
        for i in range(len(self.__fichas)):
            if(self.__fichas[i][col] == -1 
               or self.__fichas[i][col] is None):
                columna.append(self.generarFichaRan())
            else:
                columna.append(self.__fichas[i][col])
        return columna
