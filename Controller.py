#!/usr/bin/python

from pg import server
from pg import pgutil
from pg import pgconst

import datetime
import sys
import os
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


server = server.ControlServer('localhost', 8002)
server.test();
server.run()