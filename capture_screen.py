#!/bin/python

import sys
import time

from subprocess import call

while True:
    # Code executed here
    call(["ls", "-l"])
    time.sleep(10)
    
    
if (len(sys.argv) < 2):
    print "Please specify device name"
    sys.exit(1) 

device = sys.argv[1]

adb shell screencap -p | sed 's/\r$//' > screen_"$(date +'%s').png"
