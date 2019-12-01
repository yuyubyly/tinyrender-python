
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

    for x in range(x0, x1+1):
        t = 1.0*(x-x0)/(x1-x0)
        y = y0*(1.0-t) + y1*t
        if steep:
            image.set(y, x, color)
        else:
            image.set(x, y, color)

def main():
    model = new Model("obj/african_head.obj")

    TGAImage image(width, height, TGAImage::RGB)
    for (int i=0 i<model->nfaces() i++) {
        std::vector<int> face = model->face(i)
        for (int j=0 j<3 j++) {
            Vec3f v0 = model->vert(face[j])
            Vec3f v1 = model->vert(face[(j+1)%3])
            int x0 = (v0.x+1.)*width/2.
            int y0 = (v0.y+1.)*height/2.
            int x1 = (v1.x+1.)*width/2.
            int y1 = (v1.y+1.)*height/2.
            line(x0, y0, x1, y1, image, white)
        }
    }

    image.flip_vertically() // i want to have the origin at the left bottom corner of the image
    image.write_tga_file("output.tga")
    delete model
    return 0
}