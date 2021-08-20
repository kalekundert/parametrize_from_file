class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

def dot(a, b):
    return a.x * b.x + a.y * b.y
