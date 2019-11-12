# Clase ficha:
# Agrupa el tipo de ficha.
# Agrupa los estados de una ficha:
# Ninguno, alineada, seleccionada
# Además su animación: gravedad
from tipoficha import TipoFicha
from customEnums import Colores


class Ficha(object):
    def __init__(self, idTipo=0):
        self.__seleccionada = False
        self.__alineada = False
        self.__tipo = TipoFicha(idTipo)
        self.__color = self.setColor()

#  //
#  Métodos get-set
#  //

    def getSeleccionada(self):
        return self.__seleccionada

    def setSeleccionada(self, valor):
        '''Asigna valor booleano\n
        y setea el color correspondiente'''
        self.__seleccionada = valor
        self.setColor()

    def getTipo(self):
        return self.__tipo

    def getTipoInt(self):
        '''Devuelve el numero entero que identifica\n
        al tipo de ficha'''
        return self.__tipo.getId()

    def setTipo(self, tipo):
        '''Asigna el tipo\n
        y setea el color correspondiente'''
        self.__tipo = tipo
        self.setColor()

    def getAlineada(self):
        return self.__alineada

    def setAlineada(self, valor):
        '''Asigna valor booleano\n
        y setea el color correspondiente'''
        if(valor):
            self.setColor()
        self.__alineada = valor

# //
# Métodos para manipular el estado de la ficha
# //

    def setColor(self):
        '''Asigna el color a la ficha\n
        teniendo en cuenta si está seleccionada,\n
        alineada, o es No_especificada'''
        if(self.__alineada):
            self.__color = Colores.ALINEACION.value
            return Colores.ALINEACION.value
        elif(self.__seleccionada):
            self.__color = Colores.SELECCION.value
            return Colores.SELECCION.value
        else:
            self.__color = self.__tipo.getColor().value
            return self.__tipo.getColor().value

    def getColor(self):
        '''Devuelve el color de la ficha'''
        self.setColor()
        return self.__color

    def equals(self, otraFicha):
        return self.__tipo.getId() == otraFicha.getTipoInt()
