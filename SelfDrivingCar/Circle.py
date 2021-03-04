import math


class Circle:

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def is_point_inside(self, x, y):
        dx = math.pow((x-self.x), 2)
        dy = math.pow((y-self.y), 2)
        return (dx+dy) < math.pow(self.radius, 2)

    def is_circle_touch(self, center_x, center_y, radius):
        dx = math.pow((center_x-self.x), 2)
        dy = math.pow((center_y-self.y), 2)
        return (dx+dy) < math.pow((self.radius+radius), 2)

    def get_angle(self, x, y):
        dy = y - self.y
        dx = x - self.x
        return math.degrees(math.atan2(dy, dx))

    def get_direction(self, x, y, v):
        rad = math.radians(self.get_angle(x, y))
        px = math.sin(rad) * v
        py = math.cos(rad) * v
        print(tuple([int(px), int(py)]))
        return tuple([int(px), int(py)])