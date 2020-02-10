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

    def draw_swapping_chips(self, cell_array, swapping, sprite_group):
        '''Actualiza el tablero mientras se intercambian fichas'''
        chips_are_swapping = True
        display = self.__display.get_display()
        while(chips_are_swapping):
            display.fill(BKG_COLOR)
            self.draw_cells(cell_array)
            for ficha in swapping:
                if(ficha is not None):
                    chips_are_swapping = False
                    if(ficha.is_swapping()):
                        chips_are_swapping = True
                        break
            sprite_group.update(display)
            pygame.display.update()

    def draw_falling_chips(self, cell_array, sprite_group):
        '''Actualiza el tablero para la transición de
        la caida de fichas'''
        chips_are_falling = True
        display = self.__display.get_display()
        while chips_are_falling:
            display.fill(BKG_COLOR)
            self.draw_cells(cell_array)
            for ficha in sprite_group:
                chips_are_falling = False
                if(ficha.is_falling()):
                    chips_are_falling = True
                    break
            sprite_group.update(display)
            pygame.display.update()
    
    def draw_filling_board(self, new_row, cell_array, sprite_group):
        '''Actualiza la fila para la transición de
        la caida de fichas cuando hay nuevas fichas que rellenan agujeros'''
        chips_are_falling = True
        display = self.__display.get_display()
        while chips_are_falling:
            display.fill(BKG_COLOR)
            self.draw_cells(cell_array)
            for chip in new_row:
                if(chip is not None):
                    chips_are_falling = False
                    if(chip.is_falling()):
                        chips_are_falling = True
                        break
            sprite_group.update(display)
            pygame.display.update()

    def update_chips(self, sprite_group):
        sprite_group.update(self.__display.get_display())

    def update_selector_position(self, selector):
        selector.update(self.__display.get_display())