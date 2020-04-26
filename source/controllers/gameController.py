import pygame
from random import random
from view.displayView import DisplayView
from view.boardView import BoardView
from model.board import Board
from model.score import Score
from selector import Selector
import controllers.spritesData as sprites
import controllers.scoreData as scores


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
        self.__score = Score()

    def __init_screen(self):
        self.__display_view = DisplayView()
        self.__display_view.init_welcome_screen()

    def init_game(self):
        self.__init_screen()
        self.__init_board()
        sprites.init_sprite_data()
        scores.init_score_data()

# FUNCTIONS ---------------------------------------------------------
    def main_menu_tick(self):
        self.__display_view.main_menu_draw()

    def selector_tick(self):
        coord = pygame.mouse.get_pos()
        position = self.__board.locate_selector(*coord)
        if position is not None:
            self.__selector.setPos(*position)
            self.__board_view.update_selector_position(self.__selector)

    def action_reset(self):
        global BKG_COLOR
        self.__selector.setPos(0, 0)
        self.__board.restart_board()
        BKG_COLOR = (random()*255, random()*255, random()*255)

    def action_click(self, x, y):
        self.__board.click_action(x, y)

    def refresh_scores(self):
        self.__board_view.set_score(self.__score.get_fruity(),
                                    self.__score.get_bitter(),
                                    self.__score.get_rotten())
        self.__board_view.draw_score()

    def chip_elimination(self, row, col):
        center = self.__board.get_cells()[row][col].get_center_pos()
        self.__board.kill_aligned_chip(row, col)
        return center

    def score_alignments(self):
        horizontal = self.__board.get_aligned_list()[0]
        vertical = self.__board.get_aligned_list()[1]
        incomplete_columns = set()
        for alignment in horizontal:
            self.__score.compute_score(self.__board.get_chips(alignment))
            self.refresh_scores()
            origins = []
            for item in alignment:
                center = self.chip_elimination(item[0], item[1])
                origins.append(center)
                incomplete_columns.add(item[1])
            self.__board_view.run_alignment_effects(origins)
        for alignment in vertical:
            self.__score.compute_score(self.__board.get_chips(alignment))
            self.refresh_scores()
            origins = []
            for item in alignment:
                center = self.chip_elimination(item[0], item[1])
                origins.append(center)
                incomplete_columns.add(item[1])
            self.__board_view.run_alignment_effects(origins)
        self.__board.clear_aligned_list()
        return incomplete_columns

    def main_board_tick(self):
        self.__board_view.update_background()
        self.__board_view.draw_score()
        self.__board_view.update_effects()
        aligned_list = self.__board.main_board_update()
        if (aligned_list != []):
            incomplete_columns = self.score_alignments()
            self.__board.pass_chips_between_cells(incomplete_columns)
            self.__board.new_chips_per_row()
            self.__board.clear_aligned_list()
