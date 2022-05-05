from tests.mock.mock_window import mock_window
from awm.distribute_windows import distribute_windows


def zero_windows():
    '''Case: work space without any window.'''
    screen_width = 1920
    screen_height = 1080
    windows = []
    distribute_windows(
        windows,
        width=screen_width,
        height=screen_height,
        horizontal=True)
    assert sum([win.get_area() for win in windows]) == 0


def n_windows():
    '''Case: work space with 1 to 5 windows.'''
    screen_width = 1920
    screen_height = 1080
    for no_windows in range(1, 6):
        windows = [mock_window() for i in range(no_windows)]
        distribute_windows(
            windows,
            width=screen_width,
            height=screen_height,
            horizontal=True)

        assert sum([win.get_area() for win in windows]
                   ) == screen_height * screen_width


if __name__ == '__main__':
    zero_windows()
    n_windows()
