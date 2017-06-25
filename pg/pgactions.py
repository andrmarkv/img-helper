import cv2

import os
import sys
import ast
import subprocess
from PIL import Image
import time
import math

from pg import pgconst, pgutil
from time import sleep
from pg.clientAndroid import clientAndroid


"""
Clear bag main function. It has to start from the main screen (map).
Parameters:
    items - mask of the items that needs to be deleted, see DEL_ITEMS_*
    templates - dictionary of populated templates
    clientAndroid - client to handle Android requests
"""
def clear_bag(items, templates, clientAndroid):
    print "started clear_bag process, item categories to delete: " + str(items)
    #Check if we are on the main screen
    img = clientAndroid.get_screen_as_array()
                    
    if img is None:
        print "clear_bag Error! Can't capture the screen."
        return
    
    if not pgutil.is_main_map(img, templates)[0]:
        print "clear_bag Error! wrong start screen."
        pgutil.save_array_as_png(img, "/tmp/", "wrong_main_screen")
        return
    
    images = templates[pgconst.TEMPLATE_CLEAR_BAG][0]
    scripts = templates[pgconst.TEMPLATE_CLEAR_BAG][1]
    
    clientAndroid.send_swipe(scripts[0])
    
    print "Checking items..."
    
    #check items in the loop using scroll
    for i in range(0,8):
        #should be initial items list screen
        img = clientAndroid.get_screen_as_array()    
        
        resutls = pgutil.is_items_visible(img, items, images)
        if resutls is not None:
            for r in resutls:
                #Remove detected item from the list of items
                items = items & (~r[0])
                
                #Click delete button for the given item, r[2][1] should give y of the center of the match region
                clientAndroid.send_touch(r[1][1][1], r[1][2][1]) 
                
                #Click select how many items 
                for j in range (0, 1):
                    clientAndroid.send_touch(530, 580) #this is coordinates of plus_button
                
                #this is coordinates of yes button
                clientAndroid.send_touch(364, 804)
                
                print "deleted item: " + str(r[0])
        
        #Exit if we already processed all selected items
        if items <= 0 :
            sleep(2)
            break
        
        #Scroll
        clientAndroid.send_swipe(scripts[1]) 
        
    #Exiting Items menu
    #this is coordinates of yes button
    clientAndroid.send_touch(364, 1184)

    
    print "Finished clearing bag"
    
    return

def click_sector(center, r0, r1, a0, a1):
    #get dots within specified sector
    dots = pgutil.get_sector_dots(center, r0, r1, a0, a1)
    
    #click selected dots
    for dot in dots:
        clientAndroid.send_touch(dot[0], dot[1])
                        
                        
def click_donut(center, r0, r1, count):
    da = 360/count #this is angle of each sector
    a0 = 0
    for i in range (0, count):
        a1 = a0 + da
        click_sector(center, r0, r1, a0, a1)
        a0 = a1
        
        
def look_around(templates):
    #click around center
    click_donut((540, 960), 50, 500, 3)
    
    #get screen
    img = clientAndroid.get_screen_as_array()
    
    #identify screen
    result = pgutil.identify_screen(img, templates)
    
    #do actions based on the screen
    if result is None:
        #we got unknown scren, save it
        pgutil.save_array_as_png(img, "/tmp", "unknown")
        
        return
    
    if result[0] == pgconst.SCREEN_INSIDE_POKESTOP:
        send_pokestop_touch_events(templates)
    elif result[0] == pgconst.SCREEN_MAIN_MAP:
        send_close_menu_touch_events(templates)
    
    return
        
        
def send_pokestop_touch_events(templates):
    script = templates[pgconst.TEMPLATE_INSIDE_POKESTOP][3]
    subprocess.call(['/usr/bin/adb', 'shell', 'sh', script])
    
def send_close_menu_touch_events(templates):
    script = templates[pgconst.TEMPLATE_MENU][4]
    subprocess.call(['/usr/bin/adb', 'shell', 'sh', script])        

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
        result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
        
    tmp = b'\n'.join(result)
    print tmp
    
    return tmp
        
        
        
    