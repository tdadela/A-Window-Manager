import unittest
from awm.workspace_manager import WorkspaceManager
from tests.mock.mock_window import Geometry


class TestWorkspaceManager(unittest.TestCase):
    '''Testing WorkspaceManager class'''

    def test_initialization(self):
        '''Check state of WorkspaceManager after initialization.'''
        geometry = Geometry(1920, 1080)
        ws_mn = WorkspaceManager(geometry, 7)

        self.assertFalse(ws_mn.is_fullscreen())
        self.assertTrue(ws_mn.is_horizontal())
        self.assertFalse(ws_mn.is_main_secondary())

    def test_change_fullscreen_state(self):
        '''Changing Boolean states of WorkspaceManager'''
        geometry = Geometry(1920, 1080)
        ws_mn = WorkspaceManager(geometry, 7)

        self.assertFalse(ws_mn.is_fullscreen())
        self.assertTrue(ws_mn.is_horizontal())
        self.assertFalse(ws_mn.is_main_secondary())

        ws_mn.change_fullscreen_state()
        self.assertTrue(ws_mn.is_fullscreen())
        ws_mn.change_orientation()
        self.assertFalse(ws_mn.is_horizontal())
        ws_mn.change_view_mode()
        self.assertTrue(ws_mn.is_main_secondary())

        ws_mn.change_fullscreen_state()
        self.assertFalse(ws_mn.is_fullscreen())
        ws_mn.change_orientation()
        self.assertTrue(ws_mn.is_horizontal())
        ws_mn.change_view_mode()
        self.assertFalse(ws_mn.is_main_secondary())


if __name__ == '__main__':
    unittest.main()
