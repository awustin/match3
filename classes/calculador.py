# Calculador
from random import random


class Calculador(object):
    def __init__(self, tamanio):
        self.__init = True
        self.__fichas = []
        self.__fichasSeleccionadas = ([])
        # fichasSeleccionadas: maximo dos simultaneamente

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
        fichasSeleccionadas = self.__fichasSeleccionadas
        if(len(fichasSeleccionadas) == 0):
            self.agregarFichaSeleccionada(x, y)
            estado['seleccionada'] = True
        elif(len(fichasSeleccionadas) == 1):
            primerItem = fichasSeleccionadas[0]
            if(primerItem != (x, y)):
                print("Swapping: [%d, %d] con [%d, %d]" % (x, y, *primerItem))
                self.swapFichas(*primerItem, *(x, y))
                estado['swap'] = True
            else:
                print("Se selecciono la misma")
                self.limpiarFichasSeleccionadas()
                estado['seleccionada'] = False
        else:
            print("Hay mas de 2 fichas seleccionadas")
            estado['seleccionada'] = False
            self.limpiarFichasSeleccionadas()

    def agregarFichaSeleccionada(self, x, y):
        self.__fichasSeleccionadas.append((x, y))

    def limpiarFichasSeleccionadas(self):
        self.__fichasSeleccionadas = ([])

    def vaciarMatrizFichasEnteros(self):
        self.__fichas.clear()
        self.__fichas = []

    def swapFichas(self, x1, y1, x2, y2):
        fichas = self.__fichas
        aux = fichas[x1][y1]
        fichas[x1][y1] = fichas[x2][y2]
        fichas[x2][y2] = aux

    def estaEnLaSeleccion(self, x, y):
        fichasSeleccionadas = self.__fichasSeleccionadas
        seleccionada = False
        for ficha in range(len(fichasSeleccionadas)):
            if((x, y) == ficha):
                seleccionada = True
        return seleccionada

    def buscarMatches(self):
        '''Devuelve una tupla de dos listas:\n
            alineaciones horizontales\n
            alineaciones verticales\n'''
        alineacionesH = self.__buscarHorizontales()
        alineacionesV = self.__buscarVerticales()
        return (alineacionesH, alineacionesV)

    def __buscarHorizontales(self):
        fichas = self.__fichas
        alineacionesH = []
        alineadas = []
        horizontal = []
        cont = 0
        for row in range(len(fichas)):
            for col in range(len(fichas[row])):
                candidato = fichas[row][col]
                if(col == 0):
                    horizontal.append(candidato)
                    alineadas.append((row, col))
                    continue
                if((horizontal[0] - candidato) != 0):
                    if(len(horizontal) > 2):
                        print(f'FILA {row}: {alineadas}')
                        alineacionesH.append(alineadas)
                        cont = cont + 1
                    horizontal = []
                    alineadas = []
                horizontal.append(candidato)
                alineadas.append((row, col))
            if(len(horizontal) > 2):
                print(f'FILA {row}: {alineadas}')
                alineacionesH.append(alineadas)
                cont = cont + 1
            horizontal = []
            alineadas = []
        return alineacionesH

    def __buscarVerticales(self):
        fichas = self.__fichas
        cont = 0
        alineacionesV = []
        alineadas = []
        vertical = []
        for col in range(len(fichas)):
            for row in range(len(fichas[col])):
                candidato = fichas[row][col]
                if(row == 0):
                    vertical.append(candidato)
                    alineadas.append((row, col))
                    continue
                if((vertical[0] - candidato) != 0):
                    if(len(vertical) > 2):
                        print(f'COL {col}: {alineadas}')
                        alineacionesV.append(alineadas)
                        cont = cont + 1
                    vertical = []
                    alineadas = []
                vertical.append(candidato)
                alineadas.append((row, col))
            if(len(vertical) > 2):
                print(f'COL {col}: {alineadas}')
                alineacionesV.append(alineadas)
                cont = cont + 1
            vertical = []
            alineadas = []
        return alineacionesV
