from pygame import draw
from pygame import time
import pygame


BASE_CELL_COLOR = (20, 40, 80)
BKG_COLOR = (120, 100, 50)


class BoardView():
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if BoardView.__instance is None:
            BoardView()
        return BoardView.__instance

    def __init__(self, display):
        """ Virtually private constructor. """
        self.__display = display
        if BoardView.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            BoardView.__instance = self

    def update_selector(self, x, y):
        self.__select.update(self.__display)

# DRAW FUNCTIONS -----------------------------------------
    def update_background(self):
        global BKG_COLOR
        self.__display.bkg_color(BKG_COLOR)

    def draw_cells(self, cell_array):
        for row in range(len(cell_array)):
            for col in range(len(cell_array[row])):
                cell = cell_array[row][col]
                draw.rect(self.__display.get_display(), cell.getColorCelda(),
                          cell.getRect())

    def draw_initial_chips(self, chip_array):
        for row in reversed(range(len(chip_array))):
            for col in range(len(chip_array)):
                time.wait(7)
                chip_array[row][col].update(self.__display.get_display())
                pygame.display.update()

    def update_chips(self, sprite_group):
        sprite_group.update(self.__display.get_display())

# COLOR FUNCTIONS ----------------------------------------------------------------
    def gradient(color):
        return color