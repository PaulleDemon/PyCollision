from numpy.lib import tracemalloc_domain
import pygame
import numpy as np
from PIL import Image
from typing import Tuple, Union, List
from itertools import zip_longest

import random


class Collision:

    def __init__(self, img_path: str, pos: list, split: list = (1, 1), optimize=False) -> None:
        
        if not all(split):
            raise ("Please enter a split values greater than 0")
        optimize = optimize
        self._pos = pos
        self._temp_pos = pos
        self._split = list(split)
        self.image = self._convertToArray(img_path)

        self.collision_points = np.array(list(self.divide(split)))
        temp = self.collision_points[:1][0].flatten()
        print("Collision points: \n", self.collision_points)
        # print("DIM: ", temp.shape, temp, type(temp[0]))
        if optimize:
            for index in range(1, len(self.collision_points)-1):
                cur_point = self.collision_points[index][2: -2]
                pre_point = self.collision_points[index-1]

                first, last = self.collision_points[index][:2],  self.collision_points[index][-2:]
                print("Cur: \n", cur_point, "\nPre: \n", pre_point, index)
                point_temp = []
                
                for x in cur_point:
                    print("X: ", x)
                    exists = False
                    for y in pre_point:
                        print("y: ", y)
                        print("Not EQUALS: ", x[0] != y[0], x[2] != y[2])
                        if x[0] == y[0] and x[2] == y[2]:
                            exists = True
                            break

                    if not exists:
                        point_temp.append(x)
                            # break
                            
        
                    print("\n---BREAK---\n")
                print("TEMP POINTS : ", point_temp, last.tolist(), first.tolist())
                point = np.array(point_temp)
                # print("POint: ", cur_point[0], cur_point[-1])
                point = np.concatenate((*first, *point_temp, *last))
                temp = np.concatenate((temp, point))
                print("Tep: \n", temp)
   
            temp = np.concatenate((temp, self.collision_points[-1:][0].ravel(), self.collision_points[-2:][0].ravel()))

            self.collision_points = temp

        else:
            self.collision_points = np.concatenate(self.collision_points).ravel()

        self.collision_points = np.reshape(self.collision_points, (-1, 4))
        # print("Final:", self.collision_points, self.collision_points.ndim)

    def _convertToArray(self, image):
        img = Image.open(image)
        img.load()

        return np.asarray(img)

    def divide(self, split: Tuple[int, int] = (1, 1)):

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




pygame.init()

# collision_check = Collision(r"assets\sample.png", [0, 0], [15, 15], optimize=False)
# collision_check = Collision(r"assets\sample.png", [0, 0], [15, 15], optimize=False)
collision_check = Collision(r"assets\sample.png", [0, 0], [15, 15], optimize=True)
screen = pygame.display.set_mode((1000, 800))

player = pygame.image.load(r"assets\playerTank.png").convert() #_alpha()

collision_object = pygame.image.load(r"assets\sample.png").convert_alpha()

colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in range(len            (collision_check.collision_points))]

running = True
speed = 2
pos_x, pos_y = (10, 10)

while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
    
    key_press = pygame.key.get_pressed()
    # colliding =  collision_check.check_collision([pos_x, pos_y])
    # print(colliding)

    if key_press[pygame.K_a]:
        pos_x -= speed

    if key_press[pygame.K_w]:
        pos_y -= speed
    
    if key_press[pygame.K_d]:
        pos_x += speed
    
    if key_press[pygame.K_s]:
        pos_y += speed
    
    screen.blit(collision_object, (0, 0))

    for color, x in zip(colors, collision_check.collision_points):
        x = (x[0], x[1], x[2]-x[0], x[3]-x[1])
        pygame.draw.rect(screen, color, pygame.Rect(x), width=3)


    screen.blit(player, (pos_x, pos_y))

    pygame.display.update()
