#!/bin/python

import sys
import os.path
import ConfigParser
import Image
import ast
import datetime

import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.feature import match_template
from skimage.color import rgb2gray

import os
from skimage.color.colorconv import rgb2grey

#convert images to 2D arrays
def img2array(image):
    a = np.array(image)
    a = rgb2grey(a)
    return a

"""
Read section of the INI file that describes particular screen.
It should contain image and region
"""
def read_template_description(templates, path, section):
    im = Image.open(os.path.join(path, config.get(section, "file")))
    img = img2array(im)
    
    tmp = config.get(section, "region")
    region = ast.literal_eval(tmp)
    
    templates[section] = (section, img, region)
    

"""
Read section of the INI file that describes particular screen.
It should contain image and region
"""
def read_templates(path):
    templates = {}
    read_template_description(templates, path, "menu-template")
    read_template_description(templates, path, "main-map-template")
    read_template_description(templates, path, "inside-pokestop-template")
    read_template_description(templates, path, "capture-template")
    read_template_description(templates, path, "pokemons-template")
    read_template_description(templates, path, "captured-pokemon-template")
    
    return templates

"""
Function that searches for the image template in the image
deltaHeight and deltaWidth define strips where template
should be find in order to consider template to be present
"""
def img_compare(template, image):
    t0 = datetime.datetime.now()
    result = match_template(image, template[1], pad_input=True)
    ij = np.unravel_index(np.argmax(result), result.shape)
    x, y = ij[::-1]

    #check if match was found within strips intersection
    himage, wimage = image.shape
    deltaWidth = template[2][0]
    deltaHeight = template[2][1]
    
    y0 = int(himage * (deltaHeight[0] / 100.0))
    y1 = int(himage * (deltaHeight[1] / 100.0))
    x0 = int(wimage * (deltaWidth[0] / 100.0))
    x1 = int(wimage * (deltaWidth[1] / 100.0))
    
    same = True
    same = same and x >= x0 and x <= x1  
    same = same and y >= y0 and y <= y1
    
    t1 = datetime.datetime.now()
    
    print ("%s is same: %s, time: %s" % (template[0], str(same), str(t1 - t0)))
       
    return same

t0 = datetime.datetime.now()

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

isOK = isOK and config.has_option("main", "path")
isOK = isOK and config.has_section("inside-pokestop-template")

if (not isOK):
    print "Some parameters are missing in section: %s" % section
    sys.exit(1)

path = config.get("main", "path")

#Read all template descriptions and populate dictionary
templates = read_templates(path)


im = Image.open(os.path.join(path, "screens/inside-pokestop.png"))
img = img2array(im)

t1 = datetime.datetime.now()

print("Preparation time: " + str(t1 - t0))

same = img_compare(templates["inside-pokestop-template"], img)



im = im.crop((0, im.size[1]/2, im.size[0], im.size[1]))
img = img2array(im)
same = img_compare(templates["inside-pokestop-template"], img)





im = Image.open(os.path.join(path, "screens/screen_1487610814.png"))
img = img2array(im)
same = img_compare(templates["inside-pokestop-template"], img)

im = Image.open(os.path.join(path, "screens/screen_1487610848.png"))
img = img2array(im)
same = img_compare(templates["inside-pokestop-template"], img)

im = Image.open(os.path.join(path, "screens/screen_1487610848.png"))
img = img2array(im)
same = img_compare(templates["inside-pokestop-template"], img)

im = Image.open(os.path.join(path, "screens/screen_1487610848.png"))
img = img2array(im)
same = img_compare(templates["inside-pokestop-template"], img)

im = Image.open(os.path.join(path, "screens/screen_1487610848.png"))
img = img2array(im)
same = img_compare(templates["inside-pokestop-template"], img)

im = Image.open(os.path.join(path, "screens/screen_1487611251.png"))
img = img2array(im)
same = img_compare(templates["inside-pokestop-template"], img)

im = Image.open(os.path.join(path, "screens/screen_1487611229.png"))
img = img2array(im)
same = img_compare(templates["inside-pokestop-template"], img)

im = Image.open(os.path.join(path, "screens/screen_1487610589.png"))
img = img2array(im)
same = img_compare(templates["inside-pokestop-template"], img)




