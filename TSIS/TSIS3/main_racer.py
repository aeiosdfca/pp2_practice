import pygame, random, os, json
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
FPS = 30  

settings_file = 'settings.json'
default_settings = {
    'snake_color': (84, 212, 255),
    'grid_overlay': False,
    'sound': False,
    'difficulty': 'medium'
}
try:
    with open(settings_file, 'r') as f:
        settings = json.load(f)
except:
    settings = default_settings.copy()

snake_color = settings['snake_color']
grid_overlay = settings['grid_overlay']
sound = settings['sound']
difficulty = settings['difficulty']

MENU = 0
PLAY = 1
GAME_OVER = 2
LEADERBOARD = 3
SETTINGS = 4
state = MENU

username = ""
input_active = False

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

leaderboard_file = 'leaderboard.json'
leaderboard = []
try:
    with open(leaderboard_file, 'r') as f:
        leaderboard = json.load(f)
except:
    leaderboard = []

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

if os.path.exists(os.path.join(script_dir, 'obstacle.png')):
    obstacle_img = pygame.image.load(os.path.join(script_dir, 'obstacle.png'))
    print(f"Loaded obstacle.png from {script_dir}")
else:
    print(f"obstacle.png not found in {script_dir}")

if os.path.exists(os.path.join(script_dir, 'coin.png')):
    coin_img = pygame.image.load(os.path.join(script_dir, 'coin.png'))
    print(f"Loaded coin.png from {script_dir}")
else:
    print(f"coin.png not found in {script_dir}")

