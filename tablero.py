# Tablero
# Celdas de 50x50 (8x8 celdas)
import pygame
from pygame import draw
from pygame import gfxdraw
from pygame import time
from handler import Handler
from celda import Celda
from random import random
import globales


X_CUAD = 480
Y_CUAD = X_CUAD
X_OFF = (globales.DIMENSION[0] - X_CUAD) / 2
Y_OFF = (globales.DIMENSION[1] - Y_CUAD) / 2
N_CELDAS = 8
X_CELDA = X_CUAD/N_CELDAS


class Tablero:
    def __init__(self, tam=(X_CUAD, X_CUAD), color=(1, 1, 1)):
        self.handler = Handler(N_CELDAS)
        self.__color_base = color
        self.__celdas = []
        self.__celdasEstanCompletas = False
        self.__matches = False

    def setCompleto(self, completo):
        '''Asigna valor a la bandera para ver si
        se debe actualizar la matriz de celdas o no.
        Si está completo (se dibujaron todas las celdas):
        no se reinicia la matriz de celdas.
        Si hubo cambios en las celdas (p ejemplo, al reiniciar
        el tablero):
        se reinicia la matriz de celdas'''
        self.__celdasEstanCompletas = completo

    def setMatches(self, matches):
        '''Asigna valor a la bandera para ver si
        se encontraron alineaciones'''
        self.__matches = matches

    def reiniciarMatrizCeldas(self):
        self.__celdas.clear()
        self.__celdas = []

    def reiniciarMatrizFichas(self):
        self.__fichas.clear()

    def reiniciarCalculador(self):
        '''Reinicia el calculador:\n
        Vacia la lista de alineadas\n
        Vacia la lista de seleccion\n
        Recarga una matriz de enteros random\n'''
        self.handler.reiniciarCalculador()

    def reiniciaFichasCeldasTablero(self):
        '''Vacía la matriz de celdas,\n
        Vacía la matriz de fichas\n
        Pone las banderas en su estado inicial'''
        self.reiniciarMatrizCeldas()
        self.reiniciarCalculador()
        self.setCompleto(False)
        self.setMatches(False)
        self.__color_base = (random()*255, random()*255, random()*255)

    def gradiente(self, color):
        difr = 50*random()
        difg = 50*random()
        difb = 50*random()
        if(difr + color[0] > 255):
            difr = -50
        if(difg + color[1] > 255):
            difg = -50
        if(difb + color[2] > 255):
            difb = -50
        r = color[0] + difr
        g = color[1] + difg
        b = color[2] + difb
        return (r, g, b)

    def generarTableroFilaPorFila(self, ventana, x_celda, x_espaciado,
                                  color_base, fichas):
        ''' Cuando las celdas no estén completas, se deberá
        generarlas.\n
        Luego, se pide la matriz de fichas random\n
        Luego, se completa fila a fila, empezando por la ultima.\n
        ventana es una Surface\n
        n es el numero de filas (igual al de columnas)\n
        x_celda es el tamaño de la celda\n
        x_espaciado es el ancho del espaciado entre celdas\n
        color_base es el color base de la celda'''
        color = color_base
        for row in range(len(fichas)):
            self.__celdas.append([])
            for col in range(len(fichas[row])):
                color = self.gradiente(color)
                celda = Celda(x_celda, x_celda, col*(x_celda+x_espaciado) +
                              X_OFF, row*(x_celda+x_espaciado) + Y_OFF,
                              color)
                celda.setColorCelda(color)
                rect = celda.getRect()
                draw.rect(ventana, color, rect)
                self.__celdas[row].append(celda)
        pygame.display.update()
        for row in reversed(range(len(fichas))):
            for col in range(len(fichas)):
                celda = self.__celdas[row][col]
                centro = celda.getPosicionCentro()
                celda.setFicha(ficha=fichas[row][col])
                colorFicha = celda.getColorFicha()
                gfxdraw.aacircle(ventana, *centro, 15, colorFicha)
                gfxdraw.filled_circle(ventana, *centro, 15, colorFicha)
                time.wait(7)
                pygame.display.update()
                if(row == len(self.__celdas)-1
                   and col == len(self.__celdas[row])-1):
                    self.setCompleto(True)

    def logicaAlineacionFichas(self):
        '''Pide que se determinen las alineaciones.
        El calculador revisa su lista de alineaciones,
        y si encuentra, dispara la logica de eliminación'''
        return self.handler.logicaAlineacionFichas()

    def actualizarTablero(self, ventana, x_celda, x_espaciado, fichas):
        '''Actualiza el tablero.
        Si no está completo (no se dibujaron todas las celdas),
        se crean instancias de Celda.
        Si está completo (ya se dibujaron todas las celdas),
        recorre la matriz de celdas en busca de cambios de 
        estado.
        ventana es una Surface
        x_celda el tamaño de la celda cuadrada.
        x_espaciado es el espaciado entre las celdas.
        color_base es el color de la celda
        fichas es la matriz (objetos) de fichas'''
        celdas = self.__celdas
        for row in range(len(celdas)):
            for col in range(len(celdas[row])):
                celda = celdas[row][col]
                if(fichas[row][col] is not None):
                    '''La ficha existe'''
                    if(not celda.getFicha().equals(fichas[row][col])):
                        '''La ficha se intercambió'''
                        celda.setFicha(fichas[row][col].getTipoInt())
                    centro = celda.getPosicionCentro()
                    colorFicha = celda.getColorFicha()
                    draw.rect(ventana, celda.getColorCelda(), celda.getRect())
                    gfxdraw.aacircle(ventana, *centro, 15, colorFicha)
                    gfxdraw.filled_circle(ventana, *centro, 15, colorFicha)
                else:
                    '''La ficha se eliminó'''
                    centro = celda.getPosicionCentro()
                    colorFicha = celda.getColorFicha()
                    draw.rect(ventana, celda.getColorCelda(), celda.getRect())
        self.__matches = self.logicaAlineacionFichas()

    def actualizarTableroConEstado(self, ventana):
        ''' Actualiza el tablero, segun el estado de las fichas
        y las alineaciones.
        El programa principal debe llamar a esta función en cada iteración'''        
        color_base = self.__color_base
        fichas = self.handler.requestFichas(N_CELDAS)
        if(not self.__celdasEstanCompletas):
            self.generarTableroFilaPorFila(ventana, X_CELDA, 5, color_base,
                                           fichas)
        else:
            self.actualizarTablero(ventana, X_CELDA, 5, fichas)

    def deseleccionarTodasCeldas(self):
        '''Recorre la matriz de celdas y deselecciona
        una por una'''
        for row in range(len(self.__celdas)):
            for col in range(len(self.__celdas[row])):
                celda = self.__celdas[row][col]
                celda.deseleccionarFicha()

    def limpiarSeleccionCeldas(self):
        '''Vacia la lista de seleccionadas en el calculador \n
        Deselecciona todas las celdas del tablero \n
        Setea el valor de 'matches' a False'''
        self.handler.limpiarSeleccion()
        self.deseleccionarTodasCeldas()
        self.__matches = False

    def clickXY(self, x, y):
        '''Busca cuál fue la casilla clickeada
        y dispara la lógica de selección de las fichas'''
        limpiar = False
        dentroCuadricula = False
        fichas = self.handler.requestFichas(N_CELDAS)
        for row in range(len(fichas)):
            if(limpiar):
                break
            for col in range(len(fichas[row])):
                celda = self.__celdas[row][col]
                if(celda.esClickeada(x, y)):
                    dentroCuadricula = True
                    print(f'Se clickeó la celda {(row, col)}')
                    estadoFicha = self.handler.seleccionFichasYEstado(row, col)
                    print(estadoFicha)
                    if(estadoFicha['seleccionada']):
                        celda.seleccionarFicha()
                    else:
                        p0 = estadoFicha['anterior']
                        if(p0 is not None):
                            self.__celdas[p0[0]][p0[1]].deseleccionarFicha()
                        celda.deseleccionarFicha()
                    if(estadoFicha['swap']):
                        limpiar = True
                        break
                    break
        if(not dentroCuadricula):
            print("Fuera del tablero")
        if(limpiar):
            self.limpiarSeleccionCeldas()
