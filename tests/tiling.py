import unittest
from tests.mock.mock_window import MockWindow, Geometry
from awm.distribute_windows import distribute_windows


resolutions = [(500, 500), (1378, 768), (1920, 1080), (4000, 2000)]

class TestWindowDistribution(unittest.TestCase):

    def test_screen_covering(self):
        '''Check if windows cover full screen'''
        for (width, height) in resolutions:
            geometry = Geometry(width, height)
            for horizontal in [True, False]:
                    n_windows(horizontal, False, geometry)

    def test_distribute_zero_windows(self):
        '''Check distribute_windows if there is no window'''
        for (width, height) in resolutions:
            geometry = Geometry(width, height)
            for horizontal in [True, False]:
                zero_windows(horizontal, geometry)


def zero_windows(is_horizontal, geometry):
    '''Case: work space without any window.'''
    windows = []
    distribute_windows(
        windows,
        geometry=geometry,
        main_secondary=False,
        horizontal=is_horizontal)
    assert sum([win.get_area() for win in windows]) == 0


def n_windows(is_horizontal, main_secondary, geometry):
    '''Case: work space with 1 to 5 windows.'''
    for no_windows in range(1, 2):
        windows = [MockWindow() for i in range(no_windows)]
        distribute_windows(
            windows,
            geometry=geometry,
            main_secondary=main_secondary,
            horizontal=is_horizontal)
        
        '''
        for win in windows:
            print(f"{len(windows)=}")
            print(f"{win.get_area()=}")
        '''
        assert sum([win.get_area() for win in windows]
                   ) == geometry.height * geometry.width


if __name__ == '__main__':
    unittest.main()
