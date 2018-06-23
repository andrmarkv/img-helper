#!/usr/bin/python

from pg import clientAndroid as ca
from pg import pgutil
from pg import pgconst
from pg import phoneSettings
from pg import pgactions

import datetime
import sys, traceback
import os
import ConfigParser
import numpy as np
from time import sleep
from setuptools.command.build_ext import if_dl

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
isOK = isOK and config.has_section("clientAndroid")
isOK = isOK and config.has_section("swipes")
isOK = isOK and config.has_section("coords")
isOK = isOK and config.has_section("templates")

if (not isOK):
    print "Error! Some ini parameters are missing"
    sys.exit(1)

#Read all template descriptions and populate dictionary
ps = pgutil.read_phone_settings(config)

serverAndroidIp = config.get("clientAndroid", "ipAddr")
serverAndroidPort = config.getint("clientAndroid", "port")

status = 0
img = None

#this loop has to start and restart application if it stopped
while True:

    #Create instance of the Android server to handle communication with the phone
    clientAndroid = None
    try:
        clientAndroid =  ca.ClientAndroid(serverAndroidIp, serverAndroidPort)
    except:
        print "Error! Can't create clientAndroid, exiting..."
        traceback.print_exc()
        sys.exit(1)
    
    i = 0
    while (i < 10):
        i = i + 1 
            
        img = clientAndroid.get_screen_as_array()
        r = pgutil.match_template(img, ps.getTemplate(pgconst.TEMPLATE_ANDROID_PG_ICON), pgconst.MIN_RECOGNITION_VAL)
        if r[0]:
            print "got Android screen, launching pg..."
            clientAndroid.send_touch(r[2])
            status = 1;
            break
        
    
    if status < 1:
        print "Error! Can't get PG icon, exiting..."
        pgutil.save_array_as_png(img, ps.saveDir, "problem_getting_android_screen")
        sys.exit(1)
    else:
        #reset status
        status = 0
    
    #check if we got main screen
    i = 0
    img0 = None
    sameCount = 0
    while (i < 100):
        i = i + 1
        img = clientAndroid.get_screen_as_array()
        r = pgutil.match_template(img, ps.getTemplate(pgconst.TEMPLATE_POKEYBALL_MAP_SCREEN), pgconst.MIN_RECOGNITION_VAL)
        if r[0]:
            print "got main map screen, restart was OK!"
            #clientAndroid.send_touch(r[2])
            status = 2;
            break
        
        r = pgutil.match_template(img, ps.getTemplate(pgconst.TEMPLATE_EXIT_YES_BUTTON), pgconst.MIN_RECOGNITION_VAL)
        if r[0]:
            print "got initial screen, restart was OK!"
            clientAndroid.send_touch(r[2])
            status = 3;
            break
        
        print "waiting for the main screen, i = %d, sameCount = %d" % (i, sameCount)
        if (i > 1 and img0 is not None):
            # do check only if size of the images is the same (flipped screen case)
            if(np.shape(img)[0] == np.shape(img0)[0]):
                a = pgutil.crop(img, 70, 200)
                a0 = pgutil.crop(img0, 70, 200)
                r = pgutil.match_template(a, a0, pgconst.MIN_RECOGNITION_VAL * 0.001)
                if(r[0]):
                    sameCount = sameCount + 1
        img0 = img
        
        # Restart if we stuck on the loading screen
        if(sameCount > 60):
            # Exit waiting loop as we need to restart app
            status = 4
            break
        
        sleep(1)

    if status < 1:
        print "Error! Can't get into the game, exiting..."
        pgutil.save_array_as_png(img, ps.saveDir, "problem_starting_game")
        sys.exit(1)
    else:
        #reset status
        status = 0
        
    # Perform restart buttons
    if status == 4:
        pgactions.force_exit_app(clientAndroid, ps)
        continue
        
    sleep(3)
    print "Zooming out main screen"
    clientAndroid.send_swipe(ps.getScript(pgconst.SCRIPT_ZOOM_OUT))
        
    print "Restart was OK! Starting controller..."
    
    clientAndroid.exit()
    
    os.system("./Controller.py " + ini_file)
    
    print "Discovered that PG app stopped, restarting everything..."
    
    