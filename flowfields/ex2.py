import datetime
import math
from math import pi, cos, sin, tan, exp
import random
import logging
import cairo
from crossproject.graph import Graph
from perlin import perlin
import matplotlib.pyplot as plt
import numpy as np
from progress.bar import Bar

CANVAS_WIDTH = 3300
CANVAS_HEIGHT = 4200
PERLIN_CELL_SIZE = 20
NOISE_SEED = 1998
HELPING_GRID_ON = False
PLOT_NOISE = False
DRAW_MAX_STEPS = 300
DRAW_STEP_LENGTH = 3
LINES_NUMBER = 10000
LINES_WIDTH_MIN = 2
LINES_WIDTH_MAX = 3
BORDER_PADDING = 100
BORDER_PADDING_ERROR = 300
CENTERS_OF_ATTRACTION_NUMBER = 3
OPERATOR = cairo.Operator.SOURCE


def randomize_coords_function():
    def uniform_distribution():
        return (
            random.uniform(BORDER_PADDING, CANVAS_WIDTH - BORDER_PADDING),
            random.uniform(BORDER_PADDING, CANVAS_HEIGHT - BORDER_PADDING)
        )

    def from_central_area():
        return (
            CANVAS_WIDTH / 2 + random.uniform(-BORDER_PADDING, BORDER_PADDING) * 3,
            CANVAS_HEIGHT / 2 + random.uniform(-BORDER_PADDING, BORDER_PADDING) * 3,
        )

    def on_the_bottom():
        return (
            random.uniform(BORDER_PADDING, CANVAS_WIDTH - BORDER_PADDING),
            CANVAS_HEIGHT - random.uniform(BORDER_PADDING, 2 * BORDER_PADDING)
        )

    def on_the_left():
        return (
            random.uniform(BORDER_PADDING, 2 * BORDER_PADDING),
            random.uniform(BORDER_PADDING, CANVAS_HEIGHT - BORDER_PADDING)
        )

    rv = random.choice([
        uniform_distribution,
        from_central_area,
        on_the_bottom,
        on_the_left
    ])
    logger.info(f"coords_function selected: {rv.__name__}")
    return rv


def randomize_step_change_function():
    main_amp = random.choice([
        1,
        0.1
    ])
    line_amp = random.choice([
        1,
        0.1,
        0.01,
        0.001,
    ])

    def just_angle(angle, _):
        return (
            DRAW_STEP_LENGTH * main_amp * cos(angle),
            DRAW_STEP_LENGTH * main_amp * sin(angle)
        )

    def angle_and_phase_multiply(angle, line_field_value):
        return (
            DRAW_STEP_LENGTH * main_amp * cos(angle * line_amp * line_field_value),
            DRAW_STEP_LENGTH * main_amp * sin(angle * line_amp * line_field_value)
        )

    def angle_and_phase_add_y(angle, line_field_value):
        return (
            DRAW_STEP_LENGTH * main_amp * cos(angle),
            DRAW_STEP_LENGTH * main_amp * sin(angle + line_field_value)
        )

    def angle_and_phase_add_x(angle, line_field_value):
        return (
            DRAW_STEP_LENGTH * main_amp * cos(angle + line_field_value),
            DRAW_STEP_LENGTH * main_amp * sin(angle)
        )

    def angle_and_separate_phase_modification_y(angle, line_field_value):
        return (
            DRAW_STEP_LENGTH * main_amp * cos(angle),
            DRAW_STEP_LENGTH * main_amp * sin(angle) + DRAW_STEP_LENGTH * sin(angle * line_amp * line_field_value)
        )

    def angle_and_separate_phase_modification_x(angle, line_field_value):
        return (
            DRAW_STEP_LENGTH * main_amp * cos(angle) + DRAW_STEP_LENGTH * cos(angle * line_amp * line_field_value),
            DRAW_STEP_LENGTH * main_amp * sin(angle)
        )

    def angle_and_phase_modification_x_y(angle, line_field_value):
        return (
            DRAW_STEP_LENGTH * main_amp * cos(angle) + DRAW_STEP_LENGTH * cos(angle * line_amp * line_field_value),
            DRAW_STEP_LENGTH * main_amp * sin(angle) + DRAW_STEP_LENGTH * sin(angle * line_amp * line_field_value)
        )

    rv = random.choice([
        just_angle,
        angle_and_phase_multiply,
        angle_and_phase_add_y,
        angle_and_phase_add_x,
        angle_and_separate_phase_modification_y,
        angle_and_separate_phase_modification_x,
        angle_and_phase_modification_x_y
    ])
    logger.info(f"step_change_function selected: {rv.__name__}")
    logger.info(f"selected main_amp: {main_amp}")
    logger.info(f"selected line_amp: {line_amp}")
    return rv