def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    if x < mouse[0] < x+w and y < mouse[1] < y+h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.SysFont(None, 24)
    txt = font.render(text, True, (0,0,0))
    screen.blit(txt, (x + w//2 - txt.get_width()//2, y + h//2 - txt.get_height()//2))

def save_leaderboard():
    with open(leaderboard_file, 'w') as f:
        json.dump(leaderboard, f)

def save_settings():
    settings['snake_color'] = snake_color
    settings['grid_overlay'] = grid_overlay
    settings['sound'] = sound
    settings['difficulty'] = difficulty
    with open(settings_file, 'w') as f:
        json.dump(settings, f)

slow_time = 0
SLOW_DURATION = 3000
speed_multiplier = 1.0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if state == MENU and input_active:
                if event.key == pygame.K_RETURN and username:
                    state = PLAY
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
            elif state == PLAY:
                if event.key == pygame.K_LEFT:
                    player_x -= player_speed
                elif event.key == pygame.K_RIGHT:
                    player_x += player_speed
                player_x = max(0, min(WIDTH-PLAYER_WIDTH, player_x))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == MENU:
                if not input_active:
                    if 150 < event.pos[0] < 250 and 150 < event.pos[1] < 180:
                        input_active = True
                    elif 150 < event.pos[0] < 250 and 200 < event.pos[1] < 230:
                        state = LEADERBOARD
                    elif 150 < event.pos[0] < 250 and 250 < event.pos[1] < 280:
                        state = SETTINGS
                    elif 150 < event.pos[0] < 250 and 300 < event.pos[1] < 330:
                        running = False
            elif state == GAME_OVER:
                if 100 < event.pos[0] < 200 and 300 < event.pos[1] < 330:
                    player_x = WIDTH//2 - PLAYER_WIDTH//2
                    player_y = HEIGHT - PLAYER_HEIGHT - 10
                    enemy_list = [[random.randint(0, WIDTH-ENEMY_WIDTH), -ENEMY_HEIGHT, enemy_speed] for _ in range(3)]
                    coins.clear()
                    obstacles.clear()
                    checkpoints.clear()
                    LANE_HAZARDS = []
                    for i in range(3):
                        lane_x = (WIDTH // 4) * (i + 1) - 10
                        LANE_HAZARDS.append([lane_x, random.randint(0, HEIGHT), 20, 20])
                    MOVING_FEATURES.clear()
                    score = 0
                    level = 1
                    checkpoint_passed = 0
                    slow_time = 0
                    speed_multiplier = 1.0
                    state = PLAY
                elif 200 < event.pos[0] < 300 and 300 < event.pos[1] < 330:
                    state = MENU
            elif state == LEADERBOARD or state == SETTINGS:
                if 150 < event.pos[0] < 250 and 350 < event.pos[1] < 380:
                    state = MENU

    if state == PLAY:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        player_x = max(0, min(WIDTH-PLAYER_WIDTH, player_x))

        now = pygame.time.get_ticks()

        if now - slow_time > SLOW_DURATION:
            speed_multiplier = 1.0 + (checkpoint_passed * 0.1)

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
            mf[0] += mf[4] * speed_multiplier
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
                leaderboard.append({"username": username, "score": score, "level": level})
                leaderboard.sort(key=lambda x: x["score"], reverse=True)
                leaderboard = leaderboard[:10]
                save_leaderboard()
                state = GAME_OVER

        for o in obstacles:
            obs_rect = pygame.Rect(o[0], o[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
            if player_rect.colliderect(obs_rect):
                print("Hit Obstacle! Game Over! Final Score:", score)
                leaderboard.append({"username": username, "score": score, "level": level})
                leaderboard.sort(key=lambda x: x["score"], reverse=True)
                leaderboard = leaderboard[:10]
                save_leaderboard()
                state = GAME_OVER

        for hazard in LANE_HAZARDS:
            hazard_rect = pygame.Rect(hazard[0], hazard[1], hazard[2], hazard[3])
            if player_rect.colliderect(hazard_rect):
                print("Hit Hazard! Game Over! Final Score:", score)
                leaderboard.append({"username": username, "score": score, "level": level})
                leaderboard.sort(key=lambda x: x["score"], reverse=True)
                leaderboard = leaderboard[:10]
                save_leaderboard()
                state = GAME_OVER

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
            pygame.draw.rect(screen, snake_color, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

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
            lb_surf = font.render(f"{s['username']}: {s['score']}", True, (255,255,255))
            screen.blit(lb_surf, (10, 60 + i*20))

    elif state == MENU:
        screen.fill((100, 100, 100))
        font = pygame.font.SysFont(None, 36)
        title = font.render("Racer Game", True, (255,255,255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        draw_button("Enter Username", 150, 150, 100, 30, (200,200,200), (255,255,255))
        draw_button("Leaderboard", 150, 200, 100, 30, (200,200,200), (255,255,255))
        draw_button("Settings", 150, 250, 100, 30, (200,200,200), (255,255,255))
        draw_button("Quit", 150, 300, 100, 30, (200,200,200), (255,255,255))
        if input_active:
            input_text = font.render(f"Username: {username}", True, (255,255,255))
            screen.blit(input_text, (WIDTH//2 - input_text.get_width()//2, 120))

    elif state == GAME_OVER:
        screen.fill((100, 100, 100))
        font = pygame.font.SysFont(None, 36)
        go_text = font.render("Game Over", True, (255,0,0))
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, 100))
        score_text = font.render(f"Score: {score} Level: {level}", True, (255,255,255))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 150))
        draw_button("Retry", 100, 300, 100, 30, (200,200,200), (255,255,255))
        draw_button("Menu", 200, 300, 100, 30, (200,200,200), (255,255,255))

    elif state == LEADERBOARD:
        screen.fill((100, 100, 100))
        font = pygame.font.SysFont(None, 24)
        lb_text = font.render("Leaderboard", True, (255,255,255))
        screen.blit(lb_text, (WIDTH//2 - lb_text.get_width()//2, 20))
        for i, entry in enumerate(leaderboard):
            entry_text = font.render(f"{i+1}. {entry['username']} - {entry['score']} (Lv{entry['level']})", True, (255,255,255))
            screen.blit(entry_text, (50, 60 + i*25))
        draw_button("Back", 150, 350, 100, 30, (200,200,200), (255,255,255))

    elif state == SETTINGS:
        screen.fill((100, 100, 100))
        font = pygame.font.SysFont(None, 24)
        set_text = font.render("Settings", True, (255,255,255))
        screen.blit(set_text, (WIDTH//2 - set_text.get_width()//2, 20))
        grid_text = font.render(f"Grid: {'On' if grid_overlay else 'Off'}", True, (255,255,255))
        screen.blit(grid_text, (50, 60))
        sound_text = font.render(f"Sound: {'On' if sound else 'Off'}", True, (255,255,255))
        screen.blit(sound_text, (50, 90))
        color_text = font.render(f"Car Color: {snake_color}", True, (255,255,255))
        screen.blit(color_text, (50, 120))
        diff_text = font.render(f"Difficulty: {difficulty}", True, (255,255,255))
        screen.blit(diff_text, (50, 150))
        draw_button("Save & Back", 150, 350, 100, 30, (200,200,200), (255,255,255))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
