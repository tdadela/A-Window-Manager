'''Distributes set of windows on screen'''
from turtle import width
from .config import BORDER_WIDTH, BAR_HEIGHT

from awm import config


def horizontal_mode(windows, width, height, x, y):
    no_windows = len(windows)
    prev_end = x
    for i, window in enumerate(windows):
        if i == no_windows - 1:
            fill_till = x + width
        else:
            fill_till = width // no_windows * (i + 1)
            fill_till += x
        window.configure(
            width=fill_till - prev_end - 2 * BORDER_WIDTH,
            height=height - 2 * BORDER_WIDTH,
            x=prev_end + 1,
            y=y,
            border_width=BORDER_WIDTH
        )
        prev_end = fill_till


def vertical_mode(windows, width, height, x, y):
    no_windows = len(windows)
    prev_end = y
    for i, window in enumerate(windows):
        if i == no_windows - 1:
            fill_till = y + height
        else:
            fill_till = height // no_windows * (i + 1)
            fill_till += y
        window.configure(
            height=fill_till - prev_end - 2 * BORDER_WIDTH,
            width=width - 2 * BORDER_WIDTH,
            y=prev_end,
            x=x,
            border_width=BORDER_WIDTH
        )
        prev_end = fill_till


def main_secondary_mode(windows, width, height, horizontal):
    x = 0
    y = BAR_HEIGHT
    height -= y
    if len(windows) < 2:
        horizontal_mode(windows, width, height, x, y)
        return

    if horizontal:
        horizontal_mode([windows[0]], width // 2, height, x, y)
        horizontal_mode(windows[1:], width - width // 2, height, width // 2, y)
    else:
        vertical_mode([windows[0]], width // 2, height, x, y)
        vertical_mode(windows[1:], width - width // 2, height, width // 2, y)


def distribute_windows(windows, *, geometry, horizontal, main_secondary):
    '''Draw windows in horizontal tiling mode'''
    width = geometry.width
    height = geometry.height
    if main_secondary:
        main_secondary_mode(windows, width, height, horizontal)
    elif horizontal:
        horizontal_mode(windows, width, height, 0, BAR_HEIGHT)
    else:
        vertical_mode(windows, width, height, 0, BAR_HEIGHT)
