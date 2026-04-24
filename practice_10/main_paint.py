import pygame, sys
pygame.init()

WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

canvas = []  
current_shape = "Square"
dragging = False
start_pos = None

font = pygame.font.SysFont(None, 20)

def draw_all():
    screen.fill((255,255,255))
    for shape, pts in canvas:
        if shape == "Square":
            pygame.draw.rect(screen, (247, 94, 237), pts, 2)
        elif shape == "RightTriangle":
            pygame.draw.polygon(screen, (247, 94, 237), pts, 2)
        elif shape == "Equilateral":
            pygame.draw.polygon(screen, (247, 94, 237), pts, 2)
        elif shape == "Rhombus":
            pygame.draw.polygon(screen, (247, 94, 237), pts, 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key in (pygame.K_q, pygame.K_ESCAPE)):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                current_shape = "Square"
            elif event.key == pygame.K_t:
                current_shape = "RightTriangle"
            elif event.key == pygame.K_e:
                current_shape = "Equilateral"
            elif event.key == pygame.K_r:
                current_shape = "Rhombus"
            elif event.key == pygame.K_c:
                canvas.clear()
            elif event.key == pygame.K_p:
                pygame.image.save(screen, "drawing.png")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            end_pos = event.pos
            dragging = False
            x1,y1 = start_pos
            x2,y2 = end_pos
            shape_pts = []
            if current_shape == "Square":
                side = max(abs(x2-x1), abs(y2-y1))
                sx = x1 + (side if x2>=x1 else -side)
                sy = y1 + (side if y2>=y1 else -side)
                rect_left = min(x1, sx)
                rect_top = min(y1, sy)
                shape_pts = [rect_left, rect_top, side, side] 
                canvas.append(("Square", pygame.Rect(rect_left, rect_top, side, side)))

            elif current_shape == "RightTriangle":
                shape_pts = [(x1,y1), (x2,y1), (x1,y2)]
                canvas.append(("RightTriangle", shape_pts))

            elif current_shape == "Equilateral":
                dx, dy = x2-x1, y2-y1
                L = (dx**2 + dy**2) ** 0.5
                if L < 1: 
                    continue
                mx, my = (x1+x2)/2, (y1+y2)/2
                ux, uy = -dy/L, dx/L
                h = (3**0.5)/2 * L
                cx = mx + ux * h
                cy = my + uy * h
                shape_pts = [(x1,y1), (x2,y2), (int(cx), int(cy))]
                canvas.append(("Equilateral", shape_pts))

            elif current_shape == "Rhombus":
                dx, dy = x2-x1, y2-y1
                px, py = -dy, dx
                shape_pts = [(x1,y1), (x2,y2), (x2+px, y2+py), (x1+px, y1+py)]
                canvas.append(("Rhombus", shape_pts))

    draw_all()
    if dragging and start_pos:
        mx,my = pygame.mouse.get_pos()
        x1,y1 = start_pos; x2,y2 = mx,my
        if current_shape == "Square":
            side = max(abs(x2-x1), abs(y2-y1))
            sx = x1 + (side if x2>=x1 else -side)
            sy = y1 + (side if y2>=y1 else -side)
            rect = pygame.Rect(min(x1,sx), min(y1,sy), side, side)
            pygame.draw.rect(screen, (200,200,200), rect, 1)
        elif current_shape == "RightTriangle":
            pts = [(x1,y1), (x2,y1), (x1,y2)]
            pygame.draw.polygon(screen, (200,200,200), pts, 1)
        elif current_shape == "Equilateral":
            dx, dy = x2-x1, y2-y1
            L = (dx**2 + dy**2) ** 0.5
            if L >= 1:
                mx2, my2 = (x1+x2)/2, (y1+y2)/2
                ux, uy = -dy/L, dx/L
                h = (3**0.5)/2 * L
                cx, cy = mx2 + ux*h, my2 + uy*h
                pts = [(x1,y1), (x2,y2), (int(cx), int(cy))]
                pygame.draw.polygon(screen, (200,200,200), pts, 1)
        elif current_shape == "Rhombus":
            dx, dy = x2-x1, y2-y1
            px, py = -dy, dx
            pts = [(x1,y1), (x2,y2), (x2+px, y2+py), (x1+px, y1+py)]
            pygame.draw.polygon(screen, (200,200,200), pts, 1)

    instructions = [
        f"Shape: {current_shape} (S/T/E/R)",
        "C: Clear, P: Save PNG, Esc/Q: Quit"
    ]
    for i, text in enumerate(instructions):
        surf = font.render(text, True, (100,100,100))
        screen.blit(surf, (10, HEIGHT-30 + i*15))

    pygame.display.update()
    clock.tick(60)
