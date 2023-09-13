import random
from PIL import ImageColor


class Primitive:
    def __init__(self, area=None, palette=None):
        self.area = area
        self.x = 0
        self.y = 0
        self.shape = None
        self.palette = palette

    def get_primitive(self):
        return self.shape

    def get_fill(self):
        return (item / 255 for item in ImageColor.getcolor(random.choice(self.palette), "RGB"))

    def touches_border(self, border):
        return not self.shape.intersection(border).is_empty

    def overlaps(self, strtree):
        # with CodeTimer("overlaps with strtree"):
        rv = strtree.query(self.shape, predicate="intersects")
        return len(rv)