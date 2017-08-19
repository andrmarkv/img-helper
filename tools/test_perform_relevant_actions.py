#!/usr/bin/python

import os
import sys

import ConfigParser

sys.path.append('../')
from pg import pgutil
from pg import clientAndroid
from pg import pgactions
from pg import phoneSettings


def read_phone_settings(config, path=None):
    if path is None:
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
    
    zonesCount = config.getint("main", "zonesCount")
    ps.zonesCount = zonesCount
    
    dotsCount = config.getint("main", "dotsCount")
    ps.dotsCount = dotsCount
    
    zonesWidth = config.getint("main", "zonesWidth")
    ps.zonesWidth = zonesWidth
    
    zonesHeight = config.getint("main", "zonesHeight")
    ps.zonesHeight = zonesHeight
    
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

if (len(sys.argv) < 2):
    print "Please specify INI file"
    sys.exit(1) 

ini_file = sys.argv[1]
if(not os.path.exists(ini_file)):
    print "INI file does not exist"
    sys.exit(1)

config = ConfigParser.ConfigParser()
config.read(ini_file)

serverAndroidIp = config.get("clientAndroid", "ipAddr")
serverAndroidPort = config.getint("clientAndroid", "port")

#Create instance of the Android server to handle communication with the phone
clientAndroid =  clientAndroid.ClientAndroid(serverAndroidIp, serverAndroidPort)

#it is possible to use method from pgactions, or local
#Read all template descriptions and populate dictionary
ps = pgutil.read_phone_settings(config)
pgactions.do_relevant_action(clientAndroid, ps)

