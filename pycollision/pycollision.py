import numpy as np
from PIL import Image
from typing import Tuple, List


def _convertImageToArray(image):
    img = Image.open(image)
    img.load()

    return np.asarray(img)


class Collision:

    def __init__(self, img_path: str, split: Tuple[int, int] = (1, 1), img_pos: Tuple[int, int] = (0, 0),
                 optimize=False):

        if not all(split):
            raise ValueError("Please enter a split values greater than 0")

        self.img_x, self.img_y = img_pos

        _optimize = optimize
        self.image = _convertImageToArray(img_path)
        self.height, self.width, *_ = self.image.shape

        self._collision_points = np.array(list(self.divide(split)), dtype='object')

        if _optimize:
            self._optimize()

        else:
            self._collision_points = np.concatenate(self._collision_points).ravel()

        self._collision_points = np.reshape(self._collision_points, (-1, 4))

    def setImgPos(self, posx: int, posy: int):
        """ sets image pos useful when the image or the object is moving"""
        self.img_x, self.img_y = posx, posy

    def _optimize(self):
        """ removes inner points of the rectangle by checking the points above and below """

        temp = self._collision_points[:1][0].ravel()

        for index in range(1, len(self._collision_points) - 1):
            pre_point = self._collision_points[index - 1]
            cur_point = self._collision_points[index]
            post_point = self._collision_points[index + 1]

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

            # point = np.array(point_temp)
            point = np.concatenate((cur_point[0], *point_temp, cur_point[-1]))

            temp = np.concatenate((temp, point))

        temp = np.concatenate((temp, self._collision_points[-1:][0].ravel()))
        self._collision_points = temp

    def divide(self, split: Tuple[int, int] = (1, 1)):

        """ creates rectangular points over non-transparent parts """

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

    def check_collision(self, pos_x=None, pos_y=None, coll_pos: Tuple[int, int] = None,
                        offset=0) -> Tuple[bool, Tuple[int, int, int, int]]:
        """ returns True if there is any collision"""

        if coll_pos is not None:
            self.setImgPos(*coll_pos)

        cond = np.where((self._collision_points[:, 0] + self.img_x - offset <= pos_x) &
                        (pos_x <= self._collision_points[:, 2] + self.img_x + offset) &
                        (self._collision_points[:, 1] + self.img_y - offset <= pos_y) &
                        (pos_y <= self._collision_points[:, 3] + self.img_y + offset))

        rect = self._collision_points[cond]

        if cond and cond[0].size != 0:
            return True, rect

        return False, None

    def smart_check(self, pos: Tuple[int, int], coll_pos: Tuple[int, int] = None, offset=0):
        """ First checks if the object is inside the outer rectangle then calls the check_collision"""

        if coll_pos is not None:
            self.setImgPos(*coll_pos)

        pos_x, pos_y = pos

        if 0 + self.img_x < pos_x < self.width + self.img_x and 0 + self.img_y < pos_y < self.height + self.img_y:
            return self.check_collision(pos_x, pos_y, offset=offset)

        return False, None

    def check_rect_inside(self, rect: Tuple[int, int, int, int], coll_pos: Tuple[int, int] = None, offset=0) -> Tuple:

        if coll_pos is not None:
            self.setImgPos(*coll_pos)

        check1, pos1 = self.smart_check(rect[:2], offset=offset)
        check2, pos2 = self.smart_check(rect[2:], offset=offset)

        return check1 or check2, (pos1, pos2)

    def check_rect_collision(self, rect: Tuple[int, int, int, int], coll_pos: Tuple[int, int] = None,
                             offset=0) -> Tuple:

        if coll_pos is not None:
            self.setImgPos(*coll_pos)

        rect = list(rect)
        topLeft, bottomRight = rect[:2], rect[2:]
        topRight, bottomLeft = (rect[2], rect[1]), (rect[0], rect[3])

        check, pos = self.smart_check(topLeft, offset=offset)
        check2, pos2 = self.smart_check(topRight, offset=offset)
        check3, pos3 = self.smart_check(bottomRight, offset=offset)
        check4, pos4 = self.smart_check(bottomLeft, offset=offset)

        pos_x, pos_y, pos_x1, pos_y1 = rect

        cond = np.argmax((self._collision_points[:, 0] + self.img_x - offset >= pos_x) &
                         (self._collision_points[:, 1] + self.img_y - offset >= pos_y) &
                         (self._collision_points[:, 0] + self.img_x + offset <= pos_x1) &
                         (self._collision_points[:, 1] + self.img_y + offset <= pos_y1))

        cond2 = np.argmax((self._collision_points[:, 2] + self.img_x - offset >= pos_x) &
                          (self._collision_points[:, 3] + self.img_y - offset >= pos_y) &
                          (self._collision_points[:, 2] + self.img_x + offset <= pos_x1) &
                          (self._collision_points[:, 3] + self.img_y + offset <= pos_y1))

        # print((check, check2, check3, check4), cond, cond2)

        if any((check, check2, check3, check4)) or np.any(cond) or np.any(cond2):
            return True, None  # pos or pos2 or pos3 or pos4

        return False, None

    def collision_points(self) -> np.ndarray:
        """ returns the collision points"""
        return self._collision_points


class GroupCollision:

    def __init__(self):
        self._group = list()

    def add(self, colobj: Collision):
        self._group.append(colobj)

    def remove(self, colobj: Collision):
        self._group.remove(colobj)

    def check(self) -> List[Tuple]:
        coll_objs = list()

        for obj_ind in range(0, len(self._group)):
            for check_ind in range(obj_ind, len(self._group)):
                for rect in self._group[check_ind].collision_points():
                    check, pos, check2, pos2 = self._group[obj_ind].check_rect(rect)

                    if any((check, check2)):
                        coll_points = (pos, pos2)
                        coll_objs.append((self._group[obj_ind], self._group[check_ind], coll_points))

        return coll_objs
