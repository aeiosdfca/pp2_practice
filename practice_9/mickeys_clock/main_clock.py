import pygame
import math
import datetime

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()
hand = pygame.image.load("mickeys_clock/images/mickey_hand.png")
h_hand = pygame.transform.scale(hand, (150, 200))
m_hand = pygame.transform.scale(hand, (100, 125))
s_hand = pygame.transform.scale(hand, (60, 75))

font = pygame.font.SysFont("Arial", 28, bold=True)

center = (WIDTH // 2, HEIGHT // 2)


def rotate_hand(image, angle):
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect(center=center)
    return rotated, rect


def draw_numbers():
    radius = 190
    for num in range(1, 13):
        angle = math.radians(num * 30 - 90)

        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)

        text = font.render(str(num), True, (0, 0, 0))
        rect = text.get_rect(center=(x, y))

        screen.blit(text, rect)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 0), center, 220, 3)
    draw_numbers()

    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    hour_angle = -6 * hour
    minute_angle = -6 * minute
    second_angle = -6 * second

    middle_hand, middle_rect = rotate_hand(h_hand, hour_angle)
    right_hand, right_rect = rotate_hand(m_hand, minute_angle)
    left_hand, left_rect = rotate_hand(s_hand, second_angle)

    screen.blit(middle_hand, middle_rect)
    screen.blit(right_hand, right_rect)
    screen.blit(left_hand, left_rect)

    pygame.display.update()
    clock.tick(1)

pygame.quit()