import pygame
import random

GROUND_LEVEL = 350
DRINK_COLOR = (0, 200, 255)
ENERGY_COLOR = (255, 200, 0)

class Item(pygame.sprite.Sprite):
    def __init__(self, kind):  
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((30, 30))
        if self.kind == "energy":
            self.image.fill(ENERGY_COLOR)
        else:
            self.image.fill(DRINK_COLOR)
        self.rect = self.image.get_rect(
            midbottom=(random.randint(900, 1100), random.randint(200, GROUND_LEVEL - 20))
        )

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

