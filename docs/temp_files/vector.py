class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

def load(path):
    vectors = []

    with open(path) as f:
        for i, line in enumerate(f):
            fields = line.split()
            if len(fields) != 2:
                raise IndexError(f"line {i+1}: expected 2 coordinates, got {len(fields)}")

            x, y = map(float, fields)
            v = Vector(x, y)
            vectors.append(v)

    return vectors
