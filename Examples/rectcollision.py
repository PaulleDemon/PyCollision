import pygame
import random
from pycollision import Collision


pygame.init()

screen = pygame.display.set_mode((1000, 800))

player_rect = pygame.Rect(0, 0, 50, 50)

collision_check = Collision(r"TestImages/sample.png", (20, 50), optimize=True, optimize_padding=(3, 1, 1, 1)) # optimize_padding(left, top, right, bottom)
collision_object = pygame.image.load(r"TestImages/sample.png").convert_alpha()

colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in
          range(len(collision_check.collision_points()))]

running = True
speed = 0.3
pos_x, pos_y = (10, 10)

coll_font = pygame.font.SysFont('Consolas', 50)

while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    key_press = pygame.key.get_pressed()

    rect = (player_rect.x, player_rect.y, player_rect.x+player_rect.width, player_rect.y+player_rect.height)
    inside, pos = collision_check.check_rect_collision(rect)

    if inside:
        screen.fill((255, 16, 8))
        screen.blit(coll_font.render("Collision", True, (255, 255, 255)), (50, 50))

    if key_press[pygame.K_a]:
        pos_x -= speed

    if key_press[pygame.K_w]:
        pos_y -= speed

    if key_press[pygame.K_d]:
        pos_x += speed

    if key_press[pygame.K_s]:
        pos_y += speed

    screen.blit(collision_object, (0, 0))

    for color, x in zip(colors, collision_check.collision_points()):
        x = (x[0], x[1], x[2] - x[0], x[3] - x[1])
        pygame.draw.rect(screen, color, pygame.Rect(x), width=3)

    player_rect = pygame.Rect(pos_x, pos_y, 50, 50)
    pygame.draw.rect(screen, (0, 0, 0),player_rect )

    pygame.display.update()
