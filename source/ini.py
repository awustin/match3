import sys
import pygame
from random import random
from pygame import mouse
from pygame import event
from pygame import sprite
import customEnums
from viewport import Viewport
from texto import Texto
from tablero import Tablero
from selector import Selector
from cellContent import UnbreakableBlock
from cellContent import Chip
from controllers.inputController import InputController
import spritesData as sprites

sys.path.insert(0, 'config')
try:
    import globales
except Exception as e:
    print(e)
    raise


class App:
    def __init__(self):
        pygame.init()

    def init_screen(self):
        self.display = Viewport(*globales.DIMENSION)
        self.display.init_viewport(globales.LOGO, globales.CAPTION)
        self.display.bkg_color(globales.COLOR_FONDO)
        self.mjeInicio = Texto(globales.TEXTO[0], globales.FONT,
                               (120, 3, 12), customEnums.TipoTexto.TITULO)
        posX = self.display.horizontal_center(self.mjeInicio.getSurface())
        posY = self.display.vertical_center(self.mjeInicio.getSurface())
        self.mjeInicio.setPosicion(posX, posY)
        self.tablero = Tablero(color=(20, 40, 80))
        self.selector = Selector(self.tablero)
        sprites.init_sprite_data()

    def main_menu(self):
        action = InputController.MainMenuTick()
        if action == 0:
            return 'exit'
        if action == 'start':
            self.match()
        if action == 'test':
            self.test()
        self.display.bkg_color(globales.COLOR_FONDO)
        self.display.draw(self.mjeInicio.getSurface(),
                          self.mjeInicio.getPosicion())
        return 1

    def match(self):
        gameOver = False
        colorPpal = (120, 100, 50)
        while(not gameOver):
            for evento in event.get():
                if(evento.type == pygame.QUIT):
                    gameOver = True
                    pygame.quit()
                    quit()
                if(evento.type == pygame.KEYDOWN):
                    if(evento.key == pygame.K_a):
                        self.selector.setPos(0, 0)
                        self.tablero.reiniciaFichasCeldasTablero()
                        return
                    if(evento.key == pygame.K_r):
                        self.selector.setPos(0, 0)
                        self.tablero.reiniciaFichasCeldasTablero()
                        colorPpal = (random()*255, random()*255, random()*255)
                if(evento.type == pygame.MOUSEBUTTONDOWN):
                    if(mouse.get_pressed()[0] == 1):
                        self.tablero.clickXY(*mouse.get_pos(), self.selector,
                                             self.display.get_display(),
                                             colorPpal)
            self.display.bkg_color(colorPpal)
            hayAlineaciones = self.tablero.actualizarTableroConEstado(
                                          self.display.get_display())
            if(hayAlineaciones):
                self.tablero.alineacionEnTablero(self.display.get_display(),
                                                 colorPpal)
            self.tablero.posicionarSelector(*mouse.get_pos(), self.selector)
            self.selector.update(self.display.get_display())
            pygame.display.update()

    def test(self):
        gameOver = False
        colorPpal = (100, 100, 100)
        print("Test...")
        items = []
        item_group = sprite.Group()
        for i in range(5):
            if i == 0:
                item = UnbreakableBlock()
            else:
                item = Chip(cell_class=i)
            item.set_center_pos(i*70 + 40, 60)
            items.append(item)
        for item in items:
            item_group.add(item)
        item_group.draw(self.display.get_display())
        while(not gameOver):
            for evento in event.get():
                if(evento.type == pygame.QUIT):
                    print('Quiting...')
                    gameOver = True
                    pygame.quit()
                    quit()
                if(evento.type == pygame.KEYDOWN):
                    if(evento.key == pygame.K_a):
                        return
            self.display.bkg_color(colorPpal)
            item_group.update(self.display.get_display())
            pygame.display.update()


if __name__ == "__main__":
    theApp = App()
    theApp.init_screen()
    game_over = False
    while not game_over:
        if theApp.main_menu() == 'exit':
            game_over = True
        pygame.display.update()
    pygame.quit()
