import pygame
import random
from pycollision import Collision


pygame.init()

screen = pygame.display.set_mode((1000, 800))

player_rect = pygame.Rect(0, 0, 50, 50)

collision_check = Collision(r"TestImages/sample.png", (50, 50), wall_collision=True)
collision_object = pygame.image.load(r"TestImages/sample.png").convert_alpha()

colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in
          range(len(collision_check.collision_points()))]

running = True
speed = 1
pos_x, pos_y = (10, 10)

bgx, bgy = (0, 0)
bg_speed = 0.05

offset = 0

coll_font = pygame.font.SysFont('Consolas', 50)

while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    key_press = pygame.key.get_pressed()

    topLeft, _ = collision_check.smart_check((pos_x, pos_y), coll_pos=(bgx, bgy), offset=offset)
    topRight, _ = collision_check.smart_check((pos_x + player_rect.width, pos_y), coll_pos=(bgx, bgy),offset=offset)
    bottomRight, _ = collision_check.smart_check((pos_x + player_rect.width, pos_y + player_rect.height),
                                                 coll_pos=(bgx, bgy), offset=offset)
    bottomLeft, _ = collision_check.smart_check((pos_x, pos_y + player_rect.height),
                                                coll_pos=(bgx, bgy), offset=offset)

    if any((topLeft, bottomLeft, bottomRight, topRight)):
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

    screen.blit(collision_object, (bgx, bgy))

    bgx += bg_speed
    bgy += bg_speed

    if bgx >= 400:
        bg_speed = -0.05

    if bgx <= 50:
        bg_speed = 0.05

    for color, x in zip(colors, collision_check.collision_points()):
        x = (x[0]+bgx, x[1]+bgy, x[2] - x[0], x[3] - x[1])
        pygame.draw.rect(screen, color, pygame.Rect(x), width=3)

    player_rect = pygame.Rect(pos_x, pos_y, 50, 50)
    pygame.draw.rect(screen, (0, 0, 0),player_rect )

    pygame.display.update()
