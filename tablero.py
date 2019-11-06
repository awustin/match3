# Tablero
# Celdas de 50x50 (8x8 celdas)
from pygame import draw
from pygame import gfxdraw
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

    def actualizarTablero(self, ventana, x_celda, x_espaciado, color_base,
                          fichas):
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
        color = color_base
        if(not self.__celdasEstanCompletas):
            for row in range(len(fichas)):
                self.__celdas.append([])
                for col in range(len(fichas[row])):
                    color = self.gradiente(color)
                    celda = Celda(x_celda, x_celda, col*(x_celda+x_espaciado) +
                                  X_OFF, row*(x_celda+x_espaciado) + Y_OFF,
                                  color)
                    celda.setFicha2(ficha=fichas[row][col])
                    celda.setColorCelda(color)
                    centro = celda.getPosicionCentro()
                    rect = celda.getRect()
                    draw.rect(ventana, color, rect)
                    colorFicha = fichas[row][col].getColor()
                    gfxdraw.aacircle(ventana, *centro, 15, colorFicha)
                    gfxdraw.filled_circle(ventana, *centro, 10, colorFicha)
                    self.__celdas[row].append(celda)
                    if(row == len(fichas)-1 and col == len(fichas[row])-1):
                        self.setCompleto(True)
        else:
            celdas = self.__celdas
            for row in range(len(celdas)):
                for col in range(len(celdas[row])):
                    celda = celdas[row][col]
                    if(not celda.getFicha2().equals(fichas[row][col])):
                        celda.setFicha2(fichas[row][col].getTipoInt())
                    centro = celda.getPosicionCentro()
                    colorFicha = celda.getColorFicha2()
                    draw.rect(ventana, celda.getColorCelda(), celda.getRect())
                    gfxdraw.aacircle(ventana, *centro, 15, colorFicha)
                    gfxdraw.filled_circle(ventana, *centro, 10, colorFicha)
        self.verificarMatches(ventana)

    def actualizarTableroConEstado(self, ventana):
        ''' Actualiza el tablero, segun el estado de las fichas
        y las alineaciones.
        El programa principal debe llamar a esta función en cada iteración'''
        fichas = self.handler.requestFichas(N_CELDAS)
        color_base = self.__color_base
        self.actualizarTablero(ventana, X_CELDA, 5, color_base, fichas)

    def deseleccionarTodasCeldas(self):
        '''Recorre la matriz de celdas y deselecciona
        una por una'''
        for row in range(len(self.__celdas)):
            for col in range(len(self.__celdas[row])):
                celda = self.__celdas[row][col]
                celda.deseleccionarFicha2()

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
                    if(estadoFicha['seleccionada']):
                        celda.seleccionarFicha2()
                    else:
                        celda.deseleccionarFicha2()
                    if(estadoFicha['swap']):
                        limpiar = True
                        break
                    break
        if(not dentroCuadricula):
            print("Fuera del tablero")
        if(limpiar):
            self.limpiarSeleccionCeldas()

    def verificarMatches(self, ventana):
        '''Verifica la existencia de alineaciones\n
        a partir de 3 fichas'''
        celdas = self.__celdas
        alineaciones = []
        if(not self.__matches):
            alineaciones = self.handler.requestMatches()
            self.setMatches(True)
        if(len(alineaciones) != 0):
            for row in range(len(celdas)):
                for col in range(len(celdas[row])):
                    coord = (row, col)
                    # Marcar alineaciones horziontales
                    for alineacion in alineaciones[0]:
                        if(coord in alineacion):
                            celdas[row][col].setFichaAlineada(True)
                    # Marcar alineaciones verticales
                    for alineacion in alineaciones[1]:
                        if(coord in alineacion):
                            celdas[row][col].setFichaAlineada(True)
