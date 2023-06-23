class InvalidCoordinateException(Exception):
    def __init__(self, x,y):
        self.x = x
        self.y = y
    
    def getError(self):
        return f"ERROR: Invalid Coordinate: ({self.x},{self.y})"