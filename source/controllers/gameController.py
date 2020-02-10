import pygame
from random import random
from view.displayView import DisplayView
from view.boardView import BoardView
from board import Board
from selector import Selector


class GameController():
    def __init__(self):
        self.__board_view = None
        self.__board = None
        self.__selector = None
        self.__display_view = None
        self.__display = None

    def events_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_r):
                    self.action_reset()
            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(pygame.mouse.get_pressed()[0] == 1):
                    self.action_click(*pygame.mouse.get_pos())
        return 1

# INITIALIZATION ----------------------------------------------------
    def __init_board(self):
        self.__board_view = BoardView(self.__display_view.get_display())
        self.__board = Board(self.__board_view)
        self.__selector = Selector(self.__board)

    def __init_screen(self):
        self.__display_view = DisplayView()
        self.__display_view.init_welcome_screen()

    def init_game(self):
        self.__init_screen()
        self.__init_board()

# FUNCTIONS ---------------------------------------------------------
    def main_menu_tick(self):
        self.__display_view.main_menu_draw()

    def selector_tick(self):
        coord = pygame.mouse.get_pos()
        position = self.__board.posicionarSelector(*coord)
        if position is not None:
            self.__selector.setPos(*position)
            self.__board_view.update_selector_position(self.__selector)

    def action_reset(self):
        global BKG_COLOR
        self.__selector.setPos(0, 0)
        self.__board.reiniciaFichasCeldasTablero()
        BKG_COLOR = (random()*255, random()*255, random()*255)

    def action_click(self, x, y):
        self.__board.clickXY(x, y)

    def action_aligned(self):
        self.__board.alineacionEnTablero()

    def main_board_tick(self):
        self.__board_view.update_background()
        chips_algined = self.__board.main_board_update()
        if chips_algined:
            self.action_aligned()
