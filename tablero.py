# Tablero
# Celdas de 50x50 (8x8 celdas)
import pygame
from pygame import draw
from pygame import gfxdraw
from pygame import time
from pygame import sprite
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
GRAVEDAD = 0.5
RESOLUCION = 1


class Tablero:
    def __init__(self, tam=(X_CUAD, X_CUAD), color=(1, 1, 1)):
        self.handler = Handler(N_CELDAS)
        self.__color_base = color
        self.__celdas = []
        self.__celdasEstanCompletas = False
        self.__grupoFichas = sprite.Group()
        self.__matches = False
        self.__seAnularon = False

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
                celda.setCoord(row, col)
                rect = celda.getRect()
                draw.rect(ventana, color, rect)
                self.__celdas[row].append(celda)
        pygame.display.update()
        for row in reversed(range(len(fichas))):
            for col in range(len(fichas)):
                celda = self.__celdas[row][col]
                centro = celda.getPosicionCentro()
                fichas[row][col].setPosicionCentro(*centro)
                celda.setFicha(ficha=fichas[row][col])
                time.wait(7)
                fichas[row][col].update(ventana)
                pygame.display.update()
                if(row == len(self.__celdas)-1
                   and col == len(self.__celdas[row])-1):
                    self.setCompleto(True)

    def buscarAlineacionFichas(self):
        '''Pide que se determinen las alineaciones.
        El calculador revisa su lista de alineaciones'''
        return self.handler.buscarAlineaciones()

    def anularFichasAlineadas(self):
        '''Pide que se anulen las fichas alineadas.
        Las setea en -1.'''
        self.__seAnularon = self.handler.anularFichasAlineadas()

    def actualizarFilaCaenFichas(self, ventana, celdas):
        '''Actualiza la fila mientras caen fichas'''
        rect = []
        for celda in celdas:
            rect.append(celda.getRect())
        pygame.display.update(rect)
        for celda in celdas:
            centro = celda.getPosicionCentro()
            if(celda.hayFicha()):
                colorFicha = celda.getColorFicha()
                gfxdraw.aacircle(ventana, *centro, 15, colorFicha)
                gfxdraw.filled_circle(ventana, *centro, 15, colorFicha)
            pygame.display.update()

    def actualizarTableroCaenFichas(self, ventana):
        '''Actualiza el tablero sin pedir al calculador la
        matriz de fichas. Sirve para estados de transición como
        la caida de fichas'''
        celdas = self.__celdas
        for row in range(len(celdas)):
            for col in range(len(celdas[row])):
                celda = celdas[row][col]
                centro = celda.getPosicionCentro()
                draw.rect(ventana, celda.getColorCelda(), celda.getRect())
                if(celda.hayFicha()):
                    colorFicha = celda.getColorFicha()
                    gfxdraw.aacircle(ventana, *centro, 15, colorFicha)
                    gfxdraw.filled_circle(ventana, *centro, 15, colorFicha)

    def fichasCaen(self, ventana, colorFondo, row, col):
        celdas = self.__celdas
        celdaInicio = self.__celdas[row][col]
        celdaFinal = self.__celdas[row+1][col]
        pos = celdaInicio.getPosicionCentro()
        final = celdaFinal.getPosicionCentro()
        t = 0
        y = pos[1]
        while(y <= final[1]):
            ventana.fill(colorFondo)
            for row in range(len(celdas)):
                for col in range(len(celdas[row])):
                    celda = celdas[row][col]
                    centro = celda.getPosicionCentro()
                    draw.rect(ventana, celda.getColorCelda(), celda.getRect())
                    if(celda.hayFicha() and not celda.sueltaFicha()):
                        colorFicha = celda.getColorFicha()
                        gfxdraw.aacircle(ventana, *centro, 15, colorFicha)
                        gfxdraw.filled_circle(ventana, *centro, 15, colorFicha)
            y = pos[1] + GRAVEDAD*pow(t, 2)
            y = int(y)
            t = t + RESOLUCION
            nuevaPos = (pos[0], y)
            if(celdaInicio.hayFicha()):
                colorFicha = celdaInicio.getColorFicha()
                gfxdraw.aacircle(ventana, *nuevaPos, 15, colorFicha)
                gfxdraw.filled_circle(ventana, *nuevaPos, 15, colorFicha)

    def pasarFichasEntreCeldasPorColumna(self, n, col, ventana, colorFondo):
        ''' 'n' es la fila desde la que empieza el recorrido.\n
        'col' es la columna actual'''
        celdas = self.__celdas
        for i in reversed(range(n)):
            if(celdas[i][col].hayFicha()):
                j = i
                while(j != n):
                    if(not celdas[j+1][col].hayFicha()):
                        self.__celdas[j][col].setSueltaFicha(True)
                        self.fichasCaen(ventana, colorFondo, j, col)
                        self.__celdas[j][col].pasarFicha(self.__celdas[j+1][col])
                        self.actualizarFilaCaenFichas(ventana, self.__celdas[j])
                        self.actualizarFilaCaenFichas(ventana, self.__celdas[j+1])
                    j = j + 1

    def pasarFichasEntreCeldas(self, ventana, colorFondo):
        for col in range(N_CELDAS):
            self.pasarFichasEntreCeldasPorColumna(N_CELDAS-1, col, ventana, colorFondo)
        self.enviarActualizacionAlineaciones()

    def enviarActualizacionAlineaciones(self):
        '''Tras un pasaje de fichas por un alineacion,
        se envia al calculador la nueva configuracion'''
        enteros = []
        for row in range(len(self.__celdas)):
            enteros.append([])
            for col in range(len(self.__celdas[row])):
                if(self.__celdas[row][col].hayFicha()):
                    ficha = self.__celdas[row][col].getFicha()
                    tipo = ficha.getTipoInt()
                    enteros[row].append(tipo)
                else:
                    enteros[row].append(-1)
        self.handler.enviarConfiguracionTablero(enteros)

    def actualizarConFichas(self, ventana):
        fichas = self.handler.requestFichas(N_CELDAS)
        self.actualizarTableroCompleto(ventana, X_CELDA, 5, fichas)
        pygame.display.update()
        return fichas

    def rellenarCeldasPorColumna(self, ventana):
        '''En cada columna, pone nuevas fichas'''
        celdas = self.__celdas
        self.enviarActualizacionAlineaciones()
        for col in range(N_CELDAS):
            columnaFichasNuevas = self.handler.requestRellenoColumna(col)
            for i in reversed(range(len(columnaFichasNuevas))):
                ficha = columnaFichasNuevas[i]
                if(not celdas[i][col].hayFicha()):
                    self.__celdas[i][col].setFicha(ficha=ficha)
                    self.actualizarFilaCaenFichas(ventana, self.__celdas[i])
        self.enviarActualizacionAlineaciones()

    def alineacionEnTablero(self, ventana):
        self.anularFichasAlineadas()
        self.actualizarConFichas(ventana)
        '''Las celdas se pasan las fichas.'''
        '''Las fichas caen'''
        '''Se transmite la nueva información al calculador'''
        self.__matches = False

    def actualizarTableroCompleto(self, ventana, x_celda, x_espaciado, fichas):
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
                        celda.getFicha().setPosicionCentro(*centro)
                        #self.agregarFichasAGrupo(celda.getFicha())
                    centro = celda.getPosicionCentro()
                    celda.getFicha().setPosicionCentro(*centro)
                    self.agregarFichasAGrupo(celda.getFicha())
                    draw.rect(ventana, celda.getColorCelda(), celda.getRect())
                else:
                    '''La ficha se eliminó'''
                    self.__celdas[row][col].borrarFicha()
                    draw.rect(ventana, celda.getColorCelda(), celda.getRect())
        self.__grupoFichas.update(ventana)

    def agregarFichasAGrupo(self, fichas):
        try:
            for row in fichas:
                for ficha in row:
                    if(ficha is not None):
                        self.__grupoFichas.add(fichas)
        except TypeError:
            if(fichas is not None):
                self.__grupoFichas.add(fichas)

    def actualizarTableroConEstado(self, ventana):
        ''' Actualiza el tablero, segun el estado de las fichas
        y las alineaciones.
        El programa principal debe llamar a esta función en cada iteración'''        
        color_base = self.__color_base
        if(not self.__celdasEstanCompletas):
            fichas = self.handler.requestFichas(N_CELDAS)  # refactor 1
            self.agregarFichasAGrupo(fichas)
            self.generarTableroFilaPorFila(ventana, X_CELDA, 5, color_base,
                                           fichas)  # refactor 2
        else:
            if(self.__matches):
                return self.__matches
            fichas = self.handler.requestFichas(N_CELDAS)  # refactor 1
            self.actualizarTableroCompleto(ventana, X_CELDA, 5, fichas)  # refactor 3
            self.__matches = self.buscarAlineacionFichas()

    def deseleccionarTodasCeldas(self):
        '''Recorre la matriz de celdas y deselecciona
        una por una'''
        for row in range(len(self.__celdas)):
            for col in range(len(self.__celdas[row])):
                celda = self.__celdas[row][col]
                if(celda.hayFicha()):
                    celda.deseleccionarFicha()

    def limpiarSeleccionCeldas(self):
        '''Vacia la lista de seleccionadas en el calculador \n
        Deselecciona todas las celdas del tablero \n
        Setea el valor de 'matches' a False'''
        self.handler.limpiarSeleccion()
        self.deseleccionarTodasCeldas()
        self.__matches = False

    def swapFichas(self, x1, y1, x2, y2):
        '''Intercambia las fichas entre las celdas'''
        ficha1 = self.__celdas[x1][y1].getFicha()
        self.__celdas[x1][y1].setFicha(ficha=self.__celdas[x2][y2].getFicha())
        self.__celdas[x2][y2].setFicha(ficha=ficha1)

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
                if(celda.esClickeada(x, y) and celda.hayFicha()):
                    dentroCuadricula = True
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
                        p0 = estadoFicha['anterior']
                        self.swapFichas(row, col, p0[0], p0[1])
                        self.enviarActualizacionAlineaciones()
                        limpiar = True
                        break
                    break
        if(not dentroCuadricula):
            print("Fuera del tablero")
        if(limpiar):
            self.limpiarSeleccionCeldas()
