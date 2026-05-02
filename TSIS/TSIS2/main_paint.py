import pygame, sys, datetime
pygame.init()

WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

canvas = []
current_tool = "Square"
dragging = False
start_pos = None
brush_size = 2
text_input = ""
text_pos = None
text_active = False
color = (247, 94, 237)

font = pygame.font.SysFont(None, 20)
canvas_surface = pygame.Surface((WIDTH, HEIGHT))

def draw_all():
    canvas_surface.fill((255,255,255))
    for item in canvas:
        typ = item['type']
        pts = item['pts']
        col = item['color']
        sz = item['size']
        if typ == "Square":
            pygame.draw.rect(canvas_surface, col, pts, sz)
        elif typ in ["RightTriangle", "Equilateral", "Rhombus"]:
            pygame.draw.polygon(canvas_surface, col, pts, sz)
        elif typ == "Line":
            pygame.draw.line(canvas_surface, col, pts[0], pts[1], sz)
        elif typ in ["Pencil", "Eraser"]:
            for i in range(1, len(pts)):
                pygame.draw.line(canvas_surface, col, pts[i-1], pts[i], sz)
        elif typ == "Text":
            surf = font.render(pts, True, col)
            canvas_surface.blit(surf, item['pos'])
        elif typ == "Fill":
            flood_fill(canvas_surface, pts[0], pts[1], col)

