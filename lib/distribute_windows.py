'''Distributes set of windows on screen'''


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
                height=height,
                x=prev_end + 1,
                y=0
            )
            prev_end = fill_till
    else:
        for i, window in enumerate(windows):
            if i == no_windows - 1:
                fill_till = height
            else:
                fill_till = height // no_windows * (i + 1)
            window.configure(
                height=fill_till - prev_end,
                width=width,
                y=prev_end + 1,
                x=0
            )
            prev_end = fill_till
