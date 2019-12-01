
class Vec2(object):
    def __init__(self, u = 0, v = 0):
        self.raw = [u, v]

    def __getitem__(self, index):
        return self.raw[index]

    def __setitem__(self, index, value):
        self.raw[index] = value

    def __getattr__(self, item):
        if item in ("x", "u"):
            return self.raw[0]
        elif item in ("y", "v"):
            return self.raw[1]
        else:
            raise ValueError

    def __setattr__(self, item, value):
        if item in ("x", "u"):
            self.raw[0] = value
        elif item in ("y", "v"):
            self.raw[1] = value
        elif item == "raw":
            self.__dict__[item] = value
        else:
            raise ValueError

    def __add__(self, other):
        return Vec2(self.u + other.u, self.v + other.v)

    def __sub__(self, other):
        return Vec2(self.u - other.u, self.v - other.v)

    def __mul__(self, f):
        return Vec2(self.u * f, self.v * f)

    def __str__(self):
        s = "(%s , %s)"  % (self.u, self.v)
        return s

class Vec3(object):
    def __init__(self, x = 0, y = 0, z = 0):
        self.raw = [x, y, z]

    def __getitem__(self, index):
        return self.raw[index]

    def __setitem__(self, index, value):
        self.raw[index] = value

    def __getattr__(self, item):
        if item in ("x", "ivert"):
            return self.raw[0]
        elif item in ("y", "iuv"):
            return self.raw[1]
        elif item in ("z", "inorm"):
            return self.raw[2]
        else:
            raise ValueError

    def __setattr__(self, item, value):
        if item in ("x", "ivert"):
            self.raw[0] = value
        elif item in ("y", "iuv"):
            self.raw[1] = value
        elif item in ("z", "inorm"):
            self.raw[2] = value
        elif item == "raw":
            self.__dict__[item] = value
        else:
            raise ValueError

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __str__(self):
        s = "(%s, %s, %s)" % (self.x, self.y, self.z)
        return s

    def cross(self, other):
        return Vec3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def norm(self):
        import math
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def normalize(self, l=1):
        other = l/self.norm()
        return Vec3(self.x * other, self.y * other, self.z * other)