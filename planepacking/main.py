import random
import logging
import time

from shapely.geometry import Point, LineString, LinearRing
from shapely import affinity, union, STRtree
from PIL import Image, ImageDraw
import cairo
from crossproject.codetimer import CodeTimer
from primitives_library.circle import Circle
from primitives_library.rounded_square import RoundedSquare
from primitives_library.random_rectangle import RandomRectangle
from crossproject.palettes import PALETTES


c = 1.3
n = 4000
a0 = 500000

MAX_TRIES = 20

class Graph:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    XMAX = 1650
    YMAX = 2100

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, XMAX, YMAX)
    ctx = cairo.Context(surface)
    ctx.set_operator(cairo.Operator.DIFFERENCE)


    palette_name = random.choice(list(PALETTES.keys()))
    palette = PALETTES.get(palette_name)
    # palette = PALETTES.get("LOSTCENTURY")
    logger.info(f"palette is {palette_name}")

    border = LinearRing([[0, 0], [XMAX, 0], [XMAX, YMAX], [0, YMAX], [0, 0]]).buffer(100)



def init_all_primitives(c, n, a0):
    rv = [random.choice([
                RoundedSquare(area=a0 * 1 / i ** c,
                              palette=Graph.palette)
                ]) for i in range(1, n + 1)]
    return rv


def get_placement_coords(x_max, y_max):
    return (
        random.random() * x_max // 20 * 20,
        random.random() * y_max // 20 * 20
    )


if __name__ == '__main__':
    start_time = time.time()

    primitives = init_all_primitives(c, n, a0)

    placed_objects = [Point(0, 0)]
    placed_objects_strtree = STRtree(placed_objects)

    tries_logger = []
    for idx, item in enumerate(primitives):
        tries = 0
        while tries < MAX_TRIES:
            tries += 1
            x, y = get_placement_coords(Graph.XMAX, Graph.YMAX)
            item.define_object(x, y)

            if not item.overlaps(placed_objects_strtree) and not item.touches_border(Graph.border):
                item.draw_object(Graph.ctx)
                with CodeTimer("union"):
                    placed_objects = union(placed_objects, item.get_primitive())
                # with CodeTimer("str_creation"):
                placed_objects_strtree = STRtree(placed_objects)
                break

        Graph.logger.info(f"placed {idx}. Previous tries {tries}")

    Graph.surface.write_to_png('out.png')
    im = Image.open("out.png")
    im.show()

    Graph.logger.info("--- %s seconds ---" % (time.time() - start_time))
