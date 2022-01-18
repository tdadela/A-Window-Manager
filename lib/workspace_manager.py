from lib.tree import Tree


class WorkspaceManager:

    def __init__(self, geometry, no_workspaces):
        self.workspaces = [Tree(geometry) for i in range(no_workspaces)]
        self.active_workspace = 0

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

        # self.draw_windows()

    def receive_window(self, window):
        self.workspaces[
            self.active_workspace].add_window(window)
