import sys
import customEnums
from viewport import Viewport
from view.texto import Texto

sys.path.insert(0, 'config')
try:
    import globales
except Exception as e:
    print(e)
    raise


class DisplayView():
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if DisplayView.__instance is None:
            DisplayView()
        return DisplayView.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.__viewport = None
        if DisplayView.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DisplayView.__instance = self

    def get_display(self):
        return self.__viewport

    def init_welcome_screen(self):
        self.__viewport = Viewport(*globales.DIMENSION)
        self.__viewport.init_viewport(globales.LOGO, globales.CAPTION)
        self.__viewport.bkg_color(globales.COLOR_FONDO)
        self.init_welcome_text()

    def init_welcome_text(self):
        self.__welcome_msg = Texto(globales.TEXTO[0], globales.FONT,
                                   (120, 3, 12), customEnums.TipoTexto.TITULO)
        posX = self.__viewport.horizontal_center(self.__welcome_msg.getSurface())
        posY = self.__viewport.vertical_center(self.__welcome_msg.getSurface())
        self.__welcome_msg.setPosicion(posX, posY)

    def main_menu_draw(self):
        self.__viewport.draw(self.__welcome_msg.getSurface(),
                             self.__welcome_msg.getPosicion())
