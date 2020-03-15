# Board
# Celdas de 50x50 (8x8 celdas)
import sys
from pygame import sprite
from handler import Handler
from celda import Celda
# from model.score import Score
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
X_OFF = (globales.DIMENSION[0] - X_CUAD) / 2 + 70
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
        self.__base_color = color
        self.__cells_array = []
        self.__cells_ready = False
        self.__chips_spr_group = sprite.Group()
        self.__aligned_list = []

    def get_aligned_list(self):
        return self.__aligned_list

    def clear_aligned_list(self):
        self.__aligned_list = []

    def get_cells(self):
        '''Devuelve la matriz de celdas'''
        return self.__cells_array

    def get_chips(self, coord_list):
        '''Arguments: \n
        list: is a list of tuples (row, col)'''
        chip_list = []
        if coord_list != [] and coord_list is not None:
            for coord in coord_list:
                chip = self.__cells_array[coord[0]][coord[1]].get_cell_content()
                chip_list.append(chip)
        return chip_list

    def clear_cells_array(self):
        self.__cells_array.clear()
        self.__cells_array = []

    def restart_chips(self):
        '''Reinicia el calculador:\n
        Vacia la lista de alineadas\n
        Vacia la lista de seleccion\n
        Recarga una matriz de enteros random\n'''
        self.handler.restart_chips()

    def restart_board(self):
        '''Vacía la matriz de celdas,\n
        Vacía la matriz de fichas\n
        Pone las banderas en su estado inicial'''
        self.clear_cells_array()
        self.restart_chips()
        self.__aligned_list = []
        self.__cells_ready = False
        self.__chips_spr_group.empty()
        self.__base_color = (random()*255, random()*255, random()*255)

    def __gradient(self, color):
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

    def start_board(self, fichas):
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
            self.__cells_array.append([])
            for col in range(len(fichas[row])):
                color = self.__gradient(color)
                celda = Celda(X_CELDA, X_CELDA, col*(X_CELDA+X_SPACING) +
                              X_OFF, row*(X_CELDA+X_SPACING) + Y_OFF,
                              color)
                celda.setColorCelda(color)
                celda.setCoord(row, col)
                celda.setFicha(ficha=fichas[row][col])
                self.__cells_array[row].append(celda)
                if(row == len(self.__cells_array)-1
                   and col == len(self.__cells_array[row])-1):
                    self.__cells_ready = True
        self.__view.draw_cells(self.__cells_array)
        self.__view.draw_initial_chips(fichas)

    def scan_alignments(self):
        '''Pide que se determinen las alineaciones.
        El calculador revisa su lista de alineaciones'''
        self.update_chips_calculator()
        if(self.__aligned_list == []):
            self.__aligned_list = self.handler.buscarAlineaciones()

    def asign_new_origin_cells(self, columnas):
        '''A las fichas que ya existen y ya cayeron,
        les es asignada su celda origen'''
        for col in columnas:
            for row in reversed(range(N_CELDAS)):
                ficha = self.__cells_array[row][col].get_cell_content()
                if(ficha is not None):
                    celdaDestino = ficha.get_target_cell()
                    if(celdaDestino is not None):
                        celdaOrigen = ficha.get_origin_cell()
                        celdaOrigen.pasarFicha(celdaDestino)
                        ficha.set_target_cell(None)
                        ficha.set_origin_cell(celdaDestino)

    def update_chips_calculator(self):
        '''Tras un pasaje de fichas por un alineacion,
        se envia al calculador la nueva configuracion'''
        enteros = []
        for row in range(len(self.__cells_array)):
            enteros.append([])
            for col in range(len(self.__cells_array[row])):
                if(self.__cells_array[row][col].hayFicha()):
                    ficha = self.__cells_array[row][col].get_cell_content()
                    token_class = ficha.get_class()
                    enteros[row].append(token_class)
                else:
                    enteros[row].append(-1)
        self.handler.enviarConfiguracionTablero(enteros)
        return enteros

    def pass_chips_between_cells(self, columnas):
        '''Las fichas eliminadas dejan agujeros.
        las fichas que estan encima, empiezan a caer ocupando
        su lugar\n
        Usa la lista de tuplas (celdaOrigen, celdaDestino)
        entre las que se deben pasar las fichas'''
        celdas = self.__cells_array
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
                        celdaDestino = self.__cells_array[row + agujerosDebajo][col]
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
        self.__view.draw_falling_chips(self.__cells_array, self.__chips_spr_group)
        self.asign_new_origin_cells(columnas)

    def kill_aligned_chip(self, row, col):
        if self.__cells_array[row][col].hayFicha():
            self.__cells_array[row][col].kill_chip()

    def row_has_holes(self, fila):
        has_holes = False
        for celda in self.__cells_array[fila]:
            if(not celda.hayFicha()):
                has_holes = True
                break
        return has_holes

    def new_chips_per_row(self):
        '''Pide al calculador las nuevas fichas
        para completar el tablero'''
        self.update_chips_calculator()
        for row in reversed(range(len(self.__cells_array))):
            if(self.row_has_holes(row)):
                nuevaFila = self.handler.requestNuevasFichasPorFila(row)
                for col in range(len(nuevaFila)):
                    posicionAparecen = self.__cells_array[0][col]. \
                                       get_center_pos()
                    if(nuevaFila[col] is not None):
                        ficha = nuevaFila[col]
                        celdaDestino = self.__cells_array[row][col]
                        ficha.set_center_pos(*posicionAparecen)
                        ficha.set_target_cell(celdaDestino)
                        ficha.set_target_position(
                              celdaDestino.get_center_pos()[1])
                        ficha.set_initial_speed(VELOCIDAD_RELLENO)
                        self.add_chips_to_group(ficha)
                        ficha.set_dropped(True)
                        self.__view.draw_filling_board(nuevaFila,
                                                       self.__cells_array,
                                                       self.__chips_spr_group)
                for ficha in nuevaFila:
                    if(ficha is not None):
                        celdaDestino = ficha.get_target_cell()
                        celdaDestino.setFicha(ficha=ficha)
                        ficha.set_target_cell(None)
                        ficha.set_origin_cell(celdaDestino)
        self.update_chips_calculator()

    def complete_chips_scan(self):
        '''Actualiza el tablero. Sin pedir fichas al calculador.
        Si está completo (ya se dibujaron todas las celdas),
        recorre la matriz de celdas en busca de cambios de
        estado.'''
        celdas = self.__cells_array
        for row in range(len(celdas)):
            for col in range(len(celdas[row])):
                celda = celdas[row][col]
                if(celda.hayFicha()):
                    '''La ficha existe'''
                    self.add_chips_to_group(celda.get_cell_content())
                else:
                    '''La ficha se eliminó'''
                    self.__cells_array[row][col].borrarFicha()

    def add_chips_to_group(self, fichas):
        try:
            for row in fichas:
                for ficha in row:
                    if(ficha is not None):
                        self.__chips_spr_group.add(fichas)
        except TypeError:
            if(fichas is not None):
                self.__chips_spr_group.add(fichas)

    def main_board_update(self):
        ''' Actualiza el tablero, segun el estado de las fichas
        y las alineaciones.\n
        El programa principal debe llamar a esta función en cada iteración'''
        if(not self.__cells_ready):
            fichas = self.handler.requestFichas(N_CELDAS)
            self.add_chips_to_group(fichas)
            self.start_board(fichas)
        else:
            if(self.__aligned_list != []):
                return self.__aligned_list
            self.update_chips_calculator()
            self.complete_chips_scan()
            self.scan_alignments()
            self.__view.draw_cells(self.__cells_array)
            self.__view.update_chips(self.__chips_spr_group)
        return []

    def unselect_all_cells(self):
        '''Recorre la matriz de celdas y deselecciona
        una por una'''
        for row in range(len(self.__cells_array)):
            for col in range(len(self.__cells_array[row])):
                celda = self.__cells_array[row][col]
                if(celda.hayFicha()):
                    celda.deseleccionarFicha()

    def clear_selection(self):
        '''Vacia la lista de seleccionadas en el calculador \n
        Deselecciona todas las celdas del tablero \n
        Setea el valor de 'matches' a False'''
        self.handler.clear_selection()
        self.unselect_all_cells()
        self.__aligned_list = []

    def chips_swap(self, x1, y1, x2, y2):
        '''Intercambia las fichas entre las celdas'''
        celda1 = self.__cells_array[x1][y1]
        celda2 = self.__cells_array[x2][y2]
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
        fichasSwapping.append(ficha1)
        fichasSwapping.append(ficha2)
        # Actualizar durante animacion
        self.__view.draw_swapping_chips(self.__cells_array, fichasSwapping,
                                        self.__chips_spr_group)
        # Setear celdaOrigen
        ficha1.set_origin_cell(celda2)
        ficha2.set_origin_cell(celda1)
        ficha1.set_target_cell(None)
        ficha2.set_target_cell(None)
        celda1.setFicha(ficha=ficha2)
        celda2.setFicha(ficha=ficha1)

    def click_action(self, x, y):
        '''Busca cuál fue la casilla clickeada
        y dispara la lógica de selección de las fichas'''
        limpiar = False
        dentroCuadricula = False
        fichas = self.handler.requestFichas(N_CELDAS)
        for row in range(len(fichas)):
            if(limpiar):
                break
            for col in range(len(fichas[row])):
                celda = self.__cells_array[row][col]
                if(celda.esClickeada(x, y) and celda.hayFicha()):
                    dentroCuadricula = True
                    token_class = self.__cells_array[row][col].get_cell_content() \
                        .get_class()
                    if(token_class in NOT_CLICKABLE):
                        break
                    estadoFicha = self.handler.seleccionFichasYEstado(row, col)
                    if(estadoFicha['seleccionada']):
                        celda.seleccionarFicha()
                    else:
                        p0 = estadoFicha['anterior']
                        if(p0 is not None):
                            self.__cells_array[p0[0]][p0[1]].deseleccionarFicha()
                        celda.deseleccionarFicha()
                    if(estadoFicha['swap']):
                        p0 = estadoFicha['anterior']
                        self.chips_swap(row, col, p0[0], p0[1])
                        self.update_chips_calculator()
                        limpiar = True
                        break
                    break
        if(not dentroCuadricula):
            print("Fuera del tablero")
        if(limpiar):
            self.clear_selection()

    def locate_selector(self, x, y):
        for row in range(len(self.__cells_array)):
            for col in range(len(self.__cells_array[row])):
                celda = self.__cells_array[row][col]
                if(celda.getRect().collidepoint(x, y)):
                    return (row, col)
