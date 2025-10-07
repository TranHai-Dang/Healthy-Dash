import pygame, sys, random
from player import Player
from obstacle import Obstacle
from items import Item

pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Groups
player = pygame.sprite.GroupSingle(Player())
obstacles = pygame.sprite.Group()
items = pygame.sprite.Group()

# Timers
SPAWN_OBSTACLE = pygame.USEREVENT + 1
SPAWN_ITEM = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_OBSTACLE, 1500)
pygame.time.set_timer(SPAWN_ITEM, 2000)

# Stats
score = 0
energy = 100     # nhảy cao
drink = 100     # tốc độ
game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_OBSTACLE and game_active:
            obstacles.add(Obstacle())
        if event.type == SPAWN_ITEM and game_active:
            kind = random.choice(["energy", "drink"])
            items.add(Item(kind))

    if game_active:
        screen.fill((30, 30, 30))

        # Giảm dần 2 thanh
        energy -= 0.1
        drink -= 0.1
        if energy <= 0 or drink <= 0:
            game_active = False

        # Điều chỉnh tốc độ obstacles theo drink
        speed_factor = max(0.5, drink / 100)
        for obs in obstacles:
            obs.rect.x -= int(5 * speed_factor)
        for itm in items:
            itm.rect.x -= int(5 * speed_factor)

        # Update & draw
        player.update()
        player.draw(screen)
        obstacles.update()
        obstacles.draw(screen)
        items.update()
        items.draw(screen)

        # Collision check
        if pygame.sprite.spritecollide(player.sprite, obstacles, False):
            game_active = False

        collected = pygame.sprite.spritecollide(player.sprite, items, True)
        for item in collected:
            if item.kind == "energy":
                energy = min(energy + 20, 100)
            elif item.kind == "drink":
                drink = min(drink + 20, 100)
                score += 1

        # Vượt chướng ngại vật → điểm
        for obs in obstacles:
            if obs.rect.right < player.sprite.rect.left and not hasattr(obs, 'scored'):
                score += 1
                obs.scored = True

        # Hiển thị điểm
        score_text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # --- THANH NĂNG LƯỢNG ---
        # Nền
        pygame.draw.rect(screen, (60, 60, 60), (10, 40, 200, 15))
        pygame.draw.rect(screen, (60, 60, 60), (10, 65, 200, 15))
        # Energy (vàng)
        pygame.draw.rect(screen, (255, 200, 0), (10, 40, int(energy * 2), 15))
        # Drink (xanh)
        pygame.draw.rect(screen, (0, 200, 255), (10, 65, int(drink * 2), 15))

    else:
        screen.fill((0, 0, 0))
        msg = font.render("Game Over - Press SPACE to restart", True, (255, 255, 255))
        screen.blit(msg, (180, 180))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            score = 0
            energy = 100
            drink = 100
            obstacles.empty()
            items.empty()
            player.sprite.rect.midbottom = (100, 350)
            game_active = True

    pygame.display.flip()
    clock.tick(60)








