class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

# start here
def to_vector(obj):
    if isinstance(obj, Vector):
        return obj

    # If the input object is a container with two elements, use those elements 
    # to construct a vector.

    try: return Vector(*obj)
    except: pass

    # If the input object has x and y attributes, use those attributes to 
    # construct a vector.
    
    try: return Vector(obj.x, obj.y)
    except: pass
