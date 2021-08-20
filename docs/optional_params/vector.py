import math

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

def from_angle(angle, *, unit='rad', magnitude=1):
    if unit == 'deg':
        angle = math.radians(angle)

    x = magnitude * math.cos(angle)
    y = magnitude * math.sin(angle)

    return Vector(x, y)

