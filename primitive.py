import math
from codetimer import CodeTimer
from shapely.geometry import Point, LinearRing, Polygon
import random

class Primitive:
    def __init__(self, area=None, ):
        self.area = area
        self.x = 0
        self.y = 0
        # self.radius = 0
        self.size = 0
        self.primitive = None

    def get_primitive(self):
        return self.primitive

    def touches_border(self, border):
        return not self.primitive.intersection(border).is_empty

    def overlaps(self, placed):
        with CodeTimer("overlaps"):
            return not self.primitive.intersection(placed).is_empty
    # https://stackoverflow.com/questions/14697442/faster-way-of-polygon-intersection-with-shapely

    def define_object(self, x, y):
        self.x = x
        self.y = y
        self.size = math.sqrt(self.area)
        self.primitive = Polygon([(self.x, self.y),
                                     (self.x + self.size, self.y),
                                     (self.x + self.size, self.y + self.size),
                                     (self.x, self.y + self.size),
                                     (self.x, self.y)]).buffer(2)

        # self.radius = math.sqrt(self.area / math.pi)
        # self.primitive = Point(self.x, self.y).buffer(self.radius)
        return self.primitive

    def draw_object(self, draw, palette):
        # draw.ellipse((self.x - self.radius,
        #               self.y - self.radius,
        #               self.x + self.radius,
        #               self.y + self.radius), fill=random.choice(palette), outline=None, width=1)

        draw.rounded_rectangle((self.x, self.y, self.x + self.size, self.y + self.size), radius=self.size/5, fill=random.choice(palette), outline=None)