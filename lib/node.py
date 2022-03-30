'''Window Tree for managing windows locations'''
from enum import Enum


class Orientation (Enum):
    horizontal = 0
    vertical = 1


class Node():
    '''Node in Window Tree responsible for managing windows locations'''

    def __init__(self, geometry, window, parent,
                 orientation=Orientation.horizontal):
        self.geometry = geometry
        if window:
            self.children = [window]
        else:
            self.children = []
        self.parent = parent
        self.orientation = orientation

    def add_window(self, window):
        '''Add window to node or node child'''
        self.children.append(window)

    def get_all_windows(self):
        '''Return list of all windows in current node
        and current node children'''
        windows = []
        for node in self.children:
            if isinstance(node, Node):
                if node.children:
                    windows += node.get_all_windows()
            else:
                windows.append(node)

        return windows

    def remove_window(self, window):
        '''Remove window from tree'''
        if window in self.children:
            self.children.remove(window)
        else:
            for node in self.children:
                if isinstance(node, Node):
                    node.remove_window(window)

    def move_left(self, window):
        if window in self.children:
            i = self.children.index(window)
            if i > 0:
                self.children[i -
                              1], self.children[i] = self.children[i], self.children[i -
                                                                                     1]
        else:
            for node in self.children:
                node.move_left(window)

    def move_right(self, window):
        if window in self.children:
            i = self.children.index(window)
            if i < len(self.children) - 1:
                if isinstance(self.children[i + 1], Node):
                    self.children.remove(window)
                    self.children[i].add_window(window)
                else:
                    self.children[i +
                                  1], self.children[i] = self.children[i], self.children[i +
                                                                                         1]
        else:
            for node in self.children:
                node.move_left(window)
