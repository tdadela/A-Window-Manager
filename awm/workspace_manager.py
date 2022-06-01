import socket
from awm.node import Node


class WorkspaceManager:

    def __init__(self, geometry, no_workspaces):
        self.workspaces = [
            Node(geometry, None, None) for i in range(no_workspaces)]
        self.fullscreen_mode = [False for i in range(no_workspaces)]
        self.main_secondary_mode = [False for i in range(no_workspaces)]
        self.horizontal_orientation = [True for i in range(no_workspaces)]
        self.active_workspace = 0

        # refactor
        self.host = socket.gethostname()
        self.port = 8080

    def is_fullscreen(self):
        '''Check if current work space is in full screen mode.'''
        return self.fullscreen_mode[self.active_workspace]

    def is_horizontal(self):
        '''Check if current work space is in full screen mode.'''
        return self.horizontal_orientation[self.active_workspace]

    def is_main_secondary(self):
        return self.main_secondary_mode[self.active_workspace]

    def change_fullscreen_state(self):
        '''Enable/disable full screen mode in current work space.'''
        self.fullscreen_mode[self.active_workspace] = not self.fullscreen_mode[self.active_workspace]

    def change_orientation(self):
        '''Switch between horizontal, vertical orientation in current work space.'''
        self.horizontal_orientation[self.active_workspace] = not self.horizontal_orientation[self.active_workspace]

    def change_view_mode(self):
        '''Switch between default and main-secondary orientation in current work space.'''
        self.main_secondary_mode[self.active_workspace] = not self.main_secondary_mode[self.active_workspace]

    def get_current_workspace(self):
        return self.workspaces[self.active_workspace]

    def change_workspace(self, target):
        if target == self.active_workspace:
            return
        for window in self.get_current_workspace().get_all_windows():
            # map/unmap doesn't need display.sync() to take effect
            window.unmap()

        self.active_workspace = target

        for window in self.get_current_workspace().get_all_windows():
            window.map()

        message = str(target + 1)
        with socket.socket() as soc:  # TODO: Jakub, please, improve this part of code
            try:                      # xd ~Jakub
                soc.connect((self.host, self.port))
                soc.send(message.encode('utf-8'))
            except BaseException:
                pass

        # self.draw_windows()

    def receive_window(self, window):
        self.workspaces[
            self.active_workspace].add_window(window)

    def remove_window(self, window):
        window.unmap()
        for wsp in self.workspaces:
            wsp.remove_window(window)

    def move_window_left(self, window):
        self.workspaces[
            self.active_workspace].move_left(window)

    def move_window_right(self, window):
        self.workspaces[
            self.active_workspace].move_right(window)

    # TODO consider changing name to move_window_to_other_workspace
    def move_between_workspaces(self, window, target):
        self.remove_window(window)
        self.workspaces[target].add_window(window)
