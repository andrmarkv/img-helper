#!/usr/bin/python

from pg import serverControl
from pg import clientAndroid
from pg import pgutil
from pg import pgconst
from pg import msgHandler
from pg import phoneSettings
from pg import pgactions

import datetime
import sys
import os
import thread
import ConfigParser

"""
Read all phone specific settings from the INI 
"""
def read_phone_settings(config):
    path = config.get("main", "path")
  
    coords = pgutil.read_coords(config)
    scripts = pgutil.read_scripts(config, path)
    templates = pgutil.read_templates(config, path)
    
    ps = phoneSettings.PhoneSettings(coords, scripts, templates)

    return ps


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
isOK = isOK and config.has_section("controlServer")
isOK = isOK and config.has_section("clientAndroid")
isOK = isOK and config.has_section("swipes")
isOK = isOK and config.has_section("coords")
isOK = isOK and config.has_section("templates")

if (not isOK):
    print "Error! Some ini parameters are missing"
    sys.exit(1)

#Read all template descriptions and populate dictionary
ps = read_phone_settings(config)

serverIp = config.get("controlServer", "ipAddr")
serverPort = config.getint("controlServer", "port")

serverAndroidIp = config.get("clientAndroid", "ipAddr")
serverAndroidPort = config.getint("clientAndroid", "port")

#Create instance of the Android server to handle communication with the phone
clientAndroid =  clientAndroid.ClientAndroid(serverAndroidIp, serverAndroidPort)


#TESTING
#items_to_delete = pgconst.DEL_ITEMS_POKEYBALL | pgconst.DEL_ITEMS_NANAB_BERRY | pgconst.DEL_ITEMS_POTION | pgconst.DEL_ITEMS_RAZZ_BERRY | pgconst.DEL_ITEMS_REVIVE
#pgactions.clear_bag(clientAndroid, items_to_delete, ps)


#pgutil.click_sector(templates, (540, 960), 50, 500, 30, 60)
#pgutil.click_donut(templates, (540, 960), 50, 500, 6)
pgactions.look_around(clientAndroid, ps)

sys.exit(1)


clientAndroid.sendMessage(1, 2, "This is a test message", 100)

#Create handler class that has to handle CONTROL messages
# handler = msgHandler.MsgHandler(templates)

#Create instance of the server and pass handler to it
# server = serverControl.ServerControl(serverIp, serverPort, handler, clientAndroid)


# server.test();
# server.run()