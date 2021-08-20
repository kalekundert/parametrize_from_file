import math

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalize(self):
        m = math.sqrt(self.x**2 + self.y**2)

        if m == 0:
            raise NullVectorError
        else:
            self.x /= m
            self.y /= m

class NullVectorError(Exception):
    pass
