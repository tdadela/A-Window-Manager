'''Window Tree for managing windows locations'''


class Tree():
    '''Window Tree for managing windows locations'''

    def __init__(self, geometry):
        self.height = geometry.height
        self.width = geometry.width
        self.windows = []
        self.nodes = []

    def add_window(self, window):
        '''Add window to tree'''
        self.windows.append(window)

    def remove_window(self, window):
        '''Remove window from tree'''
        if window in self.windows:
            self.windows.remove(window)

    def receive_window(self, window):
        self.windows.append(window)

    def get_all_windows(self):
        '''Return list of all windows'''
        return self.windows


class Node():

    def __init__(self, window):
        self.windows = [window]
        self.nodes = []

    def add_window(self, window):
        self.windows.append(window)

    def get_all_windows(self):
        windows = []
        for node in self.nodes:
            if node.children:
                windows += node.get_all_windows()

        return windows
