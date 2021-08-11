import pygame
import random
from pycollision import Collision

pygame.init()

screen = pygame.display.set_mode((1000, 800))

player_rect = pygame.Rect(0, 0, 50, 50)

collision_check = Collision(r"Examples/TestImages/sample.png", (15, 15), optimize=True)
collision_object = pygame.image.load(r"Examples/TestImages/sample.png").convert_alpha()

colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in
          range(len(collision_check.collision_points()))]

running = True
speed = 1.5
pos_x, pos_y = (10, 10)

offset = 0

while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    key_press = pygame.key.get_pressed()

    topLeft, _ = collision_check.smart_check((pos_x, pos_y), offset=offset)
    topRight, _ = collision_check.smart_check((pos_x + player_rect.width, pos_y),offset=offset)
    bottomRight, _ = collision_check.smart_check((pos_x + player_rect.width, pos_y + player_rect.height), offset=offset)
    bottomLeft, _ = collision_check.smart_check((pos_x, pos_y + player_rect.height), offset=offset)

    if key_press[pygame.K_a] and not any((topLeft, bottomLeft)) and pos_x >= 0:
        pos_x -= speed

    if key_press[pygame.K_w] and not any((topLeft, topRight)) and pos_y >= 0:
        pos_y -= speed

    if key_press[pygame.K_d] and not any((bottomRight, topRight)) and pos_x <= 950:
        pos_x += speed

    if key_press[pygame.K_s] and not any((bottomLeft, bottomRight)) and pos_y <= 750:
        pos_y += speed

    screen.blit(collision_object, (0, 0))

    for color, x in zip(colors, collision_check.collision_points()):  # remove this to remove the colourful rectangles
        x = (x[0], x[1], x[2] - x[0], x[3] - x[1])
        pygame.draw.rect(screen, color, pygame.Rect(x), width=3)

    player_rect = pygame.Rect(pos_x, pos_y, 50, 50)
    pygame.draw.rect(screen, (0, 0, 0), player_rect)

    pygame.display.update()
