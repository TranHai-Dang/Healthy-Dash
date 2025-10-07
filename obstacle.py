import pygame
import random

GROUND_LEVEL = 350
OBSTACLE_COLOR = (255, 0, 0)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(OBSTACLE_COLOR)
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), GROUND_LEVEL))

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()