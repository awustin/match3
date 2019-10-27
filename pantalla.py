# Pantalla
# Responsable de la Ventana y de la pantalla
import pygame


class Pantalla(object):
    def __init__(self, width, height, config='default'):
        self.__dim = (width, height)
        pygame.init()
        if(config == 'default'):
            self.inicializarDefault()
        else:
            raise Exception('Configuracion de pantalla inválida: %s' % config)

    def inicializarDefault(self):
        self.__disp = pygame.display.set_mode(self.__dim,
                                              pygame.RESIZABLE |
                                              pygame.HWSURFACE |
                                              pygame.DOUBLEBUF)

    def inicializarVentana(self, logoDir, caption):
        self.__logosurf = pygame.image.load(logoDir)
        pygame.display.set_icon(self.__logosurf)
        self.__caption = pygame.display.set_caption(caption)

    def renderTexto(self, texto, fontObject, colorRGB):
        return fontObject.render(texto, 1, colorRGB)

    def colorFondo(self, colorRGB):
        self.__disp.fill(colorRGB)

    def dibujar(self, source, dest, area=None):
        self.__disp.blit(source, dest, area)

    # Devuelve X para que la superficie quede centrada
    def posicionCentrarX(self, superficie):
        pantallaX = self.__disp.get_size()[0]
        superficieX = superficie.get_size()[0]
        return ((pantallaX - superficieX)/2)

    def posicionCentrarY(self, superficie):
        pantallaY = self.__disp.get_size()[1]
        superficieY = superficie.get_size()[1]
        return ((pantallaY - superficieY)/2)

    def getDisplay(self):
        return self.__disp
