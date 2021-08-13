import pygame
import random
from pycollision import Collision, list_collision

# use W, A, S, D to move player 1 and arrow keys to move player1

pygame.init()

screen = pygame.display.set_mode((1000, 800))

player = pygame.image.load(r"TestImages/playerTank.png").convert_alpha()
player_rect = player.get_rect()

player2 = pygame.image.load(r"TestImages/playerTank.png").convert_alpha()
player_rect2 = player.get_rect()

player1_col = Collision(r"TestImages/playerTank.png", (5, 5))
player2_col = Collision(r"TestImages/playerTank.png", (10, 10), wall_collision=True)

colors1 = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in
           range(len(player1_col.collision_points()))]

colors2 = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in
           range(len(player2_col.collision_points()))]

running = True
speed = 0.3
pos_x, pos_y = (10, 10)

ply2X, ply2Y = (0, 0)

offset = 0

coll_font = pygame.font.SysFont('Consolas', 50)

while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    player1_col.setSpritePos(pos_x, pos_y)  # important
    player2_col.setSpritePos(ply2X, ply2Y)  # important

    # print(list_collision([player1_col, player2_col]))
    if list(list_collision([player1_col, player2_col])):
        screen.fill((255, 16, 8))
        screen.blit(coll_font.render("Collision", True, (255, 255, 255)), (50, 50))

    key_press = pygame.key.get_pressed()

    if key_press[pygame.K_a] and pos_x >= 0:
        pos_x -= speed

    if key_press[pygame.K_w] and pos_y >= 0:
        pos_y -= speed

    if key_press[pygame.K_d] and pos_x <= 950:
        pos_x += speed

    if key_press[pygame.K_s] and pos_y <= 750:
        pos_y += speed

    if key_press[pygame.K_LEFT] and ply2X >= 0:
        ply2X -= speed

    if key_press[pygame.K_UP] and ply2Y >= 0:
        ply2Y -= speed

    if key_press[pygame.K_RIGHT] and ply2X <= 950:
        ply2X += speed

    if key_press[pygame.K_DOWN] and ply2Y <= 750:
        ply2Y += speed

    screen.blit(player, (pos_x, pos_y))
    screen.blit(player2, (ply2X, ply2Y))

    for color, x in zip(colors1, player1_col.collision_points()):
        x = (x[0]+pos_x, x[1]+pos_y, x[2] - x[0], x[3] - x[1])
        pygame.draw.rect(screen, color, pygame.Rect(x), width=3)

    for color, x in zip(colors2, player2_col.collision_points()):
        x = (x[0]+ply2X, x[1]+ply2Y, x[2] - x[0], x[3] - x[1])
        pygame.draw.rect(screen, color, pygame.Rect(x), width=3)

    pygame.display.update()
