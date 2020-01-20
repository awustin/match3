import sys
import pygame
from random import random
from pygame import time
from pygame import mouse
from pygame import event
from pygame import sprite
import customEnums
from pantalla import Pantalla
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
        self.display = Pantalla(*globales.DIMENSION)
        self.display.inicializarVentana(globales.LOGO, globales.CAPTION)
        self.display.colorFondo(globales.COLOR_FONDO)
        self.mjeInicio = Texto(globales.TEXTO[0], globales.FONT,
                               (120, 3, 12), customEnums.TipoTexto.TITULO)
        posX = self.display.posicionCentrarX(self.mjeInicio.getSurface())
        posY = self.display.posicionCentrarY(self.mjeInicio.getSurface())
        self.mjeInicio.setPosicion(posX, posY)
        self.tablero = Tablero(color=(20, 40, 80))
        self.selector = Selector(self.tablero)
        sprites.init_sprite_data()

    def main_menu(self):
        action = InputController.MainMenuTick()
        if action == 0:
            return 0
        if action == 'start':
            self.partida()
        if action == 'test':
            self.test()
        self.display.colorFondo(globales.COLOR_FONDO)
        self.display.dibujar(self.mjeInicio.getSurface(),
                             self.mjeInicio.getPosicion())
        return 1

    def run_game(self):
        clock = time.Clock()
        game_over = False
        while not game_over:
            if self.main_menu() == 0:
                game_over = True
            pygame.display.update()
            clock.tick_busy_loop(50)
        pygame.quit()

    def partida(self):
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
                                             self.display.getDisplay(),
                                             colorPpal)
            self.display.colorFondo(colorPpal)
            hayAlineaciones = self.tablero.actualizarTableroConEstado(
                                          self.display.getDisplay())
            if(hayAlineaciones):
                self.tablero.alineacionEnTablero(self.display.getDisplay(),
                                                 colorPpal)
            self.tablero.posicionarSelector(*mouse.get_pos(), self.selector)
            self.selector.update(self.display.getDisplay())
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
        item_group.draw(self.display.getDisplay())
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
            self.display.colorFondo(colorPpal)
            item_group.update(self.display.getDisplay())
            pygame.display.update()


if __name__ == "__main__":
    theApp = App()
    theApp.init_screen()
    theApp.run_game()
