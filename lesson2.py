

from geometry import Vec2, Vec3
from tgaimage import TGAImage, TGAColor

width = 200
height = 200
def barycentric(pts, x, y):
    u = Vec3(pts[2][0] - pts[0][0], pts[1][0] - pts[0][0], pts[0][0] - x).cross(
          Vec3(pts[2][1] - pts[0][1], pts[1][1] - pts[0][1], pts[0][1] - y)
    )

    if abs(u[2]) < 1:
        return Vec3(-1, 1, 1)
    return Vec3(1.0 - (1.0 * u.x + u.y) / u.z, 1.0 * u.y / u.z, 1.0 * u.x / u.z)

def triangle(pts, image, color):
    bboxmin = Vec2(image.get_width() - 1, image.get_height() - 1)
    bboxmax = Vec2(0, 0)
    clamp = Vec2(image.get_width() - 1, image.get_height() - 1)
    for i in xrange(3):
        for j in xrange(2):
            bboxmin[j] = max(0, min(bboxmin[j], pts[i][j]))
            bboxmax[j] = min(clamp[j], max(bboxmax[j], pts[i][j]))

    for x in xrange(bboxmin.x, bboxmax.x+1):
        for y in xrange(bboxmin.y, bboxmax.y+1):
            bc_screen = barycentric(pts, x, y)
            if bc_screen.x < 0 or bc_screen.y < 0 or bc_screen.z < 0:
                continue
            image.set(x, y, color)

def main():
    frame = TGAImage(200, 200, TGAImage.RGB)
    pts = [Vec2(10, 10), Vec2(100, 30), Vec2(190, 160)]
    triangle(pts, frame, TGAColor(255, 0, 0))
    frame.flip_vertically()
    frame.write_tga_file("lesson2.tga")
    return 0

def test():
    pts = [Vec2(10, 10), Vec2(100, 30), Vec2(190, 160)]
    print barycentric(pts, 190, 51)
    return 0

def main2():
    from model import Model
    from tgaimage import TGAImage, TGAColor
    model = Model("obj/african_head.obj")

    width = 800
    height = 800

    image = TGAImage(width, height, TGAImage.RGB)
    import random
    for i in xrange(model.nfaces()):
        face = model.face(i)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        v0 = model.vert(face[0])
        v1 = model.vert(face[1])
        v2 = model.vert(face[2])

        x0 = int((v0.x + 1.) * width / 2.)
        y0 = int((v0.y + 1.) * height / 2.)
        x1 = int((v1.x + 1.) * width / 2.)
        y1 = int((v1.y + 1.) * height / 2.)
        x2 = int((v2.x + 1.) * width / 2.)
        y2 = int((v2.y + 1.) * height / 2.)

        pts = [Vec2(x0, y0), Vec2(x1, y1), Vec2(x2, y2)]
        triangle(pts, image, TGAColor(r, g, b))
        print i


    image.flip_vertically()
    image.write_tga_file("lesson2_2.tga")
    return 0


def main3():
    from model import Model
    from tgaimage import TGAImage, TGAColor
    model = Model("obj/african_head.obj")

    width = 800
    height = 800

    image = TGAImage(width, height, TGAImage.RGB)
    light_dir = Vec3(0,0,-1)

    for i in xrange(model.nfaces()):
        face = model.face(i)
        screen_coords = [Vec2(), Vec2(), Vec2(), ]
        world_coords = [Vec3(), Vec3(), Vec3(), ]

        for j in xrange(3):
            v = model.vert(face[j])
            screen_coords[j] = Vec2(int((v.x+1.)*width/2.), int((v.y+1.)*height/2.))
            world_coords[j] = v
        n = (world_coords[2]-world_coords[0]).cross(world_coords[1]-world_coords[0])
        n = n.normalize()
        intensity = n*light_dir
        if intensity>0:
            triangle([screen_coords[0], screen_coords[1], screen_coords[2]], image, TGAColor(intensity*255, intensity*255, intensity*255, 255))
        print i

    image.flip_vertically()
    image.write_tga_file("lesson2_3.tga")

if __name__ == "__main__":
    main3()
    # test()