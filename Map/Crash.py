import pygame


class Crash(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        #Desenha o acidente no mapa
        self.image = pygame.image.load('Map/Resources/collision.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
