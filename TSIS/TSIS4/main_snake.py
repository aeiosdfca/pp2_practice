import pygame, random, json, psycopg2

pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
FPS = 10

settings_file = 'settings.json'
default_settings = {
    'snake_color': (84, 212, 255),
    'grid_overlay': False,
    'sound': False
}
try:
    with open(settings_file, 'r') as f:
        settings = json.load(f)
except:
    settings = default_settings.copy()

snake_color = settings['snake_color']
grid_overlay = settings['grid_overlay']
sound = settings['sound']

MENU = 0
PLAY = 1
GAME_OVER = 2
LEADERBOARD = 3
SETTINGS = 4
state = MENU

snake = [(200, 200)]
snake_dir = (0, -20)  
snake_length = 3
level = 1
score = 0
speed_boost = False
slow_motion = False
shield = False
power_up_timer = 0
power_up_active = None
player_name = "Player"

foods = []
power_ups = []
obstacles = []

FOOD_SPAWN_TIME = 2000 
last_food_spawn = pygame.time.get_ticks()

food_types = [
    (70, 5, 10000, (0, 255, 0), 1),  
    (20, 8, 7000,  (255, 255, 0), 2), 
    (10, 12, 5000, (255, 0, 0), 3),
    (10, 10, 8000, (139, 0, 0), -2)  
]
weights = [ft[0] for ft in food_types]  

power_up_types = [
    ('speed_boost', (255, 165, 0), 5),  
    ('slow_motion', (0, 191, 255), 5),  
    ('shield', (128, 0, 128), 0)  
]

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="leaderboard_db",
        user="postgres",
        password="12345678"
    )

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            level INTEGER NOT NULL,
            date DATE DEFAULT CURRENT_DATE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_score(name, score, level):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO leaderboard (name, score, level, date) VALUES (%s, %s, %s, CURRENT_DATE)", (name, score, level))
    conn.commit()
    cur.close()
    conn.close()

def get_leaderboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, score, level, date FROM leaderboard ORDER BY score DESC LIMIT 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def spawn_food():
    idx = random.choices(range(len(food_types)), weights=weights, k=1)[0]
    _, radius, life, color, value = food_types[idx]
    while True:
        x = random.randrange(radius, WIDTH - radius, 20)
        y = random.randrange(radius, HEIGHT - radius, 20)
        pos = (x, y)
        if not any(pygame.Rect(x-radius, y-radius, 2*radius, 2*radius).colliderect(obs) for obs in obstacles):
            break
    spawn_time = pygame.time.get_ticks()
    foods.append({"pos": pos, "radius": radius, "spawn": spawn_time, 
                  "life": life, "color": color, "value": value})

def spawn_power_up():
    if power_ups:
        return
    typ, color, duration = random.choice(power_up_types)
    while True:
        x = random.randrange(10, WIDTH - 10, 20)
        y = random.randrange(10, HEIGHT - 10, 20)
        pos = (x, y)
        if not any(pygame.Rect(x-10, y-10, 20, 20).colliderect(obs) for obs in obstacles):
            break
    spawn_time = pygame.time.get_ticks()
    power_ups.append({"pos": pos, "type": typ, "color": color, "spawn": spawn_time, "duration": duration})

def spawn_obstacles():
    obstacles.clear()
    num_blocks = level - 2
    for _ in range(num_blocks):
        while True:
            x = random.randrange(0, WIDTH, 20)
            y = random.randrange(0, HEIGHT, 20)
            rect = pygame.Rect(x, y, 20, 20)
            if not any(rect.colliderect(sx, sy, 20, 20) for sx, sy in snake) and not any(rect.colliderect(obs) for obs in obstacles):
                obstacles.append(rect)
                break

