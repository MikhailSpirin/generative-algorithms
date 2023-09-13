from math import cos,sin,pi
import random
import cairo
from PIL import ImageColor, Image
from .palettes import PALETTES


class Graph:
    def __init__(self, canvas_width=None, canvas_height=None, palette_name=None):
        self.final_surface = None
        self.final_ctx = None
        self.surface_bg = None
        self.ctx_bg = None
        self.bg_color = "#000000"
        self.surface = None
        self.ctx = None
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        if palette_name:
            self.palette_name = palette_name
            self.palette = PALETTES.get(palette_name)
        else:
            print("here")

            self.palette_name = random.choice(list(PALETTES.keys()))
            self.palette = PALETTES.get(self.palette_name)

        self.init_cairo()

    def init_cairo(self):
        self.final_surface = cairo.ImageSurface(cairo.FORMAT_RGB24, self.canvas_width, self.canvas_height)
        self.final_ctx = cairo.Context(self.final_surface)
        self.surface_bg = cairo.ImageSurface(cairo.FORMAT_RGB24, self.canvas_width, self.canvas_height)
        self.ctx_bg = cairo.Context(self.surface_bg)

        self.ctx_bg.set_source_rgb(*(item / 255 for item in ImageColor.getcolor(self.bg_color, "RGB")))
        self.ctx_bg.rectangle(0, 0, self.canvas_width, self.canvas_height)
        self.ctx_bg.fill()

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.canvas_width, self.canvas_height)
        self.ctx = cairo.Context(self.surface)
        # self.ctx.set_operator(cairo.Operator.DIFFERENCE)

    def get_random_color_from_palette(self):
        return (item / 255 for item in ImageColor.getcolor(random.choice(self.palette), "RGB"))

    def open_result(self, out_file_name=None):
        self.final_ctx.set_source_surface(self.surface_bg, 0, 0)
        self.final_ctx.paint()
        self.final_ctx.set_source_surface(self.surface, 0, 0)
        self.final_ctx.paint()
        self.final_surface.write_to_png(out_file_name)

        im = Image.open(out_file_name)
        im.show()

    def draw_helping_angle_grid(self, field, step):
        self.ctx_bg.set_line_width(1)
        self.ctx_bg.stroke()
        self.ctx_bg.set_source_rgba(1, 0.5, 0.5, 1)
        for i, row in enumerate(zip(*field)):
            for j, cell in enumerate(row):
                self.ctx_bg.arc(i*step, j*step, 3, 0, 2 * pi)
                self.ctx_bg.stroke()

        self.ctx_bg.set_source_rgba(1, 1, 0, 0.7)
        for i, row in enumerate(zip(*field)):
            for j, cell in enumerate(row):
                self.ctx_bg.save()

                self.ctx_bg.translate(j * step, i * step)
                # self.ctx_bg.rectangle(0, 0, step, step)
                self.ctx_bg.move_to(0, 0)
                # print(f"grid:{i} {j} {field[i, j]}, {field[i, j] / pi * 180}")
                x = step * 0.8 * cos(cell)
                y = step * 0.8 * sin(cell)
                self.ctx_bg.line_to(x, y)
                self.ctx_bg.arc(x, y, 1, 0, 2*pi)
                self.ctx_bg.stroke()
                self.ctx_bg.restore()
