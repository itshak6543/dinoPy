import pygame
import random

pygame.init()

WINDOW_WIDTH = 650
WINDOW_HEIGHT = 400
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("dino")

dino_x = 100
dino_y = 160
dino_width = 50
dino_height = 50
dino_velocity = 0
jump_strength = -11
ground_y = 150

dino_image = pygame.image.load("Frame 1 (3).png")
dino_image = pygame.transform.scale(dino_image, (dino_width, dino_height))

cactus_width = 20
cactus_height = 30
cactus_image = pygame.image.load("cactus.png")
cactus_image = pygame.transform.scale(cactus_image, (cactus_width, cactus_height))
cactus_speed = 3
cacti = []

cloud_image = pygame.image.load("cloud.png")
clouds = []

background_frames = [
    pygame.transform.scale(pygame.image.load("backround.png"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("backround2.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
]
current_background = 0
frame_counter = 0

font = pygame.font.SysFont(None, 28)

clock = pygame.time.Clock()
running = True
gravity = 0.5
game_over = False
score = 0

group_interval = 2000
min_group_interval = 1300
last_group_time = pygame.time.get_ticks()


def spawn_cactus_group():
    global cacti
    x = WINDOW_WIDTH
    y = ground_y + 20
    group_size = 1
    if random.random() < 0.5:
        group_size = 2
    for i in range(group_size):
        cacti.append(pygame.Rect(x + i * (cactus_width + 5), y, cactus_width, cactus_height))


def spawn_cloud():
    x = WINDOW_WIDTH
    y = random.randint(5, 50)
    scale = random.uniform(0.5, 1.0)
    width = int(40 * scale)
    height = int(25 * scale)
    speed_mult = random.uniform(0.3, 0.7)
    clouds.append({"rect": pygame.Rect(x, y, width, height), "speed_mult": speed_mult})


def reset_game():
    global dino_y, dino_velocity, cacti, last_group_time, game_over, score, cactus_speed, group_interval
    dino_y = 160
    dino_velocity = 0
    cacti = []
    clouds.clear()
    spawn_cactus_group()
    last_group_time = pygame.time.get_ticks()
    game_over = False
    score = 0
    cactus_speed = 3
    group_interval = 2000


spawn_cactus_group()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and dino_y >= ground_y:
                dino_velocity = jump_strength
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset_game()

    if not game_over:
        dino_velocity += gravity
        dino_y += dino_velocity
        if dino_y > ground_y:
            dino_y = ground_y
            dino_velocity = 0

        for cactus in cacti:
            cactus.x -= cactus_speed
        cacti = [cactus for cactus in cacti if cactus.x + cactus_width > 0]

        current_time = pygame.time.get_ticks()
        if current_time - last_group_time >= group_interval:
            spawn_cactus_group()
            last_group_time = current_time

        if random.random() < 0.05:
            spawn_cloud()
        for cloud in clouds:
            cloud["rect"].x -= cactus_speed * cloud["speed_mult"]
        clouds = [cloud for cloud in clouds if cloud["rect"].x + cloud["rect"].width > 0]

        frame_counter += 1
        if frame_counter >= 5:
            current_background = (current_background + 1) % len(background_frames)
            frame_counter = 0

        dino_rect = pygame.Rect(dino_x + 10, dino_y + 10, dino_width - 20, dino_height - 10)
        for cactus in cacti:
            if dino_rect.colliderect(cactus):
                game_over = True
                break

        score += 1
        if score % 100 == 0:
            cactus_speed += 0.02
            group_interval = max(min_group_interval, group_interval - 20)

    screen.blit(background_frames[current_background], (0, 0))

    for cloud in clouds:
        screen.blit(pygame.transform.scale(cloud_image, (cloud["rect"].width, cloud["rect"].height)),
                    (cloud["rect"].x, cloud["rect"].y))

    screen.blit(dino_image, (dino_x, dino_y))
    for cactus in cacti:
        screen.blit(cactus_image, (cactus.x, cactus.y))

    score_text = font.render(f"Score: {score}", True, (50, 50, 50))
    screen.blit(score_text, (15, 0))

    if game_over:
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2,
                           WINDOW_HEIGHT // 2 - text.get_height() // 2))
        info_text = font.render("PRESS ENTER TO RESTART", True, (0, 255, 0))
        screen.blit(info_text, (WINDOW_WIDTH // 2 - info_text.get_width() // 2,
                                WINDOW_HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(60)
