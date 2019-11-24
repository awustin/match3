# Clase Tipo Ficha
import pygame
from customEnums import Colores


class TipoFicha(object):
    def __init__(self, id=0):
        self.__id = id
        self.__color = self.colorTipo(id)
        self.__image = self.imageTipo(id)

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
    
    def imageTipo(self, i):
        if(i == 0):
            return Colores.GRIS
        elif(i == 1):
            return pygame.image.load('.\\data\\images\\ficha1.png')
        elif(i == 2):
            return pygame.image.load('.\\data\\images\\ficha2.png')
        elif(i == 3):
            return pygame.image.load('.\\data\\images\\ficha3.png')
        elif(i == 4):
            return pygame.image.load('.\\data\\images\\ficha4.png')
        else:
            print("Tipo Invalido")
            return None

    def getId(self):
        return self.__id
    
    def getImage(self):
        return self.__image
