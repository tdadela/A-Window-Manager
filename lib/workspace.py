class Workspace:

    def __init__(self, name):
        # user friendly name to be displayed in top bar
        self.name = name
        # self.active = False
        self.windows = []

    def receive_window(self, window):
        '''Add window to work space'''
        self.windows.append(window)
