# Enumeraciones

from enum import Enum


class TipoTexto(Enum):
    NO_ESPECIFICADO = 0
    INFO = 1
    TITULO = 2


class Colores(Enum):
    GRIS = (50, 50, 50)
    ROJO = (255, 56, 56)
    AZUL = (27, 61, 109)
    VERDE = (54, 175, 64)
    AMARILLO = (255, 184, 53)
    SELECCION = (0, 21, 20)
    ALINEACION = (251, 255, 241)
