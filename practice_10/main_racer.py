import pygame, random
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
FPS = 30  

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
player_x = WIDTH//2 - PLAYER_WIDTH//2
player_y = HEIGHT - PLAYER_HEIGHT - 10
player_speed = 5 

ENEMY_WIDTH, ENEMY_HEIGHT = 40, 60
enemy_speed = 3
enemy_list = [[random.randint(0, WIDTH-ENEMY_WIDTH), -ENEMY_HEIGHT, enemy_speed] for _ in range(3)]


COIN_RADIUS = 10
COIN_SPAWN_TIME = 2000  
last_coin_spawn = pygame.time.get_ticks()
coins = []

score = 0
COINS_TO_SPEEDUP = 5  
speedup_factor = 1.5

coin_types = [1, 3]
coin_weights = [80, 20] 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    player_x = max(0, min(WIDTH-PLAYER_WIDTH, player_x))

    now = pygame.time.get_ticks()
    if now - last_coin_spawn > COIN_SPAWN_TIME:
        last_coin_spawn = now
        coin_value = random.choices(coin_types, weights=coin_weights, k=1)[0]
        coin_x = random.randint(COIN_RADIUS, WIDTH-COIN_RADIUS)
        coins.append([coin_x, -COIN_RADIUS, coin_value])

    for e in enemy_list:
        e[1] += e[2] 
        if e[1] > HEIGHT:
            e[0] = random.randint(0, WIDTH-ENEMY_WIDTH)
            e[1] = -ENEMY_HEIGHT

    for c in coins:
        c[1] += 2 

    coins = [c for c in coins if c[1] < HEIGHT + COIN_RADIUS]


    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    for e in enemy_list:
        enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
        if player_rect.colliderect(enemy_rect): 
            print("Game Over! Final Score:", score)
            running = False

    for c in coins[:]:
        coin_rect = pygame.Rect(c[0]-COIN_RADIUS, c[1]-COIN_RADIUS, COIN_RADIUS*2, COIN_RADIUS*2)
        if player_rect.colliderect(coin_rect):
            score += c[2]
            coins.remove(c)

    if score >= COINS_TO_SPEEDUP:
        FPS = int(FPS * speedup_factor)
        for e in enemy_list:
            e[2] = enemy_speed
        COINS_TO_SPEEDUP += COINS_TO_SPEEDUP  


    screen.fill((0, 0, 0)) 
    pygame.draw.rect(screen, (209, 0, 195), (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    for e in enemy_list:
        pygame.draw.rect(screen, (0, 6, 173), (e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT))

    font = pygame.font.SysFont(None, 24)
    for c in coins:
        pygame.draw.circle(screen, (255, 255, 0), (c[0], c[1]), COIN_RADIUS)
        text = font.render(str(c[2]), True, (0,0,0))
        tx, ty = text.get_size()
        screen.blit(text, (c[0]-tx//2, c[1]-ty//2))
    score_surf = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_surf, (10, 10))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
