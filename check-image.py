#!/bin/python

import sys
import os.path
import ConfigParser
import Image, time
import numpy 

"""
Function that compares two images.
It subtracts region defined by diagonal p1, p2 from each image
and verify if regions are exactly the same in both images
"""
def img_compare(img1, img2, p1, p2):
    #crop images
    imc1 = img1.crop((p1[0], p1[1], p2[0], p2[1]))
    imc2 = img2.crop((p1[0], p1[1], p2[0], p2[1]))
    imc1.save('tests/1.png')
    imc2.save('tests/2.png')

    #convert images to 3D arrays    
    a1 = numpy.array(imc1)
    a2 = numpy.array(imc2)
    
    same = numpy.array_equal(a1, a2)
    return same



if (len(sys.argv) < 2):
    print "Please specify INI file"
    sys.exit(1) 

ini_file = sys.argv[1]
if(not os.path.exists(ini_file)):
    print "INI file does not exist"
    sys.exit(1)

config = ConfigParser.ConfigParser()
config.read(ini_file)

isOK = True

section = "main"
isOK = isOK and config.has_option(section, "path")
isOK = isOK and config.has_option(section, "menu")
isOK = isOK and config.has_option(section, "main-map")
isOK = isOK and config.has_option(section, "stop-inside")
isOK = isOK and config.has_option(section, "capture-screen")

if (not isOK):
    print "Some parameters are missing in section: %s" % section
    sys.exit(1)

path = config.get(section, "path")
im_menu = Image.open(os.path.join(path, config.get(section, "menu")))
im_main_map = Image.open(os.path.join(path, config.get(section, "main-map")))
im_stop_inside = Image.open(os.path.join(path, config.get(section, "stop-inside")))
im_capture_screen = Image.open(os.path.join(path, config.get(section, "capture-screen")))

# w,h = im.size

x1 = [90, 1280]
x2 = [265, 1470]

same = img_compare(im1, im2, x1, x2)
print same


x1 = [90, 1080]
x2 = [265, 1270]

same = img_compare(im1, im2, x1, x2)
print same

