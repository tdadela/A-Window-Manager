'''Distributes set of windows on screen'''

from awm import config


def distribute_windows(windows, *, width, height, horizontal):
    '''Draw windows in horizontal tiling mode'''
    no_windows = len(windows)
    prev_end = 0
    if horizontal:
        for i, window in enumerate(windows):
            if i == no_windows - 1:
                fill_till = width
            else:
                fill_till = width // no_windows * (i + 1)
            window.configure(
                width=fill_till - prev_end,
                height=height - config.BAR_HEIGHT,
                x=prev_end + 1,
                y=config.BAR_HEIGHT
            )
            prev_end = fill_till
    else:
        for i, window in enumerate(windows):
            if i == no_windows - 1:
                fill_till = height - config.BAR_HEIGHT
            else:
                fill_till = -config.BAR_HEIGHT + height // no_windows * (i + 1)
            window.configure(
                height=fill_till - prev_end,
                width=width,
                y=config.BAR_HEIGHT + prev_end,
                x=0
            )
            prev_end = fill_till
