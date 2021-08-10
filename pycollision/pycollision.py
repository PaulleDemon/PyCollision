import numpy as np
from PIL import Image
from typing import Tuple


def _convertImageToArray(image):
    img = Image.open(image)
    img.load()

    return np.asarray(img)


class Collision:

    def __init__(self, img_path: str, split: Tuple[int, int] = (1, 1), optimize=False) -> None:

        if not all(split):
            raise ValueError("Please enter a split values greater than 0")

        _optimize = optimize
        self.image = _convertImageToArray(img_path)
        self.height, self.width, *_ = self.image.shape

        self.collision_points = np.array(list(self.divide(split)))

        if _optimize:
            self._optimize()

        else:
            self.collision_points = np.concatenate(self.collision_points).ravel()

        self.collision_points = np.reshape(self.collision_points, (-1, 4))

    def _optimize(self):
        """ removes inner points of the rectangle by checking the points above and below """

        temp = self.collision_points[:1][0].ravel()

        for index in range(1, len(self.collision_points) - 1):
            pre_point = self.collision_points[index - 1]
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

    def divide(self, split: Tuple[int, int] = (1, 1)):

        """ creates rectanglular points over non-transparent parts """

        rows = self.image.shape[0] // split[0]
        cols = self.image.shape[1] // split[1]

        previous_height = 0
        for x, r in enumerate(range(0, self.image.shape[0], rows)):
            previous_width = 0
            temp_lst = np.empty(4, dtype="int32") * np.nan

            for y, c in enumerate(range(0, self.image.shape[1], cols)):
                img = self.image[r:r + rows, c:c + cols]

                if np.any(img[:, :, 3]):
                    rect = np.array([previous_width, previous_height, previous_width + img.shape[1],
                                     previous_height + img.shape[0]])

                    temp_lst = np.concatenate((temp_lst, rect))

                previous_width = img.shape[1] * y + img.shape[1]

            previous_height = img.shape[0] * x + img.shape[0]

            if not np.isnan(temp_lst).all():
                temp_lst = np.reshape(temp_lst, (-1, 4))
                yield temp_lst[1:]

    def check_collision(self, pos_x=None, pos_y=None, offset=0) -> Tuple[bool, Tuple[int, int, int, int]]:
        """ returns True if there is any collision"""

        if not any((pos_x, pos_y)):
            raise ValueError("Must specify at least one position")

        for x in self.collision_points:

            pos_x_in, pos_y_in = False, False

            if pos_x and x[0] - offset <= pos_x <= x[2] + offset:
                pos_x_in = True

            if pos_y and x[1] - offset < pos_y < x[3] + offset:
                pos_y_in = True

            if pos_x and pos_y is None:
                return pos_x_in, x

            elif pos_y and pos_x is None:
                return pos_y_in, x

            elif pos_x and pos_y and all((pos_x_in, pos_y_in)):
                return True, x

        return False, None

    def smart_check(self, pos: Tuple[int, int], offset=0):
        """ First checks if the object is inside the outer rectangle then calls the checkcollision"""

        pos_x, pos_y = pos

        if 0 < pos_x < self.width and 0 < pos_y < self.height:
            return self.check_collision(pos_x, pos_y, offset=offset)

        return False, None
