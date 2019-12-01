import math

def line(t0, t1, image, color):
    steep = False
    x0 = t0.x
    y0 = t0.y
    x1 = t1.x
    y1 = t1.y
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