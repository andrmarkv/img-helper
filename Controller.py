#!/usr/bin/python

from pg import serverControl
from pg import serverAndroid
from pg import pgutil
from pg import pgconst
from pg import msgHandler

import datetime
import sys
import os
import thread
import ConfigParser

"""
Read section of the INI file that describes particular screen.
It should contain image and region
"""
def read_templates(config):
    path = config.get("main", "path")
    
    templates = {}

    templates[pgconst.TEMPLATE_MENU] = pgutil.read_template_description(config, pgconst.TEMPLATE_MENU, path)
    templates[pgconst.TEMPLATE_MAIN_MAP] = pgutil.read_template_description(config, pgconst.TEMPLATE_MAIN_MAP, path)
    templates[pgconst.TEMPLATE_INSIDE_POKESTOP] = pgutil.read_template_description(config, pgconst.TEMPLATE_INSIDE_POKESTOP, path)
    
    templates[pgconst.TEMPLATE_CLEAR_BAG] = pgutil.read_template_clear_bag(config, path)
    
    return templates


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
    print "Error! Some ini parameters are missing"
    sys.exit(1)

#Read all template descriptions and populate dictionary
templates = read_templates(config)

serverIp = config.get("controlServer", "ipAddr")
serverPort = config.getint("controlServer", "port")

serverAndroidIp = config.get("androidServer", "ipAddr")
serverAndroidPort = config.getint("androidServer", "port")

#Create instance of the Android server to handle communication with the phone
serverAndroid =  serverAndroid.ServerAndroid(serverAndroidIp, serverAndroidPort)
thread.start_new_thread(serverAndroid.run, ())


#TESTING
#items_to_delete = pgconst.DEL_ITEMS_POKEYBALL | pgconst.DEL_ITEMS_NANAB_BERRY | pgconst.DEL_ITEMS_POTION | pgconst.DEL_ITEMS_RAZZ_BERRY | pgconst.DEL_ITEMS_REVIVE 
#items_to_delete = pgconst.DEL_ITEMS_POKEYBALL
#pgutil.clear_bag(items_to_delete, templates)

#pgutil.click_sector(templates, (540, 960), 50, 500, 30, 60)
#pgutil.click_donut(templates, (540, 960), 50, 500, 6)
#pgutil.look_around(templates)
#sys.exit(1)


serverAndroid.sendMessage(1, 2, "This is a test message", 100)

#Create handler class that has to handle CONTROL messages
handler = msgHandler.MsgHandler(templates)

#Create instance of the server and pass handler to it
server = serverControl.ServerControl(serverIp, serverPort, handler, serverAndroid)


server.test();
server.run()