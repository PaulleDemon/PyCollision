# PyCollision

This is a collision detection program that makes use of rectangles to detect collision.

Quick example using pygame:
```python
import pygame
import random
from pycollision import Collision

pygame.init()

screen = pygame.display.set_mode((1000, 800))

player_rect = pygame.Rect(0, 0, 50, 50)

collision_check = Collision(r"sample.png", (15, 15), wall_collision=False) # set wall collision to True if you want to check the collision only at the walls, this will be much faster
collision_object = pygame.image.load(r"sample.png").convert_alpha()

colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in
          range(len(collision_check.collision_points()))]

running = True
speed = 1.5
pos_x, pos_y = (10, 10)

coll_font = pygame.font.SysFont('Consolas', 50)

while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    pos_x, pos_y = pygame.mouse.get_pos()

    colliding, pos = collision_check.smart_check((pos_x, pos_y)) # checks if the point is first inside the outer rectangle then checks if it is inside the image
    # rect = (player_rect.x, player_rect.y, player_rect.x+player_rect.width, player_rect.height+player_rect.y)
    # colliding, pos = collision_check.rect_collide(rect)
    if colliding:
        screen.fill((255, 16, 8))
        screen.blit(coll_font.render("Collision", True, (255, 255, 255)), (50, 50))

    screen.blit(collision_object, (0, 0))

    # for color, x in zip(colors, collision_check.collision_points()):  # uncomment this to get colourful rectangles
    #     x = (x[0], x[1], x[2] - x[0], x[3] - x[1])
    #     pygame.draw.rect(screen, color, pygame.Rect(x), width=3)

    player_rect = pygame.Rect(pos_x, pos_y, 50, 50)
    pygame.draw.rect(screen, (0, 0, 0), player_rect)

    pygame.display.update()
```
save the below sample image in the same directory as the program and give a test run.

![Sample Image](https://github.com/PaulleDemon/PyCollision/blob/main/Examples/TestImages/sample.png?raw=True)

Check out more examples [here](https://github.com/PaulleDemon/PyCollision/tree/main/Examples).

Refer documentation [here](https://browsedocs.com/LBImCEvuwGje)


If you are using for research purposes, Cite this using the following:
```
P. Sajo, G. R and M. B.N, "Controlling the Accuracy and Efficiency of Collision Detection in 2d Games using Hitboxes," 2023 IEEE International Conference on Contemporary Computing and Communications (InC4), Bangalore, India, 2023, pp. 1-5, doi: 10.1109/InC457730.2023.10263197.
```
