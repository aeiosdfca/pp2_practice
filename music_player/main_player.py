import pygame

pygame.init()
pygame.mixer.init()

WIDTH = 700
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 28)

playlist = [
    "music_player/music/wave_to_earth-love..mp3",
    "music_player/music/Wisp-Your_Face.mp3",
    "music_player/music/Deftones-Sextape.mp3",
    "music_player/music/Deftones-Change.mp3",
    "music_player/music/YENA-Catch_Catch.mp3"
]

current_track = 0
is_playing = False
is_paused = False

clock = pygame.time.Clock()


def get_song_name(index):
    path = playlist[index]
    filename = path.split("/")[-1]
    return filename.replace(".mp3", "")


def play_track():
    global is_playing, is_paused
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.play()
    is_playing = True
    is_paused = False


def stop_track():
    global is_playing, is_paused
    pygame.mixer.music.stop()
    is_playing = False
    is_paused = False


def pause_track():
    global is_playing, is_paused
    if is_playing and not is_paused:
        pygame.mixer.music.pause()
        is_paused = True
        is_playing = False


def resume_track():
    global is_playing, is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
        is_playing = True


def next_track():
    global current_track
    current_track = (current_track + 1) % len(playlist)
    play_track()


def previous_track():
    global current_track
    current_track = (current_track - 1) % len(playlist)
    play_track()


def draw():
    screen.fill((30, 30, 30))

    title = font.render("Music Player", True, (255, 255, 255))
    
    song_name = get_song_name(current_track)
    song = font.render(f"Song: {song_name}", True, (255, 125, 199))
    
    track = font.render(f"Track: {current_track + 1}", True, (255, 125, 199))

    if is_paused:
        status_text = "Paused"
        status_color = (200, 200, 200)
    elif is_playing:
        status_text = "Playing"
        status_color = (255, 125, 199)
    else:
        status_text = "Stopped"
        status_color = (255, 43, 164)
    
    status = font.render(f"Status: {status_text}", True, status_color)

    controls = font.render(
        "P Play | S Stop | E Pause | C Continue | N Next | B Back | Q Quit",
        True,
        (255, 43, 164)
    )

    screen.blit(title, (300, 30))
    screen.blit(song, (200, 90))
    screen.blit(track, (200, 140))
    screen.blit(status, (200, 190))
    screen.blit(controls, (20, 320))


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play_track()

            elif event.key == pygame.K_s:
                stop_track()

            elif event.key == pygame.K_e:
                pause_track()

            elif event.key == pygame.K_c:
                resume_track()

            elif event.key == pygame.K_n:
                next_track()

            elif event.key == pygame.K_b:
                previous_track()

            elif event.key == pygame.K_q:
                running = False

    draw()

    pygame.display.update()
    clock.tick(30)

pygame.quit()