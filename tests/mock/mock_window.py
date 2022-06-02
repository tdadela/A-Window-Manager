class Geometry:
    """Geometry of a screen. """

    def __init__(self, width, height):
        self.width = width
        self.height = height



class MockWindow():
    """Fake window for testing tiling."""

    def __init__(self):
        self.height = None
        self.width = None
        self.x_start = None
        self.y_start = None
        self.border_width = None

    def configure(self, height, width, x, y, *, border_width):
        """Set window position and size."""
        self.height = height
        self.width = width
        self.x_start = x
        self.y_start = y
        self.border_width = border_width

    def get_area(self):
        '''Area of window.'''
        return (self.border_width * 2 + self.height) * (self.border_width * 2 + self.width)
