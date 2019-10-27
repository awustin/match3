# Tablero
# Celdas de 50x50 (8x8 celdas)
import pygame
from pygame import Surface
from pygame import Rect
from pygame import draw
from pygame import gfxdraw
from handler import Handler
from celda import Celda


X_CUAD = 480
N_CELDAS = 8
X_CELDA = X_CUAD/N_CELDAS


class Tablero:
    def __init__(self, tam=(X_CUAD, X_CUAD), color=(1, 1, 1, 1)):
        self.__tam = tam
        self.__surf = Surface(self.__tam)
        self.__rect = self.__surf.get_rect()
        self.handler = Handler(N_CELDAS)
        self.__completa = False

    def inicializarCruadricula(self):
        color_base = ([])
        self.__celdas = []
        self.__pivot = (X_CELDA/2, X_CELDA/2)
        x0 = self.__pivot[0]
        y0 = self.__pivot[1]
        color_base = (50, 0, 20)
        for row in (range(N_CELDAS)):
            self.__celdas.append([])
            y = y0 + X_CELDA*row
            for col in (range(N_CELDAS)):
                x = x0 + X_CELDA*col
                color_base = (color_base[0] + 1, color_base[1] + row,
                              color_base[2] + 1*col)
                print(color_base)
                colorij = pygame.Color(*color_base)
                celdaij = Celda(X_CELDA, X_CELDA, colorij)
                celdaij.setPosicionCentro(x, y)
                celdaij.setOffsetAbs(self.__pos[0], self.__pos[1])
                pygame.draw.rect(self.__surf, celdaij.getColor(),
                                 celdaij.getRect())
                print(celdaij.getPosicionCentro())
                self.__celdas[row].append(celdaij)

    def dibujarFormas(self):
        # En el Calculador: Se debe registrar qué ficha va en la matriz
        if(not self.__completa):
            for row in range(N_CELDAS):
                for col in range(N_CELDAS):
                    ficha = self.handler.requestFicha(row, col)
                    celda = self.__celdas[row][col]
                    celda.setFicha(ficha)
                    color = celda.getColorFicha()
                    gfxdraw.aacircle(self.__surf,
                                     *celda.getPosicionCentro(),
                                     15, color)
                    gfxdraw.filled_circle(self.__surf,
                                          *celda.getPosicionCentro(),
                                          15, color)
        self.__completa = True

    def clickXY(self, x, y):
        dentroCuadricula = False
        self.handler.clickXY(x, y)
        for row in range(N_CELDAS):
            for col in range(N_CELDAS):
                celda = self.__celdas[row][col]
                if(celda.esClickeada(x, y)):
                    # TODO: La celda se selecciona
                    celda.switchSeleccionar()
                    color = celda.getColorFicha()
                    print("Seleccionada: %s en %d, %d" % (celda.getSeleccionada(), row, col))
                    gfxdraw.filled_circle(self.__surf,
                                          *celda.getPosicionCentro(),
                                          15, color)
                    dentroCuadricula = True
        if(not dentroCuadricula):
            print("Fuera del tablero")

    def setCompleto(self, completo):
        self.__completa = False

    def getSurface(self):
        return self.__surf

    def setPosicionOffset(self, x, y):
        self.__pos = (x, y)
        self.__rect.center = (x+self.__tam[0]/2, y+self.__tam[1]/2)

    def getPosicion(self):
        return self.__pos

    def getCeldas(self):
        return self.__celdas

    def getPosicionCeldas(self):
        return self.__centCeldas
