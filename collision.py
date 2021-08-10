import pygame
import numpy as np
from PIL import Image
from typing import Tuple
import random


class Collision:

    def __init__(self, img_path: str,  split: Tuple[int, int] = (1, 1), optimize=False) -> None:
        
        if not all(split):
            raise ("Please enter a split values greater than 0")
  
        _optimize = optimize
        self.image = self._convertImageToArray(img_path)

        self.collision_points = np.array(list(self.divide(split)))

        if _optimize:
            self._optimize()
        
        else:
            self.collision_points = np.concatenate(self.collision_points).ravel()

        self.collision_points = np.reshape(self.collision_points, (-1, 4))


    def _optimize(self):
        """ removes inner points of the rectangle by checking the points above and below """

        temp = self.collision_points[:1][0].ravel()
        
        for index in range(1, len(self.collision_points)-1):
            pre_point = self.collision_points[index-1]
            cur_point = self.collision_points[index]
            post_point = self.collision_points[index + 1]

            point_temp = []
            for x in cur_point[1: -1]:
                pre_exists = False
                post_exists = False

                for y in pre_point:
                    if x[0] == y[0] and x[2] == y[2]:
                        pre_exists = True
                        break
                
                for z in post_point:
                    if x[0] == z[0] and x[2] == z[2]:
                        post_exists = True
                        break

                if not pre_exists or not post_exists:
                    point_temp.append(x)
                        

            point = np.array(point_temp)
            point = np.concatenate((cur_point[0], *point_temp, cur_point[-1]))

            temp = np.concatenate((temp, point))

        temp = np.concatenate((temp, self.collision_points[-1:][0].ravel()))
        self.collision_points = temp

        
    def _convertImageToArray(self, image):
        img = Image.open(image)
        img.load()

        return np.asarray(img)

    def divide(self, split: Tuple[int, int] = (1, 1)):

        """ creates rectanglular points over non-transparent parts """

        rows = self.image.shape[0] // split[0]
        cols = self.image.shape[1] // split[1]
        
        previous_height = 0
        for x, r in enumerate(range(0, self.image.shape[0], rows)):
            previous_width = 0
            temp_lst = np.empty(4, dtype="int32") * np.nan
            
            for y, c in enumerate(range(0, self.image.shape[1], cols)):
                img = self.image[r:r+rows, c:c+cols]

                if np.any(img[:, :, 3]): 
                    rect = np.array([previous_width, previous_height, previous_width + img.shape[1], previous_height + img.shape[0]])

                    temp_lst = np.concatenate((temp_lst, rect))    
                
                previous_width = img.shape[1]*y + img.shape[1]
            
            previous_height = img.shape[0]*x + img.shape[0]
    
            if not np.isnan(temp_lst).all():
                temp_lst = np.reshape(temp_lst, (-1, 4))
                yield temp_lst[1:]

    def check_collision(self, pos_x = None, pos_y = None, offset=0) -> bool:
        """ returns True if there is any collision"""

        pos_x_in, pos_y_in = False, False
        for x in self.collision_points:  

            pos_x_in, pos_y_in = False, False
            
            if pos_x and x[0]-offset <= pos_x <= x[2]+offset:
                pos_x_in = True
            
            if pos_y and x[1]-offset < pos_y < x[3]+offset:
                pos_y_in = True

            if pos_x and pos_y is None:
                return pos_x_in, None
            
            elif pos_y and pos_x is None:
                return pos_y_in, None

            elif pos_x and pos_y and all((pos_x_in, pos_y_in)):
                return pos_x_in, pos_y_in

        return False, False

    def smart_check(self,  pos_x = None, pos_y = None, offset=0):
        pass

pygame.init()

screen = pygame.display.set_mode((1000, 800))

player = pygame.image.load(r"assets\playerTank.png").convert() #_alpha()
player_rect = player.get_rect()

collision_check = Collision(r"assets\sample.png", (50, 50), optimize=True)
collision_object = pygame.image.load(r"assets\sample.png").convert_alpha()

colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in range(len            (collision_check.collision_points))]

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
    # colliding =  collision_check.check_collision(pos_x, pos_y, offset=offset)

    topLeft = all(collision_check.check_collision(pos_x, pos_y, offset=offset))
    topRight = all(collision_check.check_collision(pos_x+player_rect.width, pos_y, offset=offset))
    bottomRight = all(collision_check.check_collision(pos_x+player_rect.width, pos_y+player_rect.height, offset=offset))
    bottomLeft = all(collision_check.check_collision(pos_x, pos_y+player_rect.height, offset=offset))

    # print("ToP LEft: ", topLeft)
    print("ToP LEft: ", any([topLeft, bottomLeft]))
    print("top Right: ", topRight)
    print("Bottom Right: ", bottomRight)
    print("Bottom left: ", bottomLeft)


    if key_press[pygame.K_a] and not any([topLeft, bottomLeft]):#all([x, y]):
        pos_x -= speed

    if key_press[pygame.K_w] and not any([topLeft, topRight]): #all([x, y]):
        pos_y -= speed
    
    if key_press[pygame.K_d] and not any([topRight, bottomRight]): #all([x1, y1]):
        pos_x += speed
    
    if key_press[pygame.K_s] and not any([bottomRight, bottomLeft]): #all([x1, y1]): 
        pos_y += speed
    
    screen.blit(collision_object, (0, 0))

    for color, x in zip(colors, collision_check.collision_points):
        x = (x[0], x[1], x[2]-x[0], x[3]-x[1])
        pygame.draw.rect(screen, color, pygame.Rect(x), width=3)


    screen.blit(player, (pos_x, pos_y))

    pygame.display.update()
