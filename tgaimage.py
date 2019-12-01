
import struct
class TGA_Header(object):
    TYPE = [
        (1, "idlength"),
        (1, "colormaptype"),
        (1, "datatypecode"),
        (2, "colormaporigin"),
        (2, "colormaplength"),
        (1, "colormapdepth"),
        (2, "x_origin"),
        (2, "y_origin"),
        (2, "width"),
        (2, "height"),
        (1, "bitsperpixel"),
        (1, "imagedescriptor"),
    ]

    def __init__(self):
        self.idlength = 0
        self.colormaptype = 0
        self.datatypecode = 0
        self.colormapdepth = 0
        self.bitsperpixel = 0
        self.imagedescriptor = 0
        self.colormaporigin = 0
        self.colormaplength = 0
        self.x_origin = 0
        self.y_origin = 0
        self.width = 0
        self.height = 0

    def serialise(self):
        data = ""
        for byte, name in self.TYPE:
            if byte == 1:
                data += struct.pack("c", chr(getattr(self, name)))
            elif byte == 2:
                data += struct.pack("H", getattr(self, name))
        return data

    def dump(self, f):
        for byte, name in self.TYPE:
            if byte == 1:
                c = struct.unpack("c", f.read(byte))[0]
                setattr(self, name, ord(c))
            elif byte == 2:
                setattr(self, name, struct.unpack("H", f.read(byte))[0])

class TGAColor(object):
    def __init__(self, *args):
        if len(args) == 0:
            self.bgra = [0,0,0,0]
            self.bytespp = 1
        elif len(args) == 1:
            self.bgra = [args[0], 0, 0, 0]
            self.bytespp = 1
        elif len(args) == 2:
            self.bgra = [0, 0, 0, 0]
            for i,bgra in enumerate(args[0]):
                self.bgra[i] = bgra
            self.bytespp = args[1]
        else:
            self.bgra = [0, 0, 0, 255]
            for i, bgra in enumerate(args):
                self.bgra[i] = bgra
            self.bytespp = 4

