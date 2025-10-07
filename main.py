import pygame, sys, random
from player import Player
from obstacle import Obstacle
from items import Item  

pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

player = pygame.sprite.GroupSingle(Player())
obstacles = pygame.sprite.Group()
items = pygame.sprite.Group()  

SPAWN_OBSTACLE = pygame.USEREVENT + 1
SPAWN_ITEM = pygame.USEREVENT + 2  
pygame.time.set_timer(SPAWN_OBSTACLE, 1500)
pygame.time.set_timer(SPAWN_ITEM, 2000)  

score = 0
game_active = True
energy = 100
drink = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_OBSTACLE and game_active:
            obstacles.add(Obstacle())
        if event.type == SPAWN_ITEM and game_active:  # ✅ thêm dòng này
            items.add(Item(random.choice(["energy", "drink"])))


    if game_active:
        screen.fill((30, 30, 30))

        # cập nhật nhóm
        player.update()
        obstacles.update()
        items.update()

        # vẽ tất cả
        player.draw(screen)
        obstacles.draw(screen)
        items.draw(screen)

        # kiểm tra va chạm vật cản
        if pygame.sprite.spritecollide(player.sprite, obstacles, False):
            game_active = False

        # kiểm tra ăn item ✅
        collected = pygame.sprite.spritecollide(player.sprite, items, True)
        for item in collected:
            if item.type == "energy":
                energy = min(100, energy + 20)
            elif item.item.type == "drink":
                drink = min(100, drink + 20)

        # giảm dần theo thời gian
        energy -= 0.05
        drink -= 0.03
        if energy <= 0 or drink <= 0:
            game_active = False

        # tăng điểm khi qua chướng ngại vật
        for obs in obstacles:
            if obs.rect.right < player.sprite.rect.left and not hasattr(obs, 'scored'):
                score += 1
                obs.scored = True

        # hiển thị điểm và thanh
        pygame.draw.rect(screen, (0, 200, 255), (10, 40, energy * 2, 10))
        pygame.draw.rect(screen, (255, 200, 0), (10, 60, drink * 2, 10))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
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


