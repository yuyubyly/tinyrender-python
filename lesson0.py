


def main():
    from tgaimage import TGAColor, TGAImage
    red = TGAColor(255, 255, 0, 255)
    image = TGAImage(100, 100, TGAImage.RGB)
    for i in xrange(10):
        for j in xrange(10):
            image.set(52+i, 41+j, red)
    image.flip_vertically()
    image.write_tga_file("lesson0.tga")
    return 0

if __name__ == "__main__":
    main()