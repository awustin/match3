# Clase Tipo Ficha
from customEnums import Colores


class TipoFicha(object):
    def __init__(self, id=0):
        self.__id = id
        self.__color = self.colorTipo(id)

    def colorTipo(self, i):
        if(i == 0):
            return Colores.GRIS
        elif(i == 1):
            return Colores.ROJO
        elif(i == 2):
            return Colores.AZUL
        elif(i == 3):
            return Colores.VERDE
        elif(i == 4):
            return Colores.AMARILLO
        else:
            print("Tipo Invalido")
            return None

    def getId(self):
        return self.__id

    def getColor(self):
        return self.__color