def flood_fill(surface, x, y, new_color, old_color=None):
    if old_color is None:
        old_color = surface.get_at((x, y))
    if old_color == new_color:
        return
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if surface.get_at((cx, cy)) != old_color:
            continue
        surface.set_at((cx, cy), new_color)
        if cx > 0:
            stack.append((cx-1, cy))
        if cx < WIDTH-1:
            stack.append((cx+1, cy))
        if cy > 0:
            stack.append((cx, cy-1))
        if cy < HEIGHT-1:
            stack.append((cx, cy+1))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key in (pygame.K_q, pygame.K_ESCAPE)):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_CTRL and event.key == pygame.K_s:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                pygame.image.save(canvas_surface, f"drawing_{timestamp}.png")
                print(f"Saved as drawing_{timestamp}.png")
            elif text_active:
                if event.key == pygame.K_RETURN:
                    canvas.append({'type': 'Text', 'pts': text_input, 'color': color, 'size': brush_size, 'pos': text_pos})
                    text_input = ""
                    text_active = False
                elif event.key == pygame.K_ESCAPE:
                    text_input = ""
                    text_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode
            else:
                if event.key == pygame.K_s:
                    current_tool = "Square"
                elif event.key == pygame.K_t:
                    current_tool = "RightTriangle"
                elif event.key == pygame.K_e:
                    current_tool = "Equilateral"
                elif event.key == pygame.K_r:
                    current_tool = "Rhombus"
                elif event.key == pygame.K_l:
                    current_tool = "Line"
                elif event.key == pygame.K_p:
                    current_tool = "Pencil"
                elif event.key == pygame.K_f:
                    current_tool = "Fill"
                elif event.key == pygame.K_x:
                    current_tool = "Text"
                elif event.key == pygame.K_d:
                    current_tool = "Eraser"
                elif event.key == pygame.K_c:
                    canvas.clear()
                elif event.key == pygame.K_1:
                    brush_size = 1
                elif event.key == pygame.K_2:
                    brush_size = 2
                elif event.key == pygame.K_3:
                    brush_size = 3
                elif event.key == pygame.K_4:
                    color = (255, 0, 0)  # red
                elif event.key == pygame.K_5:
                    color = (0, 255, 0)  # green
                elif event.key == pygame.K_6:
                    color = (0, 0, 255)  # blue
                elif event.key == pygame.K_7:
                    color = (255, 255, 0)  # yellow
                elif event.key == pygame.K_8:
                    color = (255, 0, 255)  # magenta
                elif event.key == pygame.K_9:
                    color = (0, 255, 255)  # cyan
                elif event.key == pygame.K_0:
                    color = (247, 94, 237)  # default pink

        elif event.type == pygame.MOUSEBUTTONDOWN and not text_active:
            if current_tool == "Fill":
                mx, my = event.pos
                flood_fill(canvas_surface, mx, my, color)
                canvas.append({'type': 'Fill', 'pts': (mx, my), 'color': color, 'size': 0})
            elif current_tool == "Text":
                text_pos = event.pos
                text_active = True
            else:
                dragging = True
                start_pos = event.pos
                if current_tool in ["Pencil", "Eraser"]:
                    erase_color = (255, 255, 255) if current_tool == "Eraser" else color
                    canvas.append({'type': current_tool, 'pts': [event.pos], 'color': erase_color, 'size': brush_size})

        elif event.type == pygame.MOUSEMOTION and dragging and current_tool in ["Pencil", "Eraser"]:
            canvas[-1]['pts'].append(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            end_pos = event.pos
            dragging = False
            x1,y1 = start_pos
            x2,y2 = end_pos
            if current_tool == "Square":
                side = max(abs(x2-x1), abs(y2-y1))
                sx = x1 + (side if x2>=x1 else -side)
                sy = y1 + (side if y2>=y1 else -side)
                rect_left = min(x1, sx)
                rect_top = min(y1, sy)
                canvas.append({'type': "Square", 'pts': pygame.Rect(rect_left, rect_top, side, side), 'color': color, 'size': brush_size})
            elif current_tool == "RightTriangle":
                pts = [(x1,y1), (x2,y1), (x1,y2)]
                canvas.append({'type': "RightTriangle", 'pts': pts, 'color': color, 'size': brush_size})
            elif current_tool == "Equilateral":
                dx, dy = x2-x1, y2-y1
                L = (dx**2 + dy**2) ** 0.5
                if L < 1: 
                    continue
                mx, my = (x1+x2)/2, (y1+y2)/2
                ux, uy = -dy/L, dx/L
                h = (3**0.5)/2 * L
                cx = mx + ux * h
                cy = my + uy * h
                pts = [(x1,y1), (x2,y2), (int(cx), int(cy))]
                canvas.append({'type': "Equilateral", 'pts': pts, 'color': color, 'size': brush_size})
            elif current_tool == "Rhombus":
                dx, dy = x2-x1, y2-y1
                px, py = -dy, dx
                pts = [(x1,y1), (x2,y2), (x2+px, y2+py), (x1+px, y1+py)]
                canvas.append({'type': "Rhombus", 'pts': pts, 'color': color, 'size': brush_size})
            elif current_tool == "Line":
                canvas.append({'type': "Line", 'pts': [start_pos, end_pos], 'color': color, 'size': brush_size})

    draw_all()
    screen.blit(canvas_surface, (0, 0))
    if dragging and start_pos and current_tool not in ["Pencil", "Eraser"]:
        mx,my = pygame.mouse.get_pos()
        x1,y1 = start_pos; x2,y2 = mx,my
        if current_tool == "Square":
            side = max(abs(x2-x1), abs(y2-y1))
            sx = x1 + (side if x2>=x1 else -side)
            sy = y1 + (side if y2>=y1 else -side)
            rect = pygame.Rect(min(x1,sx), min(y1,sy), side, side)
            pygame.draw.rect(screen, (200,200,200), rect, brush_size)
        elif current_tool == "RightTriangle":
            pts = [(x1,y1), (x2,y1), (x1,y2)]
            pygame.draw.polygon(screen, (200,200,200), pts, brush_size)
        elif current_tool == "Equilateral":
            dx, dy = x2-x1, y2-y1
            L = (dx**2 + dy**2) ** 0.5
            if L >= 1:
                mx2, my2 = (x1+x2)/2, (y1+y2)/2
                ux, uy = -dy/L, dx/L
                h = (3**0.5)/2 * L
                cx, cy = mx2 + ux*h, my2 + uy*h
                pts = [(x1,y1), (x2,y2), (int(cx), int(cy))]
                pygame.draw.polygon(screen, (200,200,200), pts, brush_size)
        elif current_tool == "Rhombus":
            dx, dy = x2-x1, y2-y1
            px, py = -dy, dx
            pts = [(x1,y1), (x2,y2), (x2+px, y2+py), (x1+px, y1+py)]
            pygame.draw.polygon(screen, (200,200,200), pts, brush_size)
        elif current_tool == "Line":
            pygame.draw.line(screen, (200,200,200), start_pos, (mx, my), brush_size)

    if text_active and text_pos:
        surf = font.render(text_input, True, (200,200,200))
        screen.blit(surf, text_pos)

    instructions = [
        f"Tool: {current_tool} (S/T/E/R/L/P/F/X/D)",
        f"Brush: {brush_size} (1/2/3), Colors: 4-0, C: Clear, Ctrl+S: Save, Esc/Q: Quit"
    ]
    for i, text in enumerate(instructions):
        surf = font.render(text, True, (100,100,100))
        screen.blit(surf, (10, HEIGHT-30 + i*15))

    pygame.display.update()
    clock.tick(60)
