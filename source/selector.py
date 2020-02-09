# Selector
import pygame


N_CELDAS = 8


class Selector(pygame.sprite.Sprite):
    def __init__(self, board):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('..\\assets\\images\\selector.png')
        self.rect = self.image.get_rect()
        self._coord = (0, 0)
        self._board = board
        self._celdas = board.getCeldas()
        self._posicionar()

#   \\
#   Get - Set
#   \\

    def getPos(self):
        return self._coord

    def setPos(self, x, y):
        self._coord = (x, y)
        self._posicionar()

#   \\
#   Metodos
#   \\

    def _setCeldas(self):
        '''Pide las celdas'''
        self._celdas = self._board.getCeldas()

    def _posicionar(self):
        '''Posiciona el selector en la celda
        correspondiente a (x, y)'''
        if(self._celdas != []):
            x = self._coord[0]
            y = self._coord[1]
            centro = self._celdas[x][y].get_center_pos()
            self.rect.center = centro

    def izquierda(self):
        '''Corre una casilla a la izquierda'''
        x = self._coord[0]
        y = self._coord[1]
        if(x == 0):
            x = N_CELDAS - 1
        else:
            x -= 1
        self._coord = (x, y)

    def derecha(self):
        '''Corre una casilla a la derecha'''
        x = self._coord[0]
        y = self._coord[1]
        if(x == 0):
            x = N_CELDAS - 1
        else:
            x -= 1
        self._coord = (x, y)

    def arriba(self):
        '''Corre una casilla arriba'''
        x = self._coord[0]
        y = self._coord[1]
        if(y == 0):
            y = N_CELDAS - 1
        else:
            y -= 1
        self._coord = (x, y)

    def abajo(self):
        '''Corre una casilla abajo'''
        '''Corre una casilla arriba'''
        x = self._coord[0]
        y = self._coord[1]
        if(y == 0):
            y = N_CELDAS - 1
        else:
            y -= 1
        self._coord = (x, y)

    def update(self, ventana):
        self._setCeldas()
        self._posicionar()
        ventana.blit(self.image, self.rect)
