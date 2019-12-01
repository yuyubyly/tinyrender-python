from geometry import Vec3
class Model(object):
    def __init__(self, filename):
        self.verts_ = []
        self.faces_ = []
        with open(filename, "rb") as infile:
            for line in infile.readlines():
                if line[0:2] == "v ":
                    v = Vec3()
                    data = line.split()
                    for i in xrange(3):
                        v.raw[i] = float(data[i+1])
                    self.verts_.append(v)
                elif line[0:2] == "f ":
                    f = []
                    data = line.split()
                    for i in xrange(len(data)-1):
                        l = data[i+1]
                        l = l.split("/")
                        f.append(int(l[0])-1)

                    self.faces_.append(f)
        print "# v#", len(self.verts_), "f#", len(self.faces_)

    def nverts(self):
        return len(self.verts_)

    def nfaces(self):
        return len(self.faces_)

    def face(self, idx):
        return self.faces_[idx]

    def vert(self, i):
        return self.verts_[i]
