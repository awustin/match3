# JUEGO
import sys
import pygame
from random import random
from pygame import time
from pygame import mouse
from pygame import event
from pygame import sprite
import globales
import customEnums
from pantalla import Pantalla
from texto import Texto
from tablero import Tablero
from ficha import Ficha


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
        print("Presionó ENTER")
        while(not gameOver):
            for evento in event.get():
                if(evento.type == pygame.QUIT):
                    gameOver = True
                    pygame.quit()
                    quit()
                if(evento.type == pygame.KEYDOWN):
                    if(evento.key == pygame.K_a):
                        self.tablero.reiniciaFichasCeldasTablero()
                        return
                    if(evento.key == pygame.K_r):
                        self.tablero.reiniciaFichasCeldasTablero()
                        colorPpal = (random()*255, random()*255, random()*255)
                        print("Recargando tablero...")
                if(evento.type == pygame.MOUSEBUTTONDOWN):
                    if(mouse.get_pressed()[0] == 1):
                        self.tablero.clickXY(*mouse.get_pos())
            self.pantalla.colorFondo(colorPpal)
            fichasCaen = self.tablero.actualizarTableroConEstado(self.pantalla.getDisplay())
            if(fichasCaen):
                self.tablero.alineacionEnTablero(self.pantalla.getDisplay())
                # TODO: REFACTOR
                #self.tablero.pasarFichasEntreCeldas(self.pantalla.getDisplay(), colorPpal)
                #self.tablero.rellenarCeldasPorColumna(self.pantalla.getDisplay())
            pygame.display.update()

    def test(self):
        gameOver = False
        colorPpal = (100, 100, 100)
        print("Test...")
        fichas = []
        grupo_fichas = sprite.Group()
        for i in range(1, 5):
            ficha = Ficha(idTipo=i, x=40*(i-1))
            fichas.append(ficha)
        for ficha in fichas:
            grupo_fichas.add(ficha)
        fichas[0].setCae(True, 300, 0.5)
        fichas[1].setCae(True, 400, 1)
        fichas[2].setCae(True, 350, 0.9)
        fichas[3].setCae(True, 375, 1.3)
        grupo_fichas.draw(self.pantalla.getDisplay())
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
            grupo_fichas.update(self.pantalla.getDisplay())
            pygame.display.update()


if __name__ == "__main__":
    theApp = App()
    theApp.render_inicio()
    theApp.ejecutar()
