import datetime
from math import pi, cos, sin
import random
import logging
import cairo
from crossproject.codetimer import CodeTimer
from crossproject.graph import Graph
from perlin import perlin
import matplotlib.pyplot as plt
import numpy as np


CANVAS_WIDTH = 1650
CANVAS_HEIGHT = 2100
PERLIN_CELL_SIZE = 15
NOISE_SEED = 234563
HELPING_GRID_ON = False
PLOT_NOISE = False
DRAW_MAX_STEPS = 140
DRAW_STEP_LENGTH = 3
LINES_NUMBER = 1000
LINES_WIDTH_MIN = 3
LINES_WIDTH_MAX = 7
BORDER_PADDING = 100
BORDER_PADDING_ERROR = 300


def init_flow_field(perlin_cell_size, graph, seed):
    cells_number = graph.canvas_height // perlin_cell_size
    x = np.linspace(0, 1, cells_number)
    y = np.linspace(0, 1, cells_number)
    xv, yv = np.meshgrid(x, y)
    rv = perlin(xv, yv, seed=seed)
    rv += 0.5
    rv *= 2 * pi

    print(cells_number)

    if PLOT_NOISE:
        plt.imshow(rv, cmap='Blues')
        plt.show()
    return rv


def draw_line(start_x, start_y, angles_field, cell_size, graph):
    color = graph.get_random_color_from_palette()
    ctx = graph.ctx
    ctx.set_line_width(random.randint(LINES_WIDTH_MIN, LINES_WIDTH_MAX))
    ctx.set_line_cap(cairo.LineCap.ROUND)
    x, y, draw_step = start_x, start_y, 0
    actual_border = BORDER_PADDING + random.randint(0, BORDER_PADDING_ERROR)
    while (
            graph.canvas_width - actual_border> x > actual_border and
            graph.canvas_height - actual_border > y > actual_border and
            draw_step < DRAW_MAX_STEPS
    ):

        angle = angles_field[int(x // cell_size), int(y // cell_size)]
        step_x = DRAW_STEP_LENGTH * cos(angle)
        step_y = DRAW_STEP_LENGTH * sin(angle)
        ctx.move_to(x, y)
        x, y = x + step_x, y + step_y

        ctx.line_to(x, y)

        draw_step += 1
    ctx.set_source_rgb(*color)
    ctx.stroke()


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    graph = Graph(CANVAS_WIDTH, CANVAS_HEIGHT)
    angles_field = init_flow_field(PERLIN_CELL_SIZE, graph, NOISE_SEED)

    if HELPING_GRID_ON:
        graph.draw_helping_angle_grid(angles_field, PERLIN_CELL_SIZE)

    for i in range(LINES_NUMBER):
        x, y = random.uniform(100, CANVAS_WIDTH - 100), random.uniform(100, CANVAS_HEIGHT - 100)

        draw_line(start_x=x,
                  start_y=y,
                  angles_field=angles_field,
                  cell_size=PERLIN_CELL_SIZE,
                  graph=graph)

    file_name_template = f"../out/flowfields-ex1-{str(datetime.datetime.now())}.png"
    graph.open_result(file_name_template)
