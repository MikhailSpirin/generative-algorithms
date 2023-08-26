import math
import random
import logging
from shapely.geometry import Point, LineString
from shapely import affinity
from PIL import Image, ImageDraw
from palettes import PALETTES

c = 1.3
N = 1000
R0 = 300
XMAX = 2000
YMAX = 1500
MAX_TRIES = 100


def get_all_shapes_params(c, N, R0):
    rv = {}
    A0 = R0 * R0 * math.pi
    for i in range(1, N + 1):
        o = {}
        o['gi'] = 1 / i ** c
        o['area'] = A0 * o['gi']
        o['radius'] = math.sqrt(o['area'] / math.pi)
        rv[i] = o
    return rv


def get_placement_coords(x_max, y_max):
    return random.random() * x_max, random.random() * y_max // 100 * 100


def overlaps(trial, border, placed):
    if not trial.intersection(border).is_empty or not trial.intersection(placed).is_empty:
        return True
    return False


def draw_object(draw, x, y, r, palette):
    draw.ellipse((x - r, y - r, x + r, y + r), fill=random.choice(palette), outline=None, width=1)


def init_canvas():
    im = Image.new('RGB', (XMAX, YMAX), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    return im, draw


def create_border():
    return LineString([[0, 0], [XMAX, 0], [XMAX, YMAX], [0, YMAX], [0, 1]])


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    objects_to_place = get_all_shapes_params(c, N, R0)
    image, draw = init_canvas()
    current_palette = random.choice(list(PALETTES.values()))
    border = create_border()
    tries_logger = []
    placed_objects_union = Point(0, 0)
    for i in range(1, N + 1):
        tries = 0
        while tries < MAX_TRIES:
            x, y = get_placement_coords(XMAX, YMAX)
            radius = objects_to_place[i]['radius']
            trial = Point(x, y).buffer(radius)
            if not overlaps(trial, border, placed_objects_union):
                draw_object(draw, x, y, radius, current_palette)
                placed_objects_union = placed_objects_union.union(trial)
                break
            tries += 1
        logger.info(f"placed {i}. Previous tries {tries}")
    image.show()
