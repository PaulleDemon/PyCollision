### Quickstart example

Here is a quick example to get started
```py
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
read the rest of the [examples](https://github.com/PaulleDemon/PyCollision/tree/main/Examples)

### Collision class
This class is used to load images and detect collisions.

| Methods              | Parameters(type)                                                                                                               | Function                                                                                                                                                                                                                                                                                                                                                                                                          |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                                                                                                                               |
| init                 | img_path(str), split(tuple[int, int]), img_pos(tuple[int, int]),  wall_collision(bool), wall_padding(Tuple(int, int, int, int))  | The image specified must have a alpha channel else `ImageError` will be raised. `split` specifies how many rows and columns you would like to split the image into. `img_pos` specifies the current position(x, y) of the sprite. `wall_collision` makes sure only outer wall of the image is stored. Sometimes optimize doesn't do a good job specifying `wall_padding` will correct it. (left, top, right, bottom)|
| setSpritePos         | img_x(int), img_y(int)                                                                                                         | sets the image position. You must use this method if the sprite is  moving                                                                                                                                                                                                                                                                                                                                        |
| point_collide        | pos_x, pos_y, coll_pos(  tuple[int, int]), offset(int)                                                                         | Checks collision given pos_x, pos_y. Specify coll_pos if the sprite is moving,  this will internally call setImagePos. Offset specifies how much distance from the  collision rectangle before alerting collision.                                                                                                                                                                                                |
| smart_check          | pos(tuple[int, int]) , coll_pos(Tuple[int, int])  ,offset(int)                                                                 | Checks first the object is inside the bounding rectangle before calling the `point_collide` method, this can improve efficiency. All the parameters are same as  mentioned above.                                                                                                                                                                                                                                 |
| rect_collide         | rect(tuple[int, int, int, int]) , coll_pos(Tuple[int, int]) ,offset(int)                                                       | Use this if you want to check collision with a rectangular sprite, all the other parameters remains the same as above.                                                                                                                                                                                                                                                                                            |
| collision_points     | -                                                                                                                              | returns collision rectangles                                                                                                                                                                                                                                                                                                                                                                                      |

### GroupCollision class
Add and remove Collision class object to detect collision between them.

| Methods         | Parameters(type)         | Function                                                                                                                             |
|-----------------|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| addItem         | colobj(Collision)        | adds item to the group                                                                                                               |
| addItems        | colobjs(List[Collision]) | adds multiple items to the group                                                                                                     |
| removeItem      | colobj(Collision)        | removes the item from the group.                                                                                                     |
| check_collision | -                        | checks if there is any collision in the group. If there is returns it as List. (note: this simply calls the list_collision function) |

### list_collision function
Pass a list and yields objects that collide.

**parameter:** takes list of Collision objects.

**return:** Generator of collision objects and position.

### ImageError
 This error is raised when image does't contain alpha channel

**Full collision**

![Full collision](https://github.com/PaulleDemon/PyCollision/blob/main/DocumentationImages/FullCollisionImage.png?raw=True)

**wall collision**

![Wall Collision](https://github.com/PaulleDemon/PyCollision/blob/main/DocumentationImages/WallCollisionImage.png?raw=True)

**smart collision**

First checks if point is inside the outermost red rectangle, then check the inner rectangles 

![smart collision](https://github.com/PaulleDemon/PyCollision/blob/main/DocumentationImages/SmartCollision.png?raw=True)
