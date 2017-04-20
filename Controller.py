#!/usr/bin/python

from pg import server
from pg import pgutil
from pg import pgconst
from pg import msgHandler

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


#TESTING
pgutil.clear_bag(pgconst.DEL_ITEMS_POKEYBALL|pgconst.DEL_ITEMS_NANAB_BERRY, templates)


#Create handler class that has to handle CONTROL messages
handler = msgHandler.MsgHandler(templates)

#Create instance of the server and pass handler to it
server = server.ControlServer('localhost', 8002, handler)
server.test();
server.run()