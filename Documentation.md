#Documentation

### Collision class:
This class is used to load images and detect collisions.

| Methods              | Parameters(type)                                                                                                               | Function                                                                                                                                                                                                                                                                                                                                                                                                          |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                                                                                                                               |
| init                 | img_path(str), split(tuple[int, int]), img_pos(tuple[int, int]),  optimize(bool), optimize_padding(Tuple(int, int, int, int))  | The image specified must have a alpha channel else `ImageError` will be raised. `split` specifies how many rows and columns you would like to split the image into. `img_pos` specifies the current position(x, y) of the sprite. `optimize` makes sure only outer wall of the image is stored. Sometimes optimize doesn't do a good job specifying `optimize_padding` will correct it. (left, top, right, bottom)|
| setImagePos          | img_x(int), img_y(int)                                                                                                         | sets the image position. You must use this method if the sprite is  moving                                                                                                                                                                                                                                                                                                                                        |
| check_collision      | pos_x, pos_y, coll_pos(  tuple[int, int]), offset(int)                                                                         | Checks collision given pos_x, pos_y. Specify coll_pos if the sprite is moving,  this will internally call setImagePos. Offset specifies how much distance from the  collision rectangle before alerting collision.                                                                                                                                                                                                |
| smart_check          | pos(tuple[int, int]) , coll_pos(Tuple[int, int])  ,offset(int)                                                                 | Checks first the object is inside the bounding rectangle before calling the  check_collision method, this can improve efficiency. All the parameters are same as  mentioned above.                                                                                                                                                                                                                                |
| check_rect_collision | rect(tuple[int, int, int, int]) , coll_pos(Tuple[int, int]) ,offset(int)                                                       | Use this if you want to check collision with a rectangular sprite, all the other parameters remains the same as above.                                                                                                                                                                                                                                                                                            |
| collision_points     | -                                                                                                                              | returns collision rectangles                                                                                                                                                                                                                                                                                                                                                                                      |

### GroupCollision class:
Add and remove Collision class object to detect collision between them.

| Methods         | Parameters(type)         | Function                                                                                                                             |
|-----------------|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| addItem         | colobj(Collision)        | adds item to the group                                                                                                               |
| addItems        | colobjs(List[Collision]) | adds multiple items to the group                                                                                                     |
| removeItem      | colobj(Collision)        | removes the item from the group.                                                                                                     |
| check_collision | -                        | checks if there is any collision in the group. If there is returns it as List. (note: this simply calls the list_collision function) |

### list_collision function:
Pass a list and yields objects that collide.

**parameter:** takes list of Collision objects.

**return:** Generator of collision objects and position.

### ImageError:
 This error is raised when image does't contain alpha channel

**Full collision**

![Full collision](https://github.com/PaulleDemon/PyCollision/blob/main/DocumentationImages/FullCollisionImage.png?raw=True)

**wall collision**

![Wall Collision](https://github.com/PaulleDemon/PyCollision/blob/main/DocumentationImages/WallCollisionImage.png?raw=True)

**smart collision**

![smart collision](https://github.com/PaulleDemon/PyCollision/blob/main/DocumentationImages/SmartCollision.png?raw=True)