def draw_food(food):
    now = pygame.time.get_ticks()
    elapsed = now - food["spawn"]
    ratio = max(0, 1 - elapsed/food["life"])
    base_color = food["color"]
    fade_color = tuple(int(base_color[i]*ratio + 100*(1-ratio)) for i in range(3))
    pygame.draw.circle(screen, fade_color, food["pos"], food["radius"])
    font = pygame.font.SysFont(None, 20)
    text = font.render(str(food["value"]), True, (0,0,0))
    tx, ty = text.get_size()
    screen.blit(text, (food["pos"][0]-tx//2, food["pos"][1]-ty//2))

def draw_power_up(pu):
    pygame.draw.circle(screen, pu["color"], pu["pos"], 10)
    font = pygame.font.SysFont(None, 16)
    text = font.render(pu["type"][:4], True, (255,255,255))
    tx, ty = text.get_size()
    screen.blit(text, (pu["pos"][0]-tx//2, pu["pos"][1]-ty//2))

def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    if x < mouse[0] < x+w and y < mouse[1] < y+h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.SysFont(None, 24)
    txt = font.render(text, True, (0,0,0))
    screen.blit(txt, (x + w//2 - txt.get_width()//2, y + h//2 - txt.get_height()//2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if state == PLAY:
                if event.key == pygame.K_UP and snake_dir!=(0,20):
                    snake_dir = (0, -20)
                elif event.key == pygame.K_DOWN and snake_dir!=(0,-20):
                    snake_dir = (0, 20)
                elif event.key == pygame.K_LEFT and snake_dir!=(20,0):
                    snake_dir = (-20, 0)
                elif event.key == pygame.K_RIGHT and snake_dir!=(-20,0):
                    snake_dir = (20, 0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == MENU:
                if 150 < event.pos[0] < 250 and 150 < event.pos[1] < 180:
                    state = PLAY
                elif 150 < event.pos[0] < 250 and 200 < event.pos[1] < 230:
                    state = LEADERBOARD
                elif 150 < event.pos[0] < 250 and 250 < event.pos[1] < 280:
                    state = SETTINGS
                elif 150 < event.pos[0] < 250 and 300 < event.pos[1] < 330:
                    running = False
            elif state == GAME_OVER:
                if 100 < event.pos[0] < 200 and 300 < event.pos[1] < 330:
                    save_score(player_name, score, level)
                    snake = [(200, 200)]
                    snake_dir = (0, -20)
                    snake_length = 3
                    level = 1
                    score = 0
                    speed_boost = False
                    slow_motion = False
                    shield = False
                    power_up_timer = 0
                    power_up_active = None
                    foods.clear()
                    power_ups.clear()
                    obstacles.clear()
                    state = PLAY
                elif 200 < event.pos[0] < 300 and 300 < event.pos[1] < 330:
                    state = MENU
            elif state == LEADERBOARD or state == SETTINGS:
                if 150 < event.pos[0] < 250 and 350 < event.pos[1] < 380:
                    state = MENU

    if state == PLAY:
        head_x, head_y = snake[0]
        new_head = (head_x + snake_dir[0], head_y + snake_dir[1])
        snake.insert(0, new_head)
        if len(snake) > snake_length:
            snake.pop() 

        collision = False
        if not shield and (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT):
            collision = True
        if not shield and new_head in snake[1:]:
            collision = True
        if not shield and any(pygame.Rect(new_head[0], new_head[1], 20, 20).colliderect(obs) for obs in obstacles):
            collision = True
        if collision:
            if shield:
                shield = False
            else:
                state = GAME_OVER

        for food in foods[:]:
            fx, fy = food["pos"]
            r = food["radius"]
            food_rect = pygame.Rect(fx-r, fy-r, 2*r, 2*r)
            if pygame.Rect(new_head[0], new_head[1], 20,20).colliderect(food_rect):
                score += food["value"]
                if food["value"] > 0:
                    snake_length += food["value"]
                else:
                    snake_length += food["value"]
                    if snake_length <= 1:
                        state = GAME_OVER
                foods.remove(food)

        for pu in power_ups[:]:
            pu_rect = pygame.Rect(pu["pos"][0]-10, pu["pos"][1]-10, 20, 20)
            if pygame.Rect(new_head[0], new_head[1], 20,20).colliderect(pu_rect):
                power_up_active = pu["type"]
                power_up_timer = pygame.time.get_ticks() + pu["duration"] * 1000
                if pu["type"] == 'speed_boost':
                    speed_boost = True
                elif pu["type"] == 'slow_motion':
                    slow_motion = True
                elif pu["type"] == 'shield':
                    shield = True
                power_ups.remove(pu)

        now = pygame.time.get_ticks()
        if now - last_food_spawn > FOOD_SPAWN_TIME:
            spawn_food()
            last_food_spawn = now

        foods = [f for f in foods if now - f["spawn"] < f["life"]]

        if not power_ups and random.random() < 0.01:
            spawn_power_up()

        power_ups = [p for p in power_ups if now - p["spawn"] < 8000]

        if level >= 3 and not obstacles:
            spawn_obstacles()

        if score >= level * 10:
            level += 1
            if level >= 3:
                spawn_obstacles()

        current_fps = FPS
        if speed_boost and now < power_up_timer:
            current_fps *= 2
        elif slow_motion and now < power_up_timer:
            current_fps //= 2
        if power_up_active and now > power_up_timer:
            power_up_active = None
            speed_boost = False
            slow_motion = False

        screen.fill((199, 199, 199))
        if grid_overlay:
            for x in range(0, WIDTH, 20):
                pygame.draw.line(screen, (150,150,150), (x,0), (x,HEIGHT))
            for y in range(0, HEIGHT, 20):
                pygame.draw.line(screen, (150,150,150), (0,y), (WIDTH,y))

        for obs in obstacles:
            pygame.draw.rect(screen, (0,0,0), obs)

        for i, (x,y) in enumerate(snake):
            color = snake_color if i==0 else (255, 110, 226)
            pygame.draw.rect(screen, color, (x, y, 20, 20))
        for food in foods:
            draw_food(food)
        for pu in power_ups:
            draw_power_up(pu)
        font = pygame.font.SysFont(None, 24)
        scr_text = font.render(f"Score: {score} Level: {level}", True, (0,0,0))
        screen.blit(scr_text, (10, 10))

    elif state == MENU:
        screen.fill((100, 100, 100))
        font = pygame.font.SysFont(None, 36)
        title = font.render("Snake Game", True, (255,255,255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        draw_button("Play", 150, 150, 100, 30, (200,200,200), (255,255,255))
        draw_button("Leaderboard", 150, 200, 100, 30, (200,200,200), (255,255,255))
        draw_button("Settings", 150, 250, 100, 30, (200,200,200), (255,255,255))
        draw_button("Quit", 150, 300, 100, 30, (200,200,200), (255,255,255))

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
        leaderboard = get_leaderboard()
        y_offset = 60
        for i, (name, score, level, date) in enumerate(leaderboard):
            entry_text = font.render(f"{i+1}. {name} - Score: {score} Level: {level} Date: {date}", True, (255,255,255))
            screen.blit(entry_text, (20, y_offset))
            y_offset += 30
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
        color_text = font.render(f"Snake Color: {snake_color}", True, (255,255,255))
        screen.blit(color_text, (50, 120))
        draw_button("Save & Back", 150, 350, 100, 30, (200,200,200), (255,255,255))

    pygame.display.update()
    if state == PLAY:
        clock.tick(current_fps)
    else:
        clock.tick(30)

pygame.quit()
