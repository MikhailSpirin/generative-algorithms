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
    background = (item / 255 for item in ImageColor.getcolor("#CCCCCC", "RGB"))
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


def draw_cube(x, y, size):
    fill = (item / 255 for item in ImageColor.getcolor(random.choice(Graph.palette), "RGB"))

    # generate what cube has - 6 faces and 8 edges

    Graph.ctx.save()
    Graph.ctx.translate(x, y)

    Graph.ctx.move_to(0, 0)
    Graph.ctx.line_to(size, 0)
    Graph.ctx.line_to(size, size)
    Graph.ctx.line_to(0, size)
    Graph.ctx.line_to(0, 0)
    Graph.ctx.line_to(size/4, size/4)
    Graph.ctx.translate(size/4, size/4)
    Graph.ctx.line_to(size, 0)
    Graph.ctx.line_to(size, size)
    Graph.ctx.line_to(0, size)
    Graph.ctx.line_to(0, 0)

    # Graph.ctx.set_line_width(size/20)
    # Graph.ctx.set_source_rgb(*fill)
    # Graph.ctx.fill_preserve()
    Graph.ctx.set_source_rgb(0, 0, 0)
    Graph.ctx.stroke()
    # Graph.ctx.set_source_rgb(*color)
    # Graph.ctx.set_line_width(s/30)
    # Graph.ctx.stroke()
    Graph.ctx.restore()

if __name__ == '__main__':
    size = 500

    draw_cube(100, 100, size)

    Graph.final_ctx.set_source_surface(Graph.surface_bg, 0, 0)
    Graph.final_ctx.paint()
    Graph.final_ctx.set_source_surface(Graph.surface, 0, 0)
    Graph.final_ctx.paint()
    Graph.final_surface.write_to_png('out.png')

    im = Image.open("out.png")
    im.show()