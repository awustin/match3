import pygame


class InputController():
    def MainMenuTick():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 0
            if evento.type == pygame.KEYDOWN:
                if(evento.key == pygame.K_RETURN):
                    return 'start'
                if(evento.key == pygame.K_t):
                    return 'test'
        return 1