class TGAImage(object):
    GRAYSCALE = 1
    RGB = 3
    RGBA = 4

    def __init__(self,w = 0,h = 0,bpp = 0):
        self.width = w
        self.height = h
        self.bytespp = bpp
        nbytes = w * h * bpp
        self.data = [0 for i in xrange(nbytes)]

    def get_serialised_data(self, start, size):
        data = ""
        for i in xrange(size):
            data += struct.pack("B", self.data[start+i])
        return data

    def flip_vertically(self):
        if not self.data:
            return False

        bytes_per_line = self.width * self.bytespp
        half = self.height >> 1
        for j in xrange(half):
            l1 = j * bytes_per_line
            l2 = (self.height-1-j) * bytes_per_line
            self.data[l1:l1+bytes_per_line], self.data[l2:l2+bytes_per_line] = \
                self.data[l2:l2 + bytes_per_line], self.data[l1:l1 + bytes_per_line]
        return

    def flip_horizontally(self):
        if not self.data:
            return False

        half = self.width >> 1
        for i in xrange(half):
            for j in xrange(self.height):
                c1 = self.get(i, j)
                c2 = self.get(self.width-1-i, j)
                self.set(i, j, c2)
                self.set(self.width-1-i, j, c1)
        return True


    def _load_rle_data(self, f):
        pixelcount = self.width * self.height
        currentpixel = 0
        currentbyte = 0
        colorbuffer = TGAColor()

        while currentpixel < pixelcount:
            chunkheader = f.read(1)
            if chunkheader < 128:
                chunkheader += 1
                for i in xrange(chunkheader):
                    for t in xrange(self.bytespp):
                        colorbuffer.bgra[t] = f.read(1)

                    for t in xrange(self.bytespp):
                        self.data[currentbyte] = colorbuffer.bgra[t]
                        currentbyte += 1
                    currentpixel += 1
                    if currentpixel > pixelcount:
                        print "Too many pixels read\n"
                        return False
            else:
                chunkheader -= 127
                for t in xrange(self.bytespp):
                    colorbuffer.bgra[t] = f.read(1)

                for i in xrange(chunkheader):
                    for t in xrange(self.bytespp):
                        self.data[currentbyte] = colorbuffer.bgra[t]
                        currentbyte += 1
                    currentpixel += 1
                    if currentpixel > pixelcount:
                        print "Too many pixels read\n"
                        return False
        return True

    def read_tga_file(self, filename):
        if self.data:
            self.data = []

        with open(filename, "rb") as f:
            header = TGA_Header()
            header.dump(f)

            width = header.width
            height = header.height
            bytespp = header.bitsperpixel >> 3
            if width <= 0 or height <= 0 or (bytespp != TGAImage.GRAYSCALE and bytespp != TGAImage.RGB and bytespp != TGAImage.RGBA):
                return False

            nbytes = bytespp * width * height

            self.data = [0 for i in xrange(nbytes)]
            if 3 == header.datatypecode or 2 == header.datatypecode:
                for t in xrange(nbytes):
                    self.data[t] = f.read(1)
            elif 10 == header.datatypecode or 11 == header.datatypecode:
                if not self._load_rle_data(f):
                    print "an error occured while reading the data\n"
                    return False
            else:
                print "unknown file format %d \n" % header.datatypecode
                return False

            if not header.imagedescriptor & 0x20:
                self.flip_vertically()

            if header.imagedescriptor & 0x10:
                self.flip_horizontally()
            print width, "x", height, "/", bytespp * 8, "\n"
            return True

    def get(self, x, y):
        if not self.data or x < 0 or y < 0 or x >= self.width or y >= self.height:
            return TGAColor()
        t = x + y * self.width
        data = []
        for i in xrange(self.bytespp):
            data.append(self.data[t+i])
        return TGAColor(data, self.bytespp)

    def set(self, x, y, c):
        if not self.data or x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False

        for i in xrange(self.bytespp):
            self.data[(x + y * self.width) * self.bytespp+i] = c.bgra[i]
        return True

    def unload_rle_data(self, f):
        max_chunk_length = 128
        npixels = self.width * self.height
        curpix = 0
        while curpix < npixels:
            chunkstart = curpix * self.bytespp
            curbyte = curpix * self.bytespp
            run_length = 1
            raw = True
            while curpix + run_length < npixels and run_length < max_chunk_length:
                succ_eq = True
                for t in xrange(self.bytespp):
                    succ_eq = (self.data[curbyte + t] == self.data[curbyte + t + self.bytespp])
                    if not succ_eq:
                        break

                curbyte += self.bytespp
                if 1 == run_length:
                    raw = not succ_eq

                if raw and succ_eq:
                    run_length -= 1
                    break
                if not raw and not succ_eq:
                    break
                run_length += 1
            curpix += run_length
            f.write(struct.pack("B", run_length-1 if raw else run_length+127))
            f.write(self.get_serialised_data(chunkstart, run_length * self.bytespp if raw else self.bytespp))

        return True

    def write_tga_file(self, filename, rle = True):
        developer_area_ref = [0, 0, 0, 0]
        extension_area_ref = [0, 0, 0, 0]
        footer = ['T', 'R', 'U', 'E', 'V', 'I', 'S', 'I', 'O', 'N', '-', 'X', 'F', 'I', 'L', 'E', '.', '\0']

        with open(filename, 'wb') as f:
            header = TGA_Header()
            header.bitsperpixel = self.bytespp << 3
            header.width = self.width
            header.height = self.height
            if rle:
                header.datatypecode = 11 if self.bytespp == TGAImage.GRAYSCALE else 10
            else:
                header.datatypecode = 3 if self.bytespp == TGAImage.GRAYSCALE else 2
            header.imagedescriptor = 0x20

            data = header.serialise()
            f.write(data)

            if not rle:
                f.write(self.get_serialised_data(0, self.width * self.height * self.bytespp))
            else:
                if not self.unload_rle_data(f):
                    print "can't unload rle data\n"
                    return False


            data = ""
            for c in developer_area_ref:
                data += struct.pack("B", c)

            for c in extension_area_ref:
                data += struct.pack("B", c)

            for c in footer:
                data += struct.pack("c", c)
            f.write(data)
            return True
