import math
from PIL import Image

im = Image.open("test.jpg")

print(im.size)

(width, height) = im.size

box = (0, 0, int(math.floor(width*.5)), int(math.floor(height*.5)))
im.crop(box).save("out.jpg")
