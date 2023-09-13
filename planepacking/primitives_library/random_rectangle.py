from math import pi
from crossproject.codetimer import CodeTimer
from shapely.geometry import Point, LinearRing, Polygon
import random
from .primitive import Primitive


class RandomRectangle(Primitive):
    def __init__(self, area=None, palette=None):
        self.area = area
        self.palette = palette
        self.x = 0
        self.y = 0
        self.shape = None
        self.a = random.uniform(0, self.area/4)
        self.b = self.area / self.a

    def define_object(self, x, y):
        self.x = x
        self.y = y
        self.shape = Polygon([[x - self.a / 2, y - self.b / 2],
                              [x - self.a / 2, y + self.b / 2],
                              [x + self.a / 2, y + self.b / 2],
                              [x + self.a / 2, y - self.b / 2]
                              ])
        return self.shape

    def draw_object(self, ctx):
        fill = self.get_fill()
        ctx.save()
        ctx.translate(self.x - self.a / 2, self.y - self.b / 2)
        ctx.rotate(random.uniform(0, 2 * pi))
        ctx.rectangle(0,
                      0,
                      self.a,
                      self.b)
        ctx.set_source_rgb(*fill)
        ctx.fill()
        ctx.restore()
