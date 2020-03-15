import sys
from customEnums import TipoTexto
from view.texto import Texto

sys.path.insert(0, 'config')
try:
    import globales
except Exception as e:
    print(e)
    raise


class ScoreView():
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if ScoreView.__instance is None:
            ScoreView()
        return ScoreView.__instance

    def __init__(self, display):
        """ Virtually private constructor. """
        if ScoreView.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ScoreView.__instance = self
            self.__display = display
            self.__init_text()

    def __init_text(self):
        self.__score_info = Texto('SCORE', globales.FONT,
                                  (120, 3, 12), TipoTexto.INFO)
        self.__score_info.setPosicion((0, 100))

    def score_draw(self):
        self.__display.draw(self.__score_info.getSurface(),
                            self.__score_info.getPosicion())
