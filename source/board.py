# Board
# Celdas de 50x50 (8x8 celdas)
import sys
import pygame
from pygame import draw
from pygame import time
from pygame import sprite
from handler import Handler
from celda import Celda
from random import random

sys.path.insert(0, 'config')
try:
    import globales
except Exception as e:
    print(e)
    raise

X_CUAD = 480
Y_CUAD = X_CUAD
BASE_CELL_COLOR = (20, 40, 80)
BKG_COLOR = (120, 100, 50)
X_OFF = (globales.DIMENSION[0] - X_CUAD) / 2
Y_OFF = (globales.DIMENSION[1] - Y_CUAD) / 2
N_CELDAS = 8
X_CELDA = X_CUAD/N_CELDAS
X_SPACING = 5
VELOCIDAD_CAIDA = 7
VELOCIDAD_RELLENO = 10
NOT_CLICKABLE = [-1, -2]


class Board:
    def __init__(self, viewer, tam=(X_CUAD, X_CUAD), color=BASE_CELL_COLOR):
        self.handler = Handler(N_CELDAS)
        self.__view = viewer
        self.__color_base = color
        self.__celdas = []
        self.__celdasEstanCompletas = False
        self.__grupoFichas = sprite.Group()
        self.__alineaciones = []
        self.__matches = False
        self.__fichasEntreCeldas = []
        self.__estanCayendo = False
        self.__estanSwapping = False

    def getCeldas(self):
        '''Devuelve la matriz de celdas'''
        return self.__celdas

    def reiniciarMatrizCeldas(self):
        self.__celdas.clear()
        self.__celdas = []

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
        self.__matches = False
        self.__celdasEstanCompletas = False
        self.__grupoFichas.empty()
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

    def generarTableroFilaPorFila(self, fichas):
        ''' Cuando las celdas no estén completas, se deberá
        generarlas.\n
        Luego, se pide la matriz de fichas random\n
        Luego, se completa fila a fila, empezando por la ultima.\n
        ventana es una Surface\n
        n es el numero de filas (igual al de columnas)\n
        x_celda es el tamaño de la celda\n
        x_espaciado es el ancho del espaciado entre celdas\n
        color_base es el color base de la celda'''
        color = BASE_CELL_COLOR
        for row in range(len(fichas)):
            self.__celdas.append([])
            for col in range(len(fichas[row])):
                color = self.gradiente(color)
                celda = Celda(X_CELDA, X_CELDA, col*(X_CELDA+X_SPACING) +
                              X_OFF, row*(X_CELDA+X_SPACING) + Y_OFF,
                              color)
                celda.setColorCelda(color)
                celda.setCoord(row, col)
                celda.setFicha(ficha=fichas[row][col])
                self.__celdas[row].append(celda)
                if(row == len(self.__celdas)-1
                   and col == len(self.__celdas[row])-1):
                    self.__celdasEstanCompletas = True
        self.__view.draw_cells(self.__celdas)
        self.__view.draw_initial_chips(fichas)

    def buscarAlineacionFichas(self):
        '''Pide que se determinen las alineaciones.
        El calculador revisa su lista de alineaciones'''
        self.enviarActualizacionAlineaciones()
        if(self.__alineaciones == []):
            alineaciones = self.handler.buscarAlineaciones()
            if(not alineaciones):
                return False
            else:
                self.__alineaciones = alineaciones
                return True
        else:
            return True

    def actualizarTableroCaenFichas(self, ventana, colorFondo):
        '''Actualiza el tablero para la transición de
        la caida de fichas'''
        while(self.__estanCayendo):
            ventana.fill(colorFondo)
            celdas = self.__celdas
            for row in range(len(celdas)):
                for col in range(len(celdas[row])):
                    celda = celdas[row][col]
                    draw.rect(ventana, celda.getColorCelda(), celda.getRect())
            for ficha in self.__grupoFichas:
                self.__estanCayendo = False
                if(ficha.is_falling()):
                    self.__estanCayendo = True
                    break
            self.__grupoFichas.update(ventana)
            pygame.display.update()

    def asignarANuevasCeldas(self, columnas):
        '''A las fichas que ya existen y ya cayeron,
        les es asignada su celda destino'''
        for col in columnas:
            for row in reversed(range(N_CELDAS)):
                ficha = self.__celdas[row][col].get_cell_content()
                if(ficha is not None):
                    celdaDestino = ficha.get_target_cell()
                    if(celdaDestino is not None):
                        celdaOrigen = ficha.get_origin_cell()
                        celdaOrigen.pasarFicha(celdaDestino)
                        ficha.set_target_cell(None)
                        ficha.set_origin_cell(celdaDestino)

    def enviarActualizacionAlineaciones(self):
        '''Tras un pasaje de fichas por un alineacion,
        se envia al calculador la nueva configuracion'''
        enteros = []
        for row in range(len(self.__celdas)):
            enteros.append([])
            for col in range(len(self.__celdas[row])):
                if(self.__celdas[row][col].hayFicha()):
                    ficha = self.__celdas[row][col].get_cell_content()
                    token_class = ficha.get_class()
                    enteros[row].append(token_class)
                else:
                    enteros[row].append(-1)
        self.handler.enviarConfiguracionTablero(enteros)
        return enteros

    def ocuparAgujeros(self, columnas):
        '''Las fichas eliminadas dejan agujeros.
        las fichas que estan encima, empiezan a caer ocupando
        su lugar\n
        Usa la lista de tuplas (celdaOrigen, celdaDestino)
        entre las que se deben pasar las fichas'''
        celdas = self.__celdas
        for col in columnas:
            for row in range(N_CELDAS):
                celdaOrigen = celdas[row][col]
                if(celdaOrigen.hayFicha()):
                    agujerosDebajo = 0
                    j = row
                    while(j < N_CELDAS):
                        if(not celdas[j][col].hayFicha()):
                            agujerosDebajo += 1
                        j += 1
                    if(agujerosDebajo != 0):
                        celdaDestino = self.__celdas[row + agujerosDebajo][col]
                        celdaOrigen.get_cell_content().set_target_position(
                                              celdaDestino.
                                              get_center_pos()[1])
                        celdaOrigen.get_cell_content().set_initial_speed(
                                               VELOCIDAD_CAIDA)
                        celdaOrigen.get_cell_content().set_dropped(True)
                        celdaOrigen.get_cell_content() \
                            .set_origin_cell(celdaOrigen)
                        celdaOrigen.get_cell_content() \
                            .set_target_cell(celdaDestino)
                        self.__estanCayendo = True
        self.__view.draw_falling_chips(self.__celdas, self.__grupoFichas)
        # self.actualizarTableroCaenFichas(ventana, colorFondo)
        self.asignarANuevasCeldas(columnas)

    def eliminarFichasAlineadas(self):
        '''Elimina las fichas que se alinearon,
        y devuelve un conjunto con las columnas
        que tienen agujeros'''
        horizontales = self.__alineaciones[0]
        verticales = self.__alineaciones[1]
        columnasConAgujeros = set()
        for alineacion in horizontales:
            for item in alineacion:
                row = item[0]
                col = item[1]
                ficha = self.__celdas[row][col].get_cell_content()
                ficha.kill()
                self.__celdas[row][col].borrarFicha()
                columnasConAgujeros.add(col)
        for alineacion in verticales:
            for item in alineacion:
                row = item[0]
                col = item[1]
                if(self.__celdas[row][col].hayFicha()):
                    ficha = self.__celdas[row][col].get_cell_content()
                    ficha.kill()
                    self.__celdas[row][col].borrarFicha()
                columnasConAgujeros.add(col)
        self.__alineaciones = []
        return columnasConAgujeros

    def filaTieneAgujeros(self, fila):
        tieneAgujeros = False
        for celda in self.__celdas[fila]:
            if(not celda.hayFicha()):
                tieneAgujeros = True
                break
        return tieneAgujeros

    def actualizarFilaCaenNuevasFichas(self, ventana, colorFondo, nuevaFila):
        '''Actualiza la fila para la transición de
        la caida de fichas cuando hay nuevas fichas que rellenan agujeros'''
        while(self.__estanCayendo):
            ventana.fill(colorFondo)
            celdas = self.__celdas
            for row in range(len(celdas)):
                for col in range(len(celdas[row])):
                    celda = celdas[row][col]
                    draw.rect(ventana, celda.getColorCelda(), celda.getRect())
            for ficha in nuevaFila:
                if(ficha is not None):
                    self.__estanCayendo = False
                    if(ficha.is_falling()):
                        self.__estanCayendo = True
                        break
            self.__grupoFichas.update(ventana)
            pygame.display.update()

    def nuevasFichasPorFilas(self):
        '''Pide al calculador las nuevas fichas
        para completar el tablero'''
        self.enviarActualizacionAlineaciones()
        for row in reversed(range(len(self.__celdas))):
            if(self.filaTieneAgujeros(row)):
                nuevaFila = self.handler.requestNuevasFichasPorFila(row)
                for col in range(len(nuevaFila)):
                    posicionAparecen = self.__celdas[0][col]. \
                                       get_center_pos()
                    if(nuevaFila[col] is not None):
                        ficha = nuevaFila[col]
                        celdaDestino = self.__celdas[row][col]
                        ficha.set_center_pos(*posicionAparecen)
                        ficha.set_target_cell(celdaDestino)
                        ficha.set_target_position(
                              celdaDestino.get_center_pos()[1])
                        ficha.set_initial_speed(VELOCIDAD_RELLENO)
                        self.agregarFichasAGrupo(ficha)
                        ficha.set_dropped(True)
                        self.__estanCayendo = True
                        self.__view.draw_filling_board(nuevaFila,
                                                       self.__celdas,
                                                       self.__grupoFichas)
                for ficha in nuevaFila:
                    if(ficha is not None):
                        celdaDestino = ficha.get_target_cell()
                        celdaDestino.setFicha(ficha=ficha)
                        ficha.set_target_cell(None)
                        ficha.set_origin_cell(celdaDestino)
        self.enviarActualizacionAlineaciones()

    def alineacionEnTablero(self):
        if(self.__alineaciones != []):
            columnas = self.eliminarFichasAlineadas()
            self.ocuparAgujeros(columnas)
            self.nuevasFichasPorFilas()
        self.__alineaciones = []
        self.__matches = False

    def actualizarTableroCompleto(self):
        '''Actualiza el tablero. Sin pedir fichas al calculador.
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
                if(celda.hayFicha()):
                    '''La ficha existe'''
                    self.agregarFichasAGrupo(celda.get_cell_content())
                else:
                    '''La ficha se eliminó'''
                    self.__celdas[row][col].borrarFicha()

    def agregarFichasAGrupo(self, fichas):
        try:
            for row in fichas:
                for ficha in row:
                    if(ficha is not None):
                        self.__grupoFichas.add(fichas)
        except TypeError:
            if(fichas is not None):
                self.__grupoFichas.add(fichas)

    def main_board_update(self):
        ''' Actualiza el tablero, segun el estado de las fichas
        y las alineaciones.\n
        El programa principal debe llamar a esta función en cada iteración'''
        if(not self.__celdasEstanCompletas):
            fichas = self.handler.requestFichas(N_CELDAS)
            self.agregarFichasAGrupo(fichas)
            self.generarTableroFilaPorFila(fichas)
        else:
            if(self.__matches):
                return self.__matches
            self.enviarActualizacionAlineaciones()
            self.actualizarTableroCompleto()
            self.__matches = self.buscarAlineacionFichas()
            self.__view.draw_cells(self.__celdas)
            self.__view.update_chips(self.__grupoFichas)

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

    def actualizarTableroSwapping(self, ventana, colorFondo, swapping):
        '''Actualiza el tablero mientras se intercambian fichas'''
        while(self.__estanSwapping):
            ventana.fill(colorFondo)
            celdas = self.__celdas
            for row in range(len(celdas)):
                for col in range(len(celdas[row])):
                    celda = celdas[row][col]
                    draw.rect(ventana, celda.getColorCelda(), celda.getRect())
            for ficha in swapping:
                if(ficha is not None):
                    self.__estanSwapping = False
                    if(ficha.is_swapping()):
                        self.__estanSwapping = True
                        break
            self.__grupoFichas.update(ventana)
            pygame.display.update()

    def swapFichas(self, x1, y1, x2, y2):
        '''Intercambia las fichas entre las celdas'''
        celda1 = self.__celdas[x1][y1]
        celda2 = self.__celdas[x2][y2]
        fichasSwapping = []
        # Asignar ficha origen y destino: Ficha 1
        ficha1 = celda1.get_cell_content()
        ficha1.set_origin_cell(celda1)
        ficha1.set_target_cell(celda2)
        ficha1.set_swapping(True)
        # Asignar ficha origen y destino: Ficha 2
        ficha2 = celda2.get_cell_content()
        ficha2.set_origin_cell(celda2)
        ficha2.set_target_cell(celda1)
        ficha2.set_swapping(True)
        self.__estanSwapping = True
        fichasSwapping.append(ficha1)
        fichasSwapping.append(ficha2)
        # Actualizar durante animacion
        self.__view.draw_swapping_chips(self.__celdas, fichasSwapping,
                                        self.__grupoFichas)
        # Setear celdaOrigen
        ficha1.set_origin_cell(celda2)
        ficha2.set_origin_cell(celda1)
        ficha1.set_target_cell(None)
        ficha2.set_target_cell(None)
        celda1.setFicha(ficha=ficha2)
        celda2.setFicha(ficha=ficha1)

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
                    token_class = self.__celdas[row][col].get_cell_content() \
                        .get_class()
                    if(token_class in NOT_CLICKABLE):
                        break
                    estadoFicha = self.handler.seleccionFichasYEstado(row, col)
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

    def posicionarSelector(self, x, y):
        for row in range(len(self.__celdas)):
            for col in range(len(self.__celdas[row])):
                celda = self.__celdas[row][col]
                if(celda.getRect().collidepoint(x, y)):
                    return (row, col)
