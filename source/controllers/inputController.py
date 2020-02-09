import pygame


class InputController():
    def main_menu_tick():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_RETURN):
                    return 'start'
                if(event.key == pygame.K_t):
                    return 'test'
        return 1
