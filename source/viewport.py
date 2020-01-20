import pygame


class Viewport(object):
    def __init__(self, width, height, config='default'):
        self.__dim = (width, height)
        pygame.init()
        if(config == 'default'):
            self.init_default_settings()
        else:
            raise Exception('Configuracion de pantalla inválida: %s' % config)

    def init_default_settings(self):
        self.__disp = pygame.display.set_mode(self.__dim,
                                              pygame.RESIZABLE |
                                              pygame.HWSURFACE |
                                              pygame.DOUBLEBUF)

    def init_viewport(self, logoDir, caption):
        self.__logosurf = pygame.image.load(logoDir)
        pygame.display.set_icon(self.__logosurf)
        self.__caption = pygame.display.set_caption(caption)

    def bkg_color(self, colorRGB):
        self.__disp.fill(colorRGB)

    def draw(self, source, dest, area=None):
        self.__disp.blit(source, dest, area)

    def horizontal_center(self, superficie):
        pantallaX = self.__disp.get_size()[0]
        superficieX = superficie.get_size()[0]
        return ((pantallaX - superficieX)/2)

    def vertical_center(self, superficie):
        pantallaY = self.__disp.get_size()[1]
        superficieY = superficie.get_size()[1]
        return ((pantallaY - superficieY)/2)

    def get_display(self):
        return self.__disp
