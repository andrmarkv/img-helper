#!/usr/bin/python

import os
import sys
import time

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

import ConfigParser

sys.path.append('../')
from pg import pgutil
from pg import clientAndroid
from pg import pgactions
from pg import phoneSettings
from pg import pgconst


def read_phone_settings(config, path=None):
    if path is None:
        path = config.get("main", "path")
  
    coords = pgutil.read_coords(config)
    scripts = pgutil.read_scripts(config, path)
    templates = pgutil.read_templates(config, path)
    
    ps = phoneSettings.PhoneSettings(coords, scripts, templates)
    
    sectorsCount = config.getint("main", "sectorsCount")
    ps.sectorsCount = sectorsCount
    
    zonesCount = config.getint("main", "zonesCount")
    ps.zonesCount = zonesCount
    
    dotsCount = config.getint("main", "dotsCount")
    ps.dotsCount = dotsCount
    
    zonesWidth = config.getint("main", "zonesWidth")
    ps.zonesWidth = zonesWidth
    
    zonesHeight = config.getint("main", "zonesHeight")
    ps.zonesHeight = zonesHeight


def sliding_window(box, stepSize, windowSize):
    #box diagonal coordinates
    x0 = box[0][0]
    y0 = box[0][1]
    x1 = box[1][0]
    y1 = box[1][1]
    
    # slide a window across the box
    for y in xrange(y0, y1 - stepSize, stepSize):
        for x in xrange(x0, x1 - stepSize, stepSize):
            # yield the current window
            yield (x, y)    
    
if (len(sys.argv) < 3):
    print "Please specify INI file and test_image"
    sys.exit(1) 

ini_file = sys.argv[1]
if(not os.path.exists(ini_file)):
    print "INI file does not exist"
    sys.exit(1)

file = sys.argv[2]

config = ConfigParser.ConfigParser()
config.read(ini_file)

serverAndroidIp = config.get("clientAndroid", "ipAddr")
serverAndroidPort = config.getint("clientAndroid", "port")

#Create instance of the Android server to handle communication with the phone
clientAndroid =  clientAndroid.ClientAndroid(serverAndroidIp, serverAndroidPort)

#it is possible to use method from pgactions, or local
#Read all template descriptions and populate dictionary
ps = pgutil.read_phone_settings(config)

#Read image file and convert it to grey
img = cv.cvtColor(cv.imread(file), cv.COLOR_BGR2GRAY)

(winW, winH) = (64, 64)

#Read some settings and prepare zones borders
phone_center = ps.getCoord(pgconst.COORDS_CENTER)
center = (phone_center[0], int(phone_center[1] * 2 * 0.625))
x0 = int(center[0] - (ps.zonesWidth / 2))
y0 = int(center[1] - (ps.zoneHeight / 2))
x1 = int(center[0] + (ps.zonesWidth / 2))
y1 = int(center[1] + (ps.zoneHeight / 2))

cv.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 2)
#plt.imshow(img, 'gray'),plt.show()


#img = img[y1:y0, x0:x1]
box = ((x0, y0), (x1, y1))

# loop over the sliding window for each layer of the pyramid
for (x, y) in sliding_window(box, stepSize=32, windowSize=(winW, winH)):
    cv.rectangle(img, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
    cv.imshow("Window", img)
    cv.waitKey(1)
    time.sleep(0.05)

    
#Generate zones to check
zones = pgutil.get_rectangular_zones((x0, y0), (x1, y1), ps.zonesCount * 2)

for zone in zones:
    img = cv.rectangle(img, zone[0], zone[1], (255,255,255), 1)

#plt.imshow(img, 'gray'),plt.show()


