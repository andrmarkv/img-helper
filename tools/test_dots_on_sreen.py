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

def click_donut(clientAndroid, ps, center, r0, r1, count):
    da = 360/count #this is angle of each sector
    a0 = 0
    for i in range (0, count):
        a1 = a0 + da
        click_sector(clientAndroid, center, r0, r1, a0, a1)
        a0 = a1
        
    #click center of the donut as well            
    clientAndroid.send_touch(center)
    
    print "Finished clicking donut"
    
def click_sector(clientAndroid, center, r0, r1, a0, a1):
    #get dots within specified sector
    dots = pgutil.get_sector_dots(center, r0, r1, a0, a1)
    
    #sort
    pgutil.sort_dots(center, dots, 1)
    
    #click selected dots, do not sleep after each click
    for dot in dots:
        clientAndroid.send_touch((dot[0], dot[1]), 0.1)
        
    print "Finished clicking sector"


#some helper variables
center = (360,640)

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

r0 = 50
r1 = int (center[0] * 0.8)
c = (center[0], int(center[1] * 2 * 0.7))

#it is possible to use method from pgactions, or local
#Read all template descriptions and populate dictionary
ps = read_phone_settings(config, "../conf/redmi3_720_1280")
#pgactions.click_donut(clientAndroid, ps, c, r0, r1, ps.sectorsCount)
pgactions.click_circle(clientAndroid, ps, c, 35, 10)

