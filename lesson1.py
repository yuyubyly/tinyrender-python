
import math
def line(x0, y0, x1, y1, image, color):
    steep = False
    if math.fabs(x0-x1)<math.fabs(y0-y1):
        t0, t1 = x0, x1
        x0, x1 = y0, y1
        y0, y1 = t0, t1
        steep = True

    if x0>x1:
        tx, ty = x0, y0
        x0, y0 = x1, y1
        x1, y1 = tx, ty

    for x in range(int(x0), int(x1)+1):
        if x0 == x1:
            return
        else:
            t = 1.0*(x-x0)/(x1-x0)
            y = int(y0*(1.0-t) + y1*t)
            if steep:
                image.set(y, x, color)
            else:
                image.set(x, y, color)

def main():
    from model import Model
    from tgaimage import TGAImage, TGAColor
    model = Model("obj/african_head.obj")

    width = 800
    height = 800
    white = TGAColor(255, 255, 255, 255)

    index = 0
    image = TGAImage(width, height, TGAImage.RGB)
    for i in xrange(model.nfaces()):
        face = model.face(i)
        for j in xrange(3):
            v0 = model.vert(face[j])
            v1 = model.vert(face[(j+1)%3])
            x0 = int((v0.x+1.)*width/2.)
            y0 = int((v0.y+1.)*height/2.)
            x1 = int((v1.x+1.)*width/2.)
            y1 = int((v1.y+1.)*height/2.)
            # print index,":",x0, y0, "|", x1, y1
            line(x0, y0, x1, y1, image, white)
            index += 1

    image.flip_vertically()
    image.write_tga_file("output.tga")
    return 0

if __name__ == "__main__":
    main()