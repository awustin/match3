# Enumeraciones

from enum import Enum


class TipoTexto(Enum):
    NO_ESPECIFICADO = 0
    INFO = 1
    TITULO = 2


class TipoFicha(Enum):
    NO_ESPECIFICADO = 0
    CIRCULO_AM = 1
    CIRCULO_AZ = 2
    CIRCULO_R = 3
    CIRCULO_V = 4
