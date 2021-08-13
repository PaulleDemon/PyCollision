import numpy as np
from PIL import Image
from typing import Tuple, List, Generator


class ImageError(Exception):
    pass


def _convertImageToArray(image):
    img = Image.open(image)
    img.load()

    return np.asarray(img)


class Collision:

    def __init__(self, img_path: str, split: Tuple[int, int] = (1, 1), img_pos: Tuple[int, int] = (0, 0),
                 wall_collision=False, wall_padding: Tuple[int, int, int, int] = (1, 1, 1, 1)):
        """

        :param img_path: str
                Pass the image path
        :param split: (int, int)
                pass tuple of rows and columns greater than 0, default (1, 1)
        :param img_pos: (int, int)
                pass the current position of the image default 0, 0
        :param wall_collision: bool
                set this to True if you only want wall collision
        :param wall_padding: (int, int, int, int)
                sometimes optimize might leave some spaces, specify format: (left, top, right, bottom)

        """
        if not all(split):
            raise ValueError("Please enter a split values greater than 0")

        self.img_x, self.img_y = img_pos

        image = _convertImageToArray(img_path)

        if image.shape[2] != 4:
            raise ImageError("Image doesn't have alpha channel")

        self.height, self.width, *_ = image.shape

        self._collision_points = np.array(list(self.divide(image, split)), dtype='object')

        if wall_collision:
            self._wall_collision(wall_padding)

        else:
            self._collision_points = np.concatenate(self._collision_points).ravel()

        self._collision_points = np.reshape(self._collision_points, (-1, 4))

        if self._collision_points.shape[0] > 1 and self._collision_points.dtype != "object":
            self._collision_points = np.unique(self._collision_points, axis=0)

    def setSpritePos(self, posx: int, posy: int):
        """ sets image pos useful when the image or the object is moving"""
        self.img_x, self.img_y = posx, posy

    def _wall_collision(self, padding: Tuple[int, int, int, int] = (1, 1, 1, 1)):
        """ removes inner points of the rectangle by checking the points above and below """
        left, top, right, bottom = padding

        temp = np.concatenate(self._collision_points[:top]).ravel()

        for index in range(1, len(self._collision_points) - bottom):
            pre_point = self._collision_points[index - 1]
            cur_point = self._collision_points[index]
            post_point = self._collision_points[index + 1]

            point_temp = []
            for x in cur_point[left: -right]:
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

            point = np.concatenate((cur_point[:left].ravel(), *point_temp, cur_point[-right:].ravel()))

            temp = np.concatenate((temp, point))

        temp = np.concatenate((temp, self._collision_points[-bottom:][0].ravel()))
        self._collision_points = temp

    def divide(self, img_array, split: Tuple[int, int] = (1, 1)):

        """ creates rectangular points over non-transparent parts """

        rows = img_array.shape[0] // split[0]
        cols = img_array.shape[1] // split[1]

        previous_height = 0
        for x, r in enumerate(range(0, img_array.shape[0], rows)):
            previous_width = 0
            temp_lst = np.empty(4, dtype="int32") * np.nan

            for y, c in enumerate(range(0, img_array.shape[1], cols)):
                img = img_array[r:r + rows, c:c + cols]

                if np.any(img[:, :, 3]):
                    rect = np.array([previous_width, previous_height, previous_width + img.shape[1],
                                     previous_height + img.shape[0]])

                    temp_lst = np.concatenate((temp_lst, rect))

                previous_width = img.shape[1] * y + img.shape[1]

            previous_height = img.shape[0] * x + img.shape[0]

            if not np.isnan(temp_lst).all():
                temp_lst = np.reshape(temp_lst, (-1, 4))
                yield temp_lst[1:]

    def point_collide(self, pos_x=None, pos_y=None, coll_pos: Tuple[int, int] = None,
                      offset=0) -> Tuple[bool, Tuple[int, int, int, int]]:
        """ returns True if there is any collision"""

        if coll_pos is not None:
            self.setSpritePos(*coll_pos)

        cond = np.where((self._collision_points[:, 0] + self.img_x - offset <= pos_x) &
                        (pos_x <= self._collision_points[:, 2] + self.img_x + offset) &
                        (self._collision_points[:, 1] + self.img_y - offset <= pos_y) &
                        (pos_y <= self._collision_points[:, 3] + self.img_y + offset))

        rect = self._collision_points[cond]

        if np.any(rect):
            return True, rect[0].tolist()

        return False, None

    def smart_check(self, pos: Tuple[int, int], coll_pos: Tuple[int, int] = None, offset=0):
        """ First checks if the object is inside the outer rectangle then calls the check_collision"""

        if coll_pos is not None:
            self.setSpritePos(*coll_pos)

        pos_x, pos_y = pos

        if 0 + self.img_x < pos_x < self.width + self.img_x and 0 + self.img_y < pos_y < self.height + self.img_y:
            return self.point_collide(pos_x, pos_y, offset=offset)

        return False, None

    def rect_collide(self, rect: Tuple[int, int, int, int], coll_pos: Tuple[int, int] = None,
                     offset=0) -> Tuple:

        """ checks collision for rectangles pass a tuple returns True and collision rectangle if collision occurs"""
        if coll_pos is not None:
            self.setSpritePos(*coll_pos)

        rect = list(rect)
        topLeft, bottomRight = rect[:2], rect[2:]
        topRight, bottomLeft = (rect[2], rect[1]), (rect[0], rect[3])

        check, pos = self.smart_check(topLeft, offset=offset)
        check2, pos2 = self.smart_check(topRight, offset=offset)
        check3, pos3 = self.smart_check(bottomRight, offset=offset)
        check4, pos4 = self.smart_check(bottomLeft, offset=offset)

        pos_x, pos_y, pos_x1, pos_y1 = rect

        # checks whether the colliding rectangle
        cond = np.where((self._collision_points[:, 0] + self.img_x - offset >= pos_x) &
                        (self._collision_points[:, 1] + self.img_y - offset >= pos_y) &
                        (self._collision_points[:, 0] + self.img_x + offset <= pos_x1) &
                        (self._collision_points[:, 1] + self.img_y + offset <= pos_y1) |
                        (self._collision_points[:, 2] + self.img_x - offset >= pos_x) &
                        (self._collision_points[:, 3] + self.img_y - offset >= pos_y) &
                        (self._collision_points[:, 2] + self.img_x + offset <= pos_x1) &
                        (self._collision_points[:, 3] + self.img_y + offset <= pos_y1))

        rect = self._collision_points[cond]
        pos5 = None

        if np.any(rect):
            pos5 = rect[0].tolist()

        if any((check, check2, check3, check4)) or np.any(rect):
            return True, pos or pos2 or pos3 or pos4 or pos5

        return False, None

    def collision_points(self) -> np.ndarray:
        """ returns the collision points"""
        return self._collision_points


class GroupCollision:

    def __init__(self):
        self._group = list()

    def addItem(self, colobj: Collision):
        """ add single collision item """
        self._group.append(colobj)

    def addItems(self, colobjs: List):
        """ add multiple collision items at once"""
        self._group.extend(colobjs)

    def removeItem(self, colobj: Collision):
        """ remove single item"""
        self._group.remove(colobj)

    def check_collision(self) -> List:
        return list(list_collision(self._group))


def list_collision(coll_objs: List) -> Generator[Collision, Collision, List]:
    """ useful when checking if two complex shapes collide
     returns generator containing the collision-objects and the collision rectangle"""

    for obj_ind in range(0, len(coll_objs) - 1):
        for check_ind in range(obj_ind + 1, len(coll_objs)):
            x, y = coll_objs[check_ind].img_x, coll_objs[check_ind].img_y
            for rect in coll_objs[check_ind].collision_points():
                check, rect_points = coll_objs[obj_ind].rect_collide(rect + [x, y, x, y])

                if check:
                    yield coll_objs[obj_ind], coll_objs[check_ind], rect_points
                    break