def init_flow_field(perlin_cell_size, graph, seed):
    cells_number = graph.canvas_height // perlin_cell_size
    x = np.linspace(0, 1, cells_number)
    y = np.linspace(0, 2, cells_number)
    xv, yv = np.meshgrid(x, y)
    rv = perlin(xv, yv, seed=seed)
    rv += 0.5
    rv *= 2 * pi

    logger.info(f"flow_field cells number: {cells_number}")

    #
    # x = np.linspace(-1, 1, num=cells_number)
    # y = np.linspace(-1, 1, num=cells_number)
    # xx, yy = np.meshgrid(x, y)
    # zz = np.zeros((cells_number, cells_number))
    # vv = np.zeros((cells_number, cells_number))
    #
    # for x in range(cells_number):
    #     for y in range(cells_number):
    #         zz = yy + 1j * yy
    #         vv = zz * np.exp(1j * 3 * np.pi / 5)
    #         vv = np.abs(vv)
    # dat = dat[x'] + 1j * dat['y']  # Represent positions as complex numbers
    # dat['v'] = dat['z'] * np.exp(1j * 3 * np.pi / 5)  # Create vector field by rotating z by 3pi/5.
    # dat['v'] = np.abs(dat['v'])
    # print(vv)
    #
    # rv = vv

    if PLOT_NOISE:
        plt.imshow(rv, cmap='Blues')
        plt.show()
    return rv


def init_line_field(seed, distances):
    x = np.linspace(0, 1, DRAW_MAX_STEPS)
    xv, yv = np.meshgrid(x, 1)
    rv = perlin(xv, yv, seed=seed)[0]
    rv *= 2 * pi * sum(distances)
    return rv


def draw_line(start_x, start_y, angles_field, line_field, cell_size, graph, step_change_function):
    color = graph.get_random_color_from_palette()
    ctx = graph.ctx
    ctx.set_line_width(random.randint(LINES_WIDTH_MIN, LINES_WIDTH_MAX))
    ctx.set_line_cap(cairo.LineCap.ROUND)
    current_x, current_y, draw_step = start_x, start_y, 0
    actual_border = BORDER_PADDING + random.randint(0, BORDER_PADDING_ERROR)
    while (
            graph.canvas_width - actual_border > current_x > actual_border and
            graph.canvas_height - actual_border > current_y > actual_border and
            draw_step < DRAW_MAX_STEPS
    ):
        angle = angles_field[int(current_x // cell_size), int(current_y // cell_size)]
        line_field_value = line_field[draw_step]
        step_x, step_y = step_change_function(angle, line_field_value)
        ctx.move_to(current_x, current_y)
        current_x += step_x
        current_y += step_y
        ctx.line_to(current_x, current_y)
        draw_step += 1
    ctx.set_source_rgb(*color)
    ctx.stroke()


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    random.seed(NOISE_SEED)

    graph = Graph(CANVAS_WIDTH, CANVAS_HEIGHT)
    logger.info(f"palette is {graph.palette_name}")
    graph.ctx.set_operator(OPERATOR)

    angles_field = init_flow_field(PERLIN_CELL_SIZE, graph, NOISE_SEED)
    if HELPING_GRID_ON:
        graph.draw_helping_angle_grid(angles_field, PERLIN_CELL_SIZE)

    get_coords_function = randomize_coords_function()
    centers_of_attraction = [get_coords_function() for _ in range(CENTERS_OF_ATTRACTION_NUMBER)]
    step_change_function = randomize_step_change_function()

    bar = Bar('Drawing lines: ', max=LINES_NUMBER, check_tty=False)

    for i in range(LINES_NUMBER):
        x, y = get_coords_function()
        # step_change_function = randomize_step_change_function()
        all_distances = [math.sqrt((x - xx) ** 2 + (y - yy) ** 2) for xx, yy in centers_of_attraction]
        line_field = init_line_field(NOISE_SEED, all_distances)
        draw_line(start_x=x,
                  start_y=y,
                  angles_field=angles_field,
                  line_field=line_field,
                  cell_size=PERLIN_CELL_SIZE,
                  graph=graph,
                  step_change_function=step_change_function)
        bar.next()
    bar.finish()

    file_name_template = f"../out/flowfields-ex2-{str(datetime.datetime.now())}-{NOISE_SEED}.png"
    graph.open_result(file_name_template)
