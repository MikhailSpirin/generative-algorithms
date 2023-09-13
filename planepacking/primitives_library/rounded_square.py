from math import sqrt, pi
from crossproject.codetimer import CodeTimer
from shapely.geometry import Point, LinearRing, Polygon
import random
from shapely import affinity
from .primitive import Primitive


class RoundedSquare(Primitive):
    def __init__(self, area=None, palette=None):
        self.area = area
        self.palette = palette
        self.x = 0
        self.y = 0
        self.shape = None
        self.angle = 0
        self.a = sqrt(self.area)
        self.r = self.a / 3

    def define_object(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * pi)
        self.shape = LinearRing([[x - self.a / 2, y - self.a / 2],
                              [x - self.a / 2, y + self.a / 2],
                              [x + self.a / 2, y + self.a / 2],
                              [x + self.a / 2, y - self.a / 2]
                              ]).buffer(1)
        self.shape = affinity.rotate(self.shape, self.angle, origin=(self.x, self.y), use_radians=True)
        return self.shape

    def draw_object(self, ctx):
        fill = self.get_fill()
        ctx.save()
        ctx.translate(self.x, self.y)
        ctx.rotate(self.angle)
        ctx.translate(-self.a / 2, -self.a / 2)
        ctx.move_to(self.r, 0)
        ctx.line_to(self.a - self.r, 0)
        ctx.curve_to(self.a, 0, self.a, 0, self.a, self.r)
        ctx.line_to(self.a, self.a - self.r)  # Move to D
        ctx.curve_to(self.a, self.a, self.a, self.a, self.a - self.r, self.a)  # Curve to E
        ctx.line_to(self.r, self.a)  # Line to F
        ctx.curve_to(0, self.a, 0, self.a, 0, self.a - self.r)  # Curve to G
        ctx.line_to(0, self.r)  # Line to H
        ctx.curve_to(0, 0, 0, 0, self.r, 0)  # Curve to A
        ctx.set_source_rgb(*fill)
        ctx.fill()
        ctx.restore()

