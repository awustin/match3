import sys
from pygame import draw
from pygame import time
import pygame
from customEnums import TipoTexto
from view.texto import Texto
from view.visualEffects import VisualEffects

sys.path.insert(0, 'config')
try:
    import globales
except Exception as e:
    print(e)
    raise


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
        if BoardView.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            BoardView.__instance = self
            self.__display = display
            self.__fx = VisualEffects()
            self.__fruity = 0
            self.__bitter = 0
            self.__rotten = 0
            self.__init_score_text()

# CELL FUNCTIONS -----------------------------------------
    def update_background(self):
        global BKG_COLOR
        self.__display.bkg_color(BKG_COLOR)

    def draw_cells(self, cell_array):
        for row in range(len(cell_array)):
            for col in range(len(cell_array[row])):
                cell = cell_array[row][col]
                draw.rect(self.__display.get_display(), cell.getColorCelda(),
                          cell.getRect())
        self.update_effects()

    def draw_initial_chips(self, chip_array):
        for row in reversed(range(len(chip_array))):
            for col in range(len(chip_array)):
                time.wait(7)
                chip_array[row][col].update(self.__display.get_display())
                pygame.display.update()
        self.update_effects()

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
            self.draw_score()
            self.update_effects()
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
            self.draw_score()
            self.update_effects()
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
            self.draw_score()
            self.update_effects()
            pygame.display.update()

    def update_chips(self, sprite_group):
        sprite_group.update(self.__display.get_display())

    def update_selector_position(self, selector):
        selector.update(self.__display.get_display())

# SCORE FUNCTIONS -----------------------------------------------
    def set_score(self, fruity, bitter, rotten):
        self.__fruity = fruity
        self.__bitter = bitter
        self.__rotten = rotten

    def __refresh_score(self):
        self.__fruity_info = Texto(f'Fruity {self.__fruity}', globales.FONT,
                                   (120, 3, 12), TipoTexto.INFO)
        self.__bitter_info = Texto(f'Bitter {self.__bitter}', globales.FONT,
                                   (120, 3, 12), TipoTexto.INFO)
        self.__rotten_info = Texto(f'Rotten {self.__rotten}', globales.FONT,
                                   (120, 3, 12), TipoTexto.INFO)
        self.__fruity_info.setPosicion((5, 140))
        self.__bitter_info.setPosicion((5, 180))
        self.__rotten_info.setPosicion((5, 220))

    def __init_score_text(self):
        self.__score_info = Texto('SCORE', globales.FONT,
                                  (120, 3, 12), TipoTexto.INFO)
        self.__score_info.setPosicion((2, 100))
        self.__refresh_score()

    def draw_score(self):
        self.__refresh_score()
        self.__display.draw(self.__fruity_info.getSurface(),
                            self.__fruity_info.getPosicion())
        self.__display.draw(self.__bitter_info.getSurface(),
                            self.__bitter_info.getPosicion())
        self.__display.draw(self.__rotten_info.getSurface(),
                            self.__rotten_info.getPosicion())
        self.__display.draw(self.__score_info.getSurface(),
                            self.__score_info.getPosicion())

# FX ------------------------------------------------------------
    def run_alignment_effects(self, origins):
        'Pass in all the origins of the animation'
        self.__fx.run_sparkles_alignment(origins)
        self.__fx.run_power_ratio(origins)

    def update_effects(self):
        self.__fx.update_effects_sparkles_alignment(self.__display.get_display())