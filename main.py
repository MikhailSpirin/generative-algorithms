import math
import random
import logging
from shapely.geometry import Point, LineString
from PIL import Image, ImageDraw

c = 1.3
N = 3000
R0 = 400
XMAX = 2000
YMAX = 1500


def get_random_color_from_palette():
    return random.choice(["#c9cca1",
                          "#caa05a",
                          "#ae6a47",
                          "#8b4049",
                          "#543344",
                          "#515262",
                          "#63787d",
                          "#8ea091"])


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
    return random.random() * x_max, random.random() * y_max


def overlaps(trial, objs, border, placed):
    if not trial.intersection(border).is_empty:
        return True
    if not placed.intersection(trial).is_empty:
        return True


    # for item in objs.values():
    #     if math.sqrt((x - item['x']) ** 2 + (y - item['y']) ** 2) <= r + item['radius']:
    #         return True
    return False


def draw_object(draw, x, y, r):
    draw.ellipse((x - r, y - r, x + r, y + r), fill=get_random_color_from_palette(), outline=None, width=1)


def init_canvas():
    im = Image.new('RGB', (XMAX, YMAX), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    return im, draw


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    MAX_TRIES = 100
    placed_objects = {}
    objects_to_place = get_all_shapes_params(c, N, R0)
    image, draw = init_canvas()

    tries_logger = []
    border = LineString([[0, 0], [XMAX, 0], [XMAX, YMAX], [0, YMAX], [0, 1]])
    placed_objects_union = Point(0, 0)
    for i in range(1, N + 1):
        tries = 0
        while tries < MAX_TRIES:
            x, y = get_placement_coords(XMAX, YMAX)
            trial = Point(x, y).buffer(objects_to_place[i]['radius'])
            if not overlaps(trial, placed_objects, border, placed_objects_union):
                draw_object(draw, x, y, objects_to_place[i]['radius'])
                placed_objects[i] = objects_to_place[i]
                placed_objects[i]['x'] = x
                placed_objects[i]['y'] = y
                placed_objects_union = placed_objects_union.union(trial)
                break
            tries += 1
        logger.info(f"placed {i}. Previous tries {tries}")
    image.show()
