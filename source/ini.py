# JUEGO
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
from ficha import UnbreakableBlock
from ficha import Chip
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

    def render_inicio(self):
        self.pantalla = Pantalla(*globales.DIMENSION)
        self.pantalla.inicializarVentana(globales.LOGO, globales.CAPTION)
        self.pantalla.colorFondo(globales.COLOR_FONDO)
        self.mjeInicio = Texto(globales.TEXTO[0], globales.FONT,
                               (120, 3, 12), customEnums.TipoTexto.TITULO)
        posX = self.pantalla.posicionCentrarX(self.mjeInicio.getSurface())
        posY = self.pantalla.posicionCentrarY(self.mjeInicio.getSurface())
        self.mjeInicio.setPosicion(posX, posY)
        self.tablero = Tablero(color=(20, 40, 80))
        self.selector = Selector(self.tablero)
        sprites.init_sprite_data()

    def ejecutar(self):
        clock = time.Clock()
        gameOver = False
        mjeInicio = self.mjeInicio
        self.pantalla.dibujar(mjeInicio.getSurface(), mjeInicio.getPosicion())
        while not gameOver:
            for evento in event.get():
                if evento.type == pygame.QUIT:
                    gameOver = True
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if(evento.key == pygame.K_RETURN):
                        self.partida()
                    if(evento.key == pygame.K_t):
                        self.test()
            self.pantalla.colorFondo(globales.COLOR_FONDO)
            self.pantalla.dibujar(mjeInicio.getSurface(),
                                  mjeInicio.getPosicion())
            pygame.display.update()
            clock.tick_busy_loop(50)

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
                                             self.pantalla.getDisplay(),
                                             colorPpal)
            self.pantalla.colorFondo(colorPpal)
            hayAlineaciones = self.tablero.actualizarTableroConEstado(
                                          self.pantalla.getDisplay())
            if(hayAlineaciones):
                self.tablero.alineacionEnTablero(self.pantalla.getDisplay(),
                                                 colorPpal)
            self.tablero.posicionarSelector(*mouse.get_pos(), self.selector)
            self.selector.update(self.pantalla.getDisplay())
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
            item.setPosicionCentro(i*70 + 40, 60)
            items.append(item)
        for item in items:
            item_group.add(item)
        item_group.draw(self.pantalla.getDisplay())
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
            self.pantalla.colorFondo(colorPpal)
            item_group.update(self.pantalla.getDisplay())
            pygame.display.update()


if __name__ == "__main__":
    theApp = App()
    theApp.render_inicio()
    theApp.ejecutar()