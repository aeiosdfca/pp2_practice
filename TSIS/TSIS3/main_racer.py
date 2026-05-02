import pygame, random, os
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
FPS = 30  
slow_time = 0
SLOW_DURATION = 3000
speed_multiplier = 1.0

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

OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 20, 40
obstacles = []
OBSTACLE_SPAWN_TIME = 3000
last_obstacle_spawn = pygame.time.get_ticks()

CHECKPOINT_WIDTH = WIDTH
CHECKPOINT_HEIGHT = 10
checkpoints = []
CHECKPOINT_SPAWN_TIME = 10000
last_checkpoint_spawn = pygame.time.get_ticks()
checkpoint_passed = 0

ROAD_LINES = []
for i in range(0, HEIGHT, 50):
    ROAD_LINES.append([WIDTH//2 - 5, i, 10, 30])

LANE_HAZARDS = []
for i in range(3):
    lane_x = (WIDTH // 4) * (i + 1) - 10
    LANE_HAZARDS.append([lane_x, random.randint(0, HEIGHT), 20, 20])

MOVING_FEATURES = []
MOVING_FEATURE_SPAWN_TIME = 5000
last_moving_feature_spawn = pygame.time.get_ticks()

score = 0
level = 1
COINS_TO_LEVELUP = 10
speedup_factor = 10

coin_types = [1, 3]
coin_weights = [80, 20] 

leaderboard = []
if os.path.exists('leaderboard.txt'):
    with open('leaderboard.txt', 'r') as f:
        leaderboard = [int(line.strip()) for line in f.readlines()]
leaderboard.sort(reverse=True)

player_img = None
enemy_img = None
obstacle_img = None
coin_img = None

script_dir = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(script_dir, 'player_car.png')):
    player_img = pygame.image.load(os.path.join(script_dir, 'player_car.png'))
    print(f"Loaded player_car.png from {script_dir}")
else:
    print(f"player_car.png not found in {script_dir}")

if os.path.exists(os.path.join(script_dir, 'enemy_car.png')):
    enemy_img = pygame.image.load(os.path.join(script_dir, 'enemy_car.png'))
    print(f"Loaded enemy_car.png from {script_dir}")
else:
    print(f"enemy_car.png not found in {script_dir}")


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

    if now - slow_time > SLOW_DURATION:
        speed_multiplier = 1.0 + (level - 1) * 0.1
    
    if now - last_coin_spawn > COIN_SPAWN_TIME:
        last_coin_spawn = now
        coin_value = random.choices(coin_types, weights=coin_weights, k=1)[0]
        coin_x = random.randint(COIN_RADIUS, WIDTH-COIN_RADIUS)
        coins.append([coin_x, -COIN_RADIUS, coin_value])

    if now - last_obstacle_spawn > OBSTACLE_SPAWN_TIME:
        last_obstacle_spawn = now
        obs_x = random.randint(0, WIDTH-OBSTACLE_WIDTH)
        obstacles.append([obs_x, -OBSTACLE_HEIGHT])

    if now - last_checkpoint_spawn > CHECKPOINT_SPAWN_TIME:
        last_checkpoint_spawn = now
        checkpoints.append([0, -CHECKPOINT_HEIGHT])

    if now - last_moving_feature_spawn > MOVING_FEATURE_SPAWN_TIME:
        last_moving_feature_spawn = now
        mf_x = random.randint(0, WIDTH-20)
        mf_speed = random.choice([-2, 2])
        MOVING_FEATURES.append([mf_x, -20, 20, 20, mf_speed])

    for e in enemy_list:
        e[1] += e[2] * speed_multiplier
        if e[1] > HEIGHT:
            e[0] = random.randint(0, WIDTH-ENEMY_WIDTH)
            e[1] = -ENEMY_HEIGHT

    for c in coins:
        c[1] += 2 * speed_multiplier

    coins = [c for c in coins if c[1] < HEIGHT + COIN_RADIUS]

    for o in obstacles:
        o[1] += 4 * speed_multiplier

    obstacles = [o for o in obstacles if o[1] < HEIGHT + OBSTACLE_HEIGHT]

    for cp in checkpoints:
        cp[1] += 2 * speed_multiplier

    checkpoints = [cp for cp in checkpoints if cp[1] < HEIGHT + CHECKPOINT_HEIGHT]

    for mf in MOVING_FEATURES:
        mf[0] += mf[4]
        mf[1] += 3 * speed_multiplier  
        if mf[0] < 0 or mf[0] > WIDTH - 20:
            mf[4] = -mf[4]

    MOVING_FEATURES = [mf for mf in MOVING_FEATURES if mf[1] < HEIGHT + 20]

    for hazard in LANE_HAZARDS:
        hazard[1] += 2 * speed_multiplier
        if hazard[1] > HEIGHT:
            hazard[1] = -20  

    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    for e in enemy_list:
        enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
        if player_rect.colliderect(enemy_rect): 
            print("Game Over! Final Score:", score)
            leaderboard.append(score)
            leaderboard.sort(reverse=True)
            with open('leaderboard.txt', 'w') as f:
                for s in leaderboard[:5]:
                    f.write(str(s) + '\n')
            running = False

    for o in obstacles:
        obs_rect = pygame.Rect(o[0], o[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        if player_rect.colliderect(obs_rect):
            print("Hit Obstacle! Game Over! Final Score:", score)
            leaderboard.append(score)
            leaderboard.sort(reverse=True)
            with open('leaderboard.txt', 'w') as f:
                for s in leaderboard[:5]:
                    f.write(str(s) + '\n')
            running = False

    for hazard in LANE_HAZARDS:
        hazard_rect = pygame.Rect(hazard[0], hazard[1], hazard[2], hazard[3])
        if player_rect.colliderect(hazard_rect):
            print("Hit Hazard! Game Over! Final Score:", score)
            leaderboard.append(score)
            leaderboard.sort(reverse=True)
            with open('leaderboard.txt', 'w') as f:
                for s in leaderboard[:5]:
                    f.write(str(s) + '\n')
            running = False

    for c in coins[:]:
        coin_rect = pygame.Rect(c[0]-COIN_RADIUS, c[1]-COIN_RADIUS, COIN_RADIUS*2, COIN_RADIUS*2)
        if player_rect.colliderect(coin_rect):
            score += c[2]
            coins.remove(c)

    for cp in checkpoints[:]:
        cp_rect = pygame.Rect(cp[0], cp[1], CHECKPOINT_WIDTH, CHECKPOINT_HEIGHT)
        if player_rect.colliderect(cp_rect):
            checkpoint_passed += 1
            score += 50
            checkpoints.remove(cp)

    for mf in MOVING_FEATURES[:]:
        mf_rect = pygame.Rect(mf[0], mf[1], mf[2], mf[3])
        if player_rect.colliderect(mf_rect):
            speed_multiplier = 0.5
            slow_time = now
            MOVING_FEATURES.remove(mf)

    if score >= level * COINS_TO_LEVELUP:
        level += 1

    screen.fill((0, 100, 0)) 
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, WIDTH, HEIGHT))

    for line in ROAD_LINES:
        pygame.draw.rect(screen, (255, 255, 255), line)
        line[1] += 5 * speed_multiplier
        if line[1] > HEIGHT:
            line[1] = -30

    for hazard in LANE_HAZARDS:
        pygame.draw.rect(screen, (255, 0, 0), hazard)

    for mf in MOVING_FEATURES:
        pygame.draw.rect(screen, (0, 255, 0), (mf[0], mf[1], mf[2], mf[3]))

    for cp in checkpoints:
        pygame.draw.rect(screen, (0, 0, 255), (cp[0], cp[1], CHECKPOINT_WIDTH, CHECKPOINT_HEIGHT))

    if player_img:
        screen.blit(pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT)), (player_x, player_y))
    else:
        pygame.draw.rect(screen, (209, 0, 195), (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    for e in enemy_list:
        if enemy_img:
            screen.blit(pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT)), (e[0], e[1]))
        else:
            pygame.draw.rect(screen, (0, 6, 173), (e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT))

    for o in obstacles:
        if obstacle_img:
            screen.blit(pygame.transform.scale(obstacle_img, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)), (o[0], o[1]))
        else:
            pygame.draw.rect(screen, (139, 69, 19), (o[0], o[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    font = pygame.font.SysFont(None, 24)
    for c in coins:
        if coin_img:
            screen.blit(pygame.transform.scale(coin_img, (COIN_RADIUS*2, COIN_RADIUS*2)), (c[0]-COIN_RADIUS, c[1]-COIN_RADIUS))
        else:
            pygame.draw.circle(screen, (255, 255, 0), (c[0], c[1]), COIN_RADIUS)
        text = font.render(str(c[2]), True, (0,0,0))
        tx, ty = text.get_size()
        screen.blit(text, (c[0]-tx//2, c[1]-ty//2))

    slowdown_time = max(0, (SLOW_DURATION - (now - slow_time)) // 1000)
    if slowdown_time > 0:
        slowdown_surf = font.render(f"SLOWDOWN: {slowdown_time}s", True, (255, 100, 100))
        screen.blit(slowdown_surf, (WIDTH - 200, 10))

    score_surf = font.render(f"Score: {score} Level: {level} Checkpoints: {checkpoint_passed}", True, (255,255,255))
    screen.blit(score_surf, (10, 10))

    leaderboard_surf = font.render("Top Scores:", True, (255,255,255))
    screen.blit(leaderboard_surf, (10, 40))
    for i, s in enumerate(leaderboard[:3]):
        lb_surf = font.render(str(s), True, (255,255,255))
        screen.blit(lb_surf, (10, 60 + i*20))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
