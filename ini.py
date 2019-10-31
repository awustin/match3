# JUEGO
import sys
import pygame
from random import random
from pygame import time
from pygame import mouse
from pygame import event
import globales
import customEnums
from pantalla import Pantalla
from texto import Texto
from tablero import Tablero


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
        self.tablero = Tablero()
        # self.tablero.centrarTablero(self.pantalla.getDisplay())
        posX = self.pantalla.posicionCentrarX(self.tablero.getSurface())
        posY = self.pantalla.posicionCentrarY(self.tablero.getSurface())
        self.tablero.setPosicionOffset(posX, posY)
        self.tablero.inicializarCruadricula()

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
            self.pantalla.colorFondo(globales.COLOR_FONDO)
            self.pantalla.dibujar(mjeInicio.getSurface(),
                                  mjeInicio.getPosicion())
            pygame.display.update()
            clock.tick_busy_loop(50)

    def partida(self):
        gameOver = False
        mostrarInfo = False
        colorPpal = (100, 200, 100)
        print("Presionó ENTER")
        while(not gameOver):
            for evento in event.get():
                if(evento.type == pygame.QUIT):
                    gameOver = True
                    sys.exit()
                if(evento.type == pygame.KEYDOWN):
                    if(evento.key == pygame.K_a):
                        return
                    if(evento.key == pygame.K_r):
                        self.tablero.setCompleto(False)
                        self.tablero.setMatches(False)
                        colorPpal = (random()*255, random()*255, random()*255)
                        print("Recargando tablero...")
                if(evento.type == pygame.MOUSEBUTTONDOWN):
                    if(mouse.get_pressed()[0] == 1):
                        infoXY = Texto(mouse.get_pos(), globales.FONT_INFO,
                                       (0, 0, 0), customEnums.TipoTexto.INFO)
                        self.tablero.clickXY(*mouse.get_pos())
                        mostrarInfo = True
            self.pantalla.colorFondo(colorPpal)
            self.pantalla.dibujar(self.tablero.getSurface(),
                                  self.tablero.getPosicion())
            self.tablero.dibujarFormas()
            self.tablero.verificarMatches()
            if(mostrarInfo):
                self.pantalla.dibujar(infoXY.getSurface(), (0, 0))
            pygame.display.update()


if __name__ == "__main__":
    theApp = App()
    theApp.render_inicio()
    theApp.ejecutar()
