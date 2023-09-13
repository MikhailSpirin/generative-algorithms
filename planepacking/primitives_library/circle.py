from math import sqrt, pi
from crossproject.codetimer import CodeTimer
from shapely.geometry import Point, LinearRing, Polygon
from .primitive import Primitive


class Circle(Primitive):
    def __init__(self, area=None, palette=None):
        self.x = 0
        self.y = 0
        self.radius = 0
        self.shape = None
        self.area = area
        self.palette = palette

    def define_object(self, x, y):
        self.x = x
        self.y = y
        self.radius = sqrt(self.area / pi)
        self.shape = Point(self.x, self.y).buffer(self.radius+1)
        return self.shape

    def draw_object(self, ctx):
        fill = self.get_fill()
        ctx.save()
        ctx.translate(self.x, self.y)
        ctx.arc(0, 0, self.radius, 0, 2 * pi)
        ctx.set_source_rgb(*fill)
        ctx.fill()
        ctx.restore()
