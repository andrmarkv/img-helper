#!/usr/bin/python

from pg import clientAndroid as ca
from pg import pgutil
from pg import pgconst
from pg import phoneSettings

import datetime
import sys, traceback
import os
import ConfigParser
from subprocess import check_output
from subprocess import signal
from time import sleep

"""
Read all phone specific settings from the INI 
"""
def read_phone_settings(config):
    path = config.get("main", "path")
  
    coords = pgutil.read_coords(config)
    scripts = pgutil.read_scripts(config, path)
    templates = pgutil.read_templates(config, path)
    
    ps = phoneSettings.PhoneSettings(coords, scripts, templates)
    
    saveDir = config.get("main", "saveDir")
    ps.saveDir = saveDir
    
    isMaster = config.getboolean("main", "isMaster")
    if (isMaster):
        if config.has_section("slaveServer"):
            slaveIP = config.get("slaveServer", "ipAddr")
            slavePort = config.getint("slaveServer", "port")
            slave = (slaveIP, slavePort)
            ps.slave = slave
        else:
            print "Warning: no slave server is specified"

    return ps


def get_pid(ini_file):
    tmp = check_output("ps aux | grep " + ini_file, shell=True)
    lines = tmp.split('\n')
    for line in lines:
        i = line.find("Controller.py")
        j = line.find("python")
        if i >= 0 and j >= 0:
            print "Got process: " + line
            tokens = line.split(" ")
            for token in tokens[1:]:
                if len(token) > 3 and int(token) > 0:
                    return int(token)


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
ps = read_phone_settings(config)

serverAndroidIp = config.get("clientAndroid", "ipAddr")
serverAndroidPort = config.getint("clientAndroid", "port")

pid = get_pid(ini_file)
if pid is not None and pid > 0:
    print "stopping process with pid: %d" % pid
    os.kill(pid, signal.SIGKILL)
else:
    print "No Controller process"

sleep(1)

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
    clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_ANDROID_EXIT_BUTTON), 1)
    #check if we are on a main screen
    img = clientAndroid.get_screen_as_array()
    r = pgutil.match_template(img, ps.getTemplate(pgconst.TEMPLATE_EXIT_YES_BUTTON), pgconst.MIN_RECOGNITION_VAL)
    if r[0]:
        print "Got exit confirmation screen"
        clientAndroid.send_touch(r[2], 1)
        
    img = clientAndroid.get_screen_as_array()
    r = pgutil.match_template(img, ps.getTemplate(pgconst.TEMPLATE_ANDROID_PHONE_ICON), pgconst.MIN_RECOGNITION_VAL)
    if r[0]:
        print "Got to the home Android screen, all OK!"
        break