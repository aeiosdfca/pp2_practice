import pygame, random, time
pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
FPS = 10

snake = [(200, 200)]
snake_dir = (0, -20)  
snake_length = 3

foods = []
FOOD_SPAWN_TIME = 2000 
last_food_spawn = pygame.time.get_ticks()

food_types = [
    (70, 5, 10000, (0, 255, 0), 1),  
    (20, 8, 7000,  (255, 255, 0), 2), 
    (10, 12, 5000, (255, 0, 0), 3)  
]
weights = [ft[0] for ft in food_types]  

score = 0

def spawn_food():
    idx = random.choices(range(len(food_types)), weights=weights, k=1)[0]
    _, radius, life, color, value = food_types[idx]
    x = random.randrange(radius, WIDTH - radius, 20)
    y = random.randrange(radius, HEIGHT - radius, 20)
    spawn_time = pygame.time.get_ticks()
    foods.append({"pos": (x,y), "radius": radius, "spawn": spawn_time, 
                  "life": life, "color": color, "value": value})

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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir!=(0,20):
                snake_dir = (0, -20)
            elif event.key == pygame.K_DOWN and snake_dir!=(0,-20):
                snake_dir = (0, 20)
            elif event.key == pygame.K_LEFT and snake_dir!=(20,0):
                snake_dir = (-20, 0)
            elif event.key == pygame.K_RIGHT and snake_dir!=(-20,0):
                snake_dir = (20, 0)

    head_x, head_y = snake[0]
    new_head = (head_x + snake_dir[0], head_y + snake_dir[1])
    snake.insert(0, new_head)
    if len(snake) > snake_length:
        snake.pop() 


    if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT):
        print("Snake hit wall! Final Score:", score)
        running = False

    if new_head in snake[1:]:
        print("Snake collided with itself! Final Score:", score)
        running = False

    for food in foods[:]:
        fx, fy = food["pos"]
        r = food["radius"]
        food_rect = pygame.Rect(fx-r, fy-r, 2*r, 2*r)
        if pygame.Rect(new_head[0], new_head[1], 1,1).colliderect(food_rect):
            score += food["value"]
            snake_length += food["value"]  
            foods.remove(food)

    now = pygame.time.get_ticks()
    if now - last_food_spawn > FOOD_SPAWN_TIME:
        spawn_food()
        last_food_spawn = now

    foods = [f for f in foods if now - f["spawn"] < f["life"]]

    screen.fill((199, 199, 199))
    for i, (x,y) in enumerate(snake):
        color = (84, 212, 255) if i==0 else (255, 110, 226)
        pygame.draw.rect(screen, color, (x, y, 20, 20))
    for food in foods:
        draw_food(food)
    font = pygame.font.SysFont(None, 24)
    scr_text = font.render(f"Score: {score}", True, (0,0,0))
    screen.blit(scr_text, (10, 10))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
