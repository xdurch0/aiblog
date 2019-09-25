from PIL import Image


def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


im_orig = Image.open("logo_base.png")

im_square = make_square(im_orig, 177, fill_color=(255, 255, 255, 0))


desired = {"android-": [36, 48, 72, 96, 144, 192],
           "apple-": [57, 60, 72, 76, 114, 120, 144, 152, 180],
           "fav": [16, 32, 96],
           "ms-": [70, 144, 150, 310]}

for key in desired:
    for size in desired[key]:
        im_res = im_square.copy()
        im_res.thumbnail((size, size))
        im_res.save(key + "icon-" + str(size) + "x" + str(size) + ".png")
