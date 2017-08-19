#!/usr/bin/python

from pg import serverControl
from pg import clientAndroid as ca
from pg import pgutil
from pg import msgHandler

import datetime
import sys, traceback
import os
import ConfigParser

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
ps = pgutil.read_phone_settings(config)

serverIp = config.get("controlServer", "ipAddr")
serverPort = config.getint("controlServer", "port")

serverAndroidIp = config.get("clientAndroid", "ipAddr")
serverAndroidPort = config.getint("clientAndroid", "port")

#Create instance of the Android server to handle communication with the phone
clientAndroid = None
try:
    clientAndroid =  ca.ClientAndroid(serverAndroidIp, serverAndroidPort)
except:
    print "Error! Can't create clientAndroid, exiting..."
    traceback.print_exc()
    sys.exit(1)

#Create handler class that has to handle CONTROL messages
handler = msgHandler.MsgHandler(clientAndroid, ps)

#Create instance of the server and pass handler to it
server = serverControl.ServerControl(serverIp, serverPort, handler)
server.run()