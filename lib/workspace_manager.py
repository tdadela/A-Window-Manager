from lib.workspace import Workspace


class WorkspaceManager:

    def __init__(self, no_workspaces):
        self.workspaces = [Workspace(str(i + 1)) for i in range(no_workspaces)]
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
