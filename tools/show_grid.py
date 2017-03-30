"""
Show grid on the image
"""
import sys

from PIL import Image, ImageDraw

import os

cur_dir = os.path.dirname(os.path.realpath(__file__)) + "/"

if (len(sys.argv) < 2):
    print "Please specify image file"
    sys.exit(1)
    
XLines = 10
YLines = 10

im = Image.open(sys.argv[1])
width, heigth = im.size

ratio = 800.0 / heigth  # use height as ration defining factor
twidth = int(width * ratio)  
theigth = int(heigth * ratio)

im.thumbnail((twidth, theigth), Image.ANTIALIAS)

draw = ImageDraw.Draw(im)

for i in range(1, XLines):
    x = int(i * twidth / XLines)
    print x, 0, x, theigth
    draw.line((x, 0, x, theigth), fill=(255,0,0,255), width=3)
    
    # draw text
    draw.text((x, 10), str(i * 10), fill=(255,255,0,255))
    draw.text((x, theigth - 20), str(i * 10), fill=(255,255,0,255))
    
for j in range(1, YLines):
    y = int(j * theigth / YLines)
    draw.line((0, y, twidth, y), fill=(255,0,0,255), width=3)
    
    # draw text
    draw.text((10, y), str(j * 10), fill=(255,255,0,255))
    draw.text((twidth - 20, y), str(j * 10), fill=(255,255,0,255))



im.show()
    
