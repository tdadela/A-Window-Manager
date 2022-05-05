class mock_window():
    """Fake window for testing tiling."""

    def __init__(self):
        self.height = None
        self.width = None
        self.x_start = None
        self.y_start = None

    def configure(self, height, width, x, y):
        """Set window position and size."""
        self.height = height
        self.width = width
        self.x_start = x
        self.y_start = y

    def get_area(self):
        '''Area of window.'''
        return self.height * self.width
