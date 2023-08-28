import math
import random
import logging
from shapely.geometry import Point, LineString, LinearRing
from shapely import affinity, union
from PIL import Image, ImageDraw
from palettes import PALETTES
from codetimer import CodeTimer
from primitive import Primitive
import time


c = 1.4
n = 1200
a0 = 100000
XMAX = 1200
YMAX = 800
MAX_TRIES = 20


def init_all_primitives(c, n, a0):
    rv = [Primitive(a0 * 1 / i ** c) for i in range(1, n + 1)]
    # rv = [Primitive(random.choice([a0, a0*4, a0*9, a0*3])) for i in range(1, n + 1)]
    return rv


def get_placement_coords(x_max, y_max):
    return (
        random.random() * x_max // 10 * 10,
        random.random() * y_max // 10 * 10
    )


def init_graph():
    im = Image.new('RGB', (XMAX, YMAX), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    palette = random.choice(list(PALETTES.values()))
    return im, draw, palette


def create_border():
    return LinearRing([[0, 0], [XMAX, 0], [XMAX, YMAX], [0, YMAX], [0, 0]])


if __name__ == '__main__':
    start_time = time.time()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    primitives = init_all_primitives(c, n, a0)
    image, draw, palette = init_graph()
    border = create_border()

    placed_objects = Point(0, 0)

    tries_logger = []
    for idx, item in enumerate(primitives):
        tries = 0
        while tries < MAX_TRIES:
            tries += 1
            x, y = get_placement_coords(XMAX, YMAX)
            item.define_object(x, y)

            if not item.overlaps(placed_objects) and not item.touches_border(border):
                item.draw_object(draw, palette)
                with CodeTimer("union"):
                    placed_objects = union(placed_objects, item.get_primitive())
                break

        logger.info(f"placed {idx}. Previous tries {tries}")

    image.show()
    logger.info("--- %s seconds ---" % (time.time() - start_time))
    logger.info(len(placed_objects.geoms))
