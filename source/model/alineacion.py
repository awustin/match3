# Clase Alineacion: se maneja como una Cola de alineaciones


class Alineacion(object):
    def __init__(self):
        self.__fichasSeleccionadas = []
        self.__ultimaSeleccionada = []
        self.__alineaciones = []
        self.__colaAlineaciones = []

    # Get - Set

    def getAlineaciones(self):
        return self.__alineaciones

    def getHorizontales(self):
        if(self.hayHorizontales()):
            return self.__alineaciones[0]

    def getVerticales(self):
        if(self.hayVerticales()):
            return self.__alineaciones[1]

    def getSeleccionadas(self):
        return self.__fichasSeleccionadas

    def get_selected(self, i=-1):
        if i == -1:
            return self.__fichasSeleccionadas
        if i < len(self.__fichasSeleccionadas):
            return self.__fichasSeleccionadas[i]
        return None

    # FIFO

    # Alineaciones
    def hayAlineaciones(self):
        return len(self.__alineaciones) != 0

    def hayHorizontales(self):
        return len(self.__alineaciones[0]) != 0

    def hayVerticales(self):
        return len(self.__alineaciones[1]) != 0

    def haySeleccionadas(self):
        return len(self.__fichasSeleccionadas) != 0

    def hayUnaSeleccionada(self):
        return len(self.__fichasSeleccionadas) == 1
    
    def agregarASeleccion(self, item):
        self.__fichasSeleccionadas.append(item)

    def limpiarSeleccion(self):
        self.__fichasSeleccionadas.clear()

    def clear_selected(self):
        self.__fichasSeleccionadas.clear()

    def buscarHorizontales(self, matriz, n):
        '''Busca las alineaciones horizontales. Argumentos:\n
        matriz = matriz a recorrer\n
        n = cantidad minima de elementos iguales\n
        Devuelve una lista de tuplas.'''
        self.__alineaciones = []
        alineacionesH = []
        alineadas = []
        horizontal = []
        cont = 0
        for row in range(len(matriz)):
            for col in range(len(matriz[row])):
                candidato = matriz[row][col]
                if(col == 0):
                    horizontal.append(candidato)
                    alineadas.append((row, col))
                    continue
                if((horizontal[0] - candidato) != 0):
                    if(len(horizontal) > n-1):
                        alineacionesH.append(alineadas)
                        cont = cont + 1
                    horizontal = []
                    alineadas = []
                horizontal.append(candidato)
                alineadas.append((row, col))
            if(len(horizontal) > n-1):
                alineacionesH.append(alineadas)
                cont = cont + 1
            horizontal = []
            alineadas = []
        self.__alineaciones.append(alineacionesH)
        return alineacionesH

    def buscarVerticales(self, matriz, n):
        '''Busca las alineaciones horizontales. Argumentos:\n
        matriz = matriz a recorrer\n
        n = cantidad minima de elementos iguales\n
        Devuelve una lista de tuplas.'''
        cont = 0
        alineacionesV = []
        alineadas = []
        vertical = []
        for col in range(len(matriz)):
            for row in range(len(matriz[col])):
                candidato = matriz[row][col]
                if(row == 0):
                    vertical.append(candidato)
                    alineadas.append((row, col))
                    continue
                if((vertical[0] - candidato) != 0):
                    if(len(vertical) > n-1):
                        alineacionesV.append(alineadas)
                        cont = cont + 1
                    vertical = []
                    alineadas = []
                vertical.append(candidato)
                alineadas.append((row, col))
            if(len(vertical) > n-1):
                alineacionesV.append(alineadas)
                cont = cont + 1
            vertical = []
            alineadas = []
        self.__alineaciones.append(alineacionesV)
        return alineacionesV

    def __forward(self, y, row):
        if y == 7:
            return 1
        if row[y] != row[y+1]:
            return 1
        count = 1 + self.__forward(y+1, row)
        return count

    def __back(self, y, row):
        if y == 0:
            return 0
        if row[y] != row[y-1]:
            return 0
        count = 1 + self.__back(y-1, row)
        return count

    def __down(self, x, y, array):
        if x == 7:
            return 1
        if array[x][y] != array[x+1][y]:
            return 1
        count = 1 + self.__down(x+1, y, array)
        return count

    def __up(self, x, y, array):
        if x == 0:
            return 0
        if array[x][y] != array[x-1][y]:
            return 0
        count = 1 + self.__up(x-1, y, array)
        return count

    def search_adjacent(self, x, y, temp_array):
        row = temp_array[x]
        count_forward = self.__forward(y, row)
        count_backward = self.__back(y, row)
        count_downward = self.__down(x, y, temp_array)
        count_upward = self.__up(x, y, temp_array)
        return [count_forward + count_backward, count_downward + count_upward]
