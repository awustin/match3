# Clase Texto
import pygame
from pygame import font
import customEnums


class Texto(object):
    def __init__(self, string, fuente=None,
                 colorRGB=(0, 0, 0),
                 tipo=customEnums.TipoTexto.NO_ESPECIFICADO):
        self.__tipo = tipo
        if(tipo == customEnums.TipoTexto.NO_ESPECIFICADO):
            self.__fontObject = font.Font(fuente, 12)
        elif(tipo == customEnums.TipoTexto.TITULO):
            self.__fontObject = font.Font(fuente, 45)
        elif(tipo == customEnums.TipoTexto.INFO):
            self.__fontObject = font.Font(fuente, 9)
        self.__surfObject = self.__fontObject.render(str(string), 1, colorRGB)

    def getFont(self):
        return self.__fontObject

    def getSurface(self):
        return self.__surfObject

    def setPosicion(self, *coord):
        self.__pos = coord

    def getPosicion(self):
        if(self.__pos is not None):
            return self.__pos
        else:
            return -1

    @staticmethod
    def customFontTitulo(fuente):
        return font.Font(fuente, 45)

    @staticmethod
    def customFontInfo(fuente):
        return pygame.font.Font(fuente, 12)
