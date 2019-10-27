# Calculador
from random import random


class Calculador(object):
    def __init__(self, tamanio):
        self.__init = True
        self.__fichas = []
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
        print(self.__fichas)

    def setClickXY(self, x, y):
        print((x, y))
