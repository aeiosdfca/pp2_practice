import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

radius = 25
x = WIDTH // 2
y = HEIGHT // 2
step = 20

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if y - step >= radius:
            y -= step

    if keys[pygame.K_DOWN]:
        if y + step <= HEIGHT - radius:
            y += step

    if keys[pygame.K_LEFT]:
        if x - step >= radius:
            x -= step

    if keys[pygame.K_RIGHT]:
        if x + step <= WIDTH - radius:
            x += step

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (255, 8, 149), (x, y), radius)

    pygame.display.update()
    clock.tick(30)

pygame.quit()