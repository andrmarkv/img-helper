#!/usr/bin/python

from pg import serverControl
from pg import clientAndroid as ca
from pg import pgutil
from pg import msgHandler
from pg import phoneSettings

import datetime
import sys, traceback
import os
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
    
    skipPokemons = config.getboolean("main", "skipPokemons")
    ps.skipPokemons = skipPokemons

    clearBagCount = config.getint("main", "clearBagCount")
    ps.clearBagCount = clearBagCount
    
    sectorsCount = config.getint("main", "sectorsCount")
    ps.sectorsCount = sectorsCount
    
    saveDir = config.get("main", "saveDir")
    ps.saveDir = saveDir
    
    isMaster = config.getboolean("main", "isMaster")
    ps.isMaster = isMaster
    if (isMaster):
        if config.has_section("slaveServer"):
            slaveIP = config.get("slaveServer", "ipAddr")
            slavePort = config.getint("slaveServer", "port")
            slave = (slaveIP, slavePort)
            ps.slave = slave
        else:
            print "Warning: no slave server is specified"

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