from math import pi
import random
import logging
import cairo
from crossproject.codetimer import CodeTimer
from crossproject.palettes import PALETTES
from PIL import Image, ImageColor


class Graph:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    XMAX = 1650
    YMAX = 2100

    final_surface = cairo.ImageSurface(cairo.FORMAT_RGB24, XMAX, YMAX)
    final_ctx = cairo.Context(final_surface)

    surface_bg = cairo.ImageSurface(cairo.FORMAT_RGB24, XMAX, YMAX)
    ctx_bg = cairo.Context(surface_bg)
    background = (item / 255 for item in ImageColor.getcolor("#574852", "RGB"))
    ctx_bg.set_source_rgb(*background)
    ctx_bg.rectangle(0, 0, XMAX, YMAX)
    ctx_bg.fill()

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, XMAX, YMAX)
    ctx = cairo.Context(surface)

    palette_name = random.choice(list(PALETTES.keys()))
    # palette = PALETTES.get(palette_name)
    palette = PALETTES.get("LOSTCENTURY")
    logger.info(f"palette is {palette}")
    ctx.set_operator(cairo.Operator.EXCLUSION)


def draw_shape(x, y, s, inverted):
    fill = (item / 255 for item in ImageColor.getcolor(random.choice(Graph.palette), "RGB"))

    Graph.ctx.save()
    Graph.ctx.translate(x, y)
    if inverted:
        Graph.ctx.rotate(pi)
    Graph.ctx.scale(1, 1)
    Graph.ctx.arc(0, 0, s, 0, pi)

    dx = 2 * s/5
    dy = s/3.3
    Graph.ctx.rel_curve_to(0, -dy, dx, -dy, dx, 0)
    Graph.ctx.rel_curve_to(0, dy, dx, dy, dx, 0)
    Graph.ctx.rel_curve_to(0, -dy, dx, -dy, dx, 0)
    Graph.ctx.rel_curve_to(0, dy, dx, dy, dx, 0)
    Graph.ctx.rel_curve_to(0, -dy, dx, -dy, dx, 0)

    Graph.ctx.set_source_rgb(*fill)
    Graph.ctx.fill()
    # Graph.ctx.set_source_rgb(*color)
    # Graph.ctx.set_line_width(s/30)
    # Graph.ctx.stroke()
    Graph.ctx.restore()


def create_shape(x, y, s, inverted):
    if s < 4:
        return
    else:
        draw_shape(x, y, s, inverted)
        if inverted:
            create_shape(x + s*0.55, y + s, s * 0.51, inverted)
            create_shape(x - s*0.55, y + s, s * 0.51, inverted)
        else:
            create_shape(x + s * 0.55, y - s, s * 0.51, inverted)
            create_shape(x - s * 0.55, y - s, s * 0.51, inverted)

if __name__ == '__main__':
    x, y1, y2, size = Graph.XMAX * 0.5, Graph.YMAX * 0.45, Graph.YMAX * 0.55, 450


    create_shape(x, y1, size, inverted=False)
    create_shape(x, y2, size, inverted=True)


    Graph.final_ctx.set_source_surface(Graph.surface_bg, 0, 0)
    Graph.final_ctx.paint()

    Graph.final_ctx.set_source_surface(Graph.surface, 0, 0)
    Graph.final_ctx.paint()


    Graph.final_surface.write_to_png('out.png')

    im = Image.open("out.png")
    im.show()