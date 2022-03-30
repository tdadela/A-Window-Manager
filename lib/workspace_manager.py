from lib.node import Node
import socket


class WorkspaceManager:

    def __init__(self, geometry, no_workspaces):
        self.workspaces = [
            Node(geometry, None, None) for i in range(no_workspaces)]
        self.active_workspace = 0

        # refactor
        self.host = socket.gethostname()
        self.port = 8080


    def get_current_workspace(self):
        return self.workspaces[self.active_workspace]

    def change_workspace(self, target):
        if target == self.active_workspace:
            return
        for window in self.get_current_workspace().windows:
            # map/unmap doesn't need display.sync() to take effect
            window.unmap()

        self.active_workspace = target

        for window in self.get_current_workspace().windows:
            window.map()

        message = str(target + 1)
        breakpoint()
        with socket.socket() as s:
            s.connect((self.host, self.port))
            s.send(message.encode('utf-8'))

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

    def move_between_workspaces(self, window, target):
        self.remove_window(window)
        self.workspaces[target].add_window(window)
