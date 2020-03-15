import sys
import pygame
from pygame import event
from pygame import sprite
from cellContent import UnbreakableBlock
from cellContent import Chip
from controllers.inputController import InputController
from controllers.gameController import GameController
import spritesData as sprites
import scoreData as scores

sys.path.insert(0, 'config')
try:
    import globales
except Exception as e:
    print(e)
    raise

GAME_OVER = False


class App:
    def __init__(self):
        pygame.init()

    def init_game(self):
        self.__game_controller = GameController()
        self.__game_controller.init_game()
        sprites.init_sprite_data()
        scores.init_score_data()

    def main_menu(self):
        global GAME_OVER
        self.__game_controller.main_menu_tick()
        action = InputController.main_menu_tick()
        if action == 0:
            return 'exit'
        if action == 'start':
            action = self.match()
            if action == 'exit':
                return action
        if action == 'test':
            self.test()
        return 1

    def match(self):
        global GAME_OVER
        global BKG_COLOR
        while(not GAME_OVER):
            action = self.__game_controller.events_tick()
            if action == 'exit':
                return action
            self.__game_controller.main_board_tick()
            self.__game_controller.selector_tick()
            pygame.display.update()

    def test(self):
        gameOver = False
        BKG_COLOR = (100, 100, 100)
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
        item_group.draw(self.display.get_display())
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
            self.display.bkg_color(BKG_COLOR)
            item_group.update(self.display.get_display())
            pygame.display.update()


if __name__ == "__main__":
    theApp = App()
    theApp.init_game()
    while not GAME_OVER:
        if theApp.main_menu() == 'exit':
            GAME_OVER = True
        pygame.display.update()
    pygame.quit()
