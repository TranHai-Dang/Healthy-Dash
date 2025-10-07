import pygame

GROUND_LEVEL = 350
PLAYER_COLOR = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 70))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(midbottom=(100, GROUND_LEVEL))
        self.gravity = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND_LEVEL:
            self.gravity = -15  # lực nhảy

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL

    def update(self):
        self.handle_input()
        self.apply_gravity()
