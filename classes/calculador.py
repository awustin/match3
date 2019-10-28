# Calculador
from random import random


class Calculador(object):
    def __init__(self, tamanio):
        self.__init = True
        self.__fichas = []
        self.__fichasSeleccionadas = ([])
        # fichasSeleccionadas: maximo dos simultaneamente
        self.setFichasVacias(tamanio)

    def setFichasVacias(self, n):
        for row in range(n):
            self.__fichas.append([])
            for col in range(n):
                self.__fichas[row].append(0)

    def getFichaXY(self, x, y):
        ran = random()
        if(ran > 0 and ran <= 0.25):
            ficha = 1
        elif(ran > 0.25 and ran <= 0.5):
            ficha = 2
        elif(ran > 0.5 and ran <= 0.75):
            ficha = 3
        else:
            ficha = 4
        self.__fichas[x][y] = ficha
        return ficha

    def getFichas(self):
        return self.__fichas

    def logicaSeleccionFichas(self, x, y, estado):
        fichasSeleccionadas = self.__fichasSeleccionadas
        if(len(fichasSeleccionadas) == 0):
            self.agregarFichaSeleccionada(x, y)
            estado['seleccionada'] = True
        elif(len(fichasSeleccionadas) == 1):
            primerItem = fichasSeleccionadas[0]
            if(primerItem != (x, y)):
                print("Swapping...")
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
        print(fichasSeleccionadas)

    def agregarFichaSeleccionada(self, x, y):
        self.__fichasSeleccionadas.append((x, y))

    def limpiarFichasSeleccionadas(self):
        self.__fichasSeleccionadas = ([])

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
