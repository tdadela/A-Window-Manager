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

    def move_left(self, window):
        if window in self.windows:
            i = self.windows.index(window)
            if i > 0:
                self.windows[i-1], self.windows[i] = self.windows[i], self.windows[i-1]

    def move_right(self, window):
        if window in self.windows:
            i = self.windows.index(window)
            if i < len(self.windows)-1:
                self.windows[i+1], self.windows[i] = self.windows[i], self.windows[i+1]


class Node():
    '''Node in Window Tree responsible for managing windows locations'''

    def __init__(self, geometry, window, parent):
        self.geometry = geometry
        if window:
            self.windows = [window]
        else:
            self.windows = []
        self.nodes = []
        self.parent = parent

    def add_window(self, window):
        '''Add window to node or node child'''
        self.windows.append(window)

    def get_all_windows(self):
        '''Return list of all windows in current node
        and current node children'''
        windows = []
        for node in self.nodes:
            if node.children:
                windows += node.get_all_windows()

        return windows

    def remove_window(self, window):
        '''Remove window from tree'''
        if window in self.windows:
            self.windows.remove(window)
        else:
            for node in self.nodes:
                node.remove_window(window)

    def move_left(self, window):
        if window in self.windows:
            i = self.windows.index(window)
            if i > 0:
                self.windows[i-1], self.windows[i] = self.windows[i], self.windows[i-1]
        else:
            for node in self.nodes:
                node.move_left(window)

    def move_right(self, window):
        if window in self.windows:
            i = self.windows.index(window)
            if i < len(self.windows)-1:
                self.windows[i+1], self.windows[i] = self.windows[i], self.windows[i+1]
        else:
            for node in self.nodes:
                node.move_left(window)
