import cv2

import os
import sys
import ast
import subprocess
import StringIO
from PIL import Image
import numpy as np
import time
import math

from pg import pgconst
from time import sleep

"""
execute adb screen capture and return it
as numpy array of bytes (grey two dimentional, suitable for cv2 operations)
Array is equal to cv2.imread('file.png', 0)
"""
def get_screen_as_array():
    out = subprocess.check_output(['/usr/bin/adb', 'exec-out', 'screencap' , '-p'])
    if out is not None:
        io = StringIO.StringIO(out)
        im = Image.open(io)

        if im is not None:
            a = np.array(im.convert('L'))
            return a

        return None


"""
Vefify if image contains template.
Image and template are numpy two dimensional arrays
min_reconition_val is indicator of template to be found in the image. Reasonable value is 0.01
retuns tuple of (True/False, min_val, center, min_loc), where
    True - indicates that template is present in the image,
    min_val - is a value indicating global minimum while searching template
    center - is center of the location where that minimum was found
    min_loc - is top left corner of the location where that minimum was found
"""
def match_template(image, template, min_reconition_val):
    w, h = template.shape[::-1]
    
    method = cv2.TM_SQDIFF_NORMED
    
    result = None;
    
    res = cv2.matchTemplate(image, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    top_left = min_loc
    center = (top_left[0] + w/2, top_left[1] + h/2)
    
    if min_val < min_reconition_val:
        result = (True, min_val, center, min_loc);
    else:
        result = (False, min_val, center, min_loc);

    return result


"""
Read section of the INI file that describes particular screen.
It should contain image and region
"""
def read_template_description(config, section, path):
    im = cv2.imread(os.path.join(path, config.get(section, "file")), 0)
    
    tmp = config.get(section, "region")
    region = ast.literal_eval(tmp)

    script = config.get(section, "script")
    script_close = config.get(section, "script_close")
    
    template = (section, im, region, script, script_close)
    
    return template


"""
Read section of the INI file that describes clear_bag process.
It should contain images and scripts to deal with all necessary
situations on that screen
"""
def read_template_clear_bag(config, path):
    images = list()
    
    __get_templ_img(images, config, pgconst.TEMPLATE_CLEAR_BAG, path, "template_poke_ball_delete")
    __get_templ_img(images, config, pgconst.TEMPLATE_CLEAR_BAG, path, "template_razz_berry_delete")
    __get_templ_img(images, config, pgconst.TEMPLATE_CLEAR_BAG, path, "template_nanab_berry_delete")
    __get_templ_img(images, config, pgconst.TEMPLATE_CLEAR_BAG, path, "template_potion_delete")
    __get_templ_img(images, config, pgconst.TEMPLATE_CLEAR_BAG, path, "template_revive_delete")
    
    scripts = list()
    __get_templ_script(scripts, config, pgconst.TEMPLATE_CLEAR_BAG, "script_get_items_menu")
    __get_templ_script(scripts, config, pgconst.TEMPLATE_CLEAR_BAG, "script_items_scroll")
    __get_templ_script(scripts, config, pgconst.TEMPLATE_CLEAR_BAG, "script_items_delete")
    __get_templ_script(scripts, config, pgconst.TEMPLATE_CLEAR_BAG, "script_items_increase_amount")
    __get_templ_script(scripts, config, pgconst.TEMPLATE_CLEAR_BAG, "script_items_confirm_delete")
    __get_templ_script(scripts, config, pgconst.TEMPLATE_CLEAR_BAG, "script_close_menu")
    
    template = (images, scripts)
    
    return template

"""
Private method to simplify reading of the template images.
It does some basic checking and exits script if verification fails
"""
def __get_templ_img(result_list, config, section, path, name):
    tmp = cv2.imread(os.path.join(path, config.get(section, name)), 0)
    if tmp is not None:
        result_list.append(tmp)
    else:
        print "ERROR! can't read template: " + section + " " + name
        sys.exit()

"""
Private method to simplify reading of the template scripts.
It does some basic checking and exits script if verification fails
"""        
def __get_templ_script(result_list, config, section, name):
    fname = config.get(section, name)
    result_list.append(fname)

"""
Convenience function, it has to verify if current image is a main map of the game
Parameters:
    img - current screenshot
    templates - dictionary of populated templates
Returns:
    tuple (True/False, min_val, center, min_loc)
    where - True - if match was found/False - all other cases
    min_val - minimum value
    center - center of the identified minimum
    min_loc - top left corner of the identified minimum 
"""
def is_main_map(img, templates):
    r = match_template(img, templates[pgconst.TEMPLATE_MAIN_MAP][1], pgconst.MIN_RECOGNITION_VAL)
    return r

"""
Convenience function, it has to verify if current image is a main menu of the game
Parameters:
    img - current screenshot
    templates - dictionary of populated templates
Returns:
    tuple (True/False, min_val, center, min_loc)
    where - True - if match was found/False - all other cases
    min_val - minimum value
    center - center of the identified minimum
    min_loc - top left corner of the identified minimum
"""
def is_menu(img, templates):
    r = match_template(img, templates[pgconst.TEMPLATE_MENU][1], pgconst.MIN_RECOGNITION_VAL)
    return r

"""
Convenience function, it has to verify if current image is inside pokestop screen
Parameters:
    img - current screenshot
    templates - dictionary of populated templates
Returns:
    tuple (True/False, min_val, center, min_loc)
    where - True - if match was found/False - all other cases
    min_val - minimum value
    center - center of the identified minimum
    min_loc - top left corner of the identified minimum
"""
def is_inside_pokestop(img, templates):
    r = match_template(img, templates[pgconst.TEMPLATE_INSIDE_POKESTOP][1], pgconst.MIN_RECOGNITION_VAL)
    return r
    

def identify_screen(img, templates):
    r = is_main_map(img, templates)
    if r[0]:
        return (pgconst.SCREEN_MAIN_MAP, r)
    
    r = is_inside_pokestop(img, templates)
    if r[0]:
        return (pgconst.SCREEN_INSIDE_POKESTOP, r)
    
    r = is_menu(img, templates)
    if r[0]:
        return (pgconst.SCREEN_MAIN_MENU, r)
    
    return None


"""
Clear bag main function. It has to start from the main screen (map).
Parameters:
    items - mask of the items that needs to be deleted, see DEL_ITEMS_*
    templates - dictionary of populated templates
"""
def clear_bag(items, templates):
    print "started clear_bag process, item categories to delete: " + str(items)
    #Check if we are on the main screen
    img = get_screen_as_array()
                    
    if img is None:
        print "clear_bag Error! Can't capture the screen."
        return
    
    if not is_main_map(img, templates)[0]:
        print "clear_bag Error! wrong start screen."
        save_array_as_png(img, "/tmp/", "wrong_main_screen")
        return
    
    images = templates[pgconst.TEMPLATE_CLEAR_BAG][0]
    scripts = templates[pgconst.TEMPLATE_CLEAR_BAG][1]
    
    subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[0]])
    
    print "Checking items..."
    
    #check items in the loop using scroll
    for i in range(0,8):
        #should be initial items list screen
        img = get_screen_as_array()    
        
        resutls = is_items_visible(img, items, images)
        if resutls is not None:
            for r in resutls:
                #Remove detected item from the list of items
                items = items & (~r[0])
                
                #Click delete button for the given item, r[2][1] should give y of the center of the match region 
                subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[2], str(r[1][2][1])]) 
                
                #Click select how many items 
                subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[3]])
                
                #Remove double amount for pokeballs
                #if r[0] == pgconst.DEL_ITEMS_POKEYBALL:
                #    subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[3]])
                
                #Click confirm deletion 
                subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[4]])
                
                print "deleted item: " + str(r[0])
        
        #Exit if we already processed all selected items
        if items <= 0 :
            sleep(2)
            break
        
        #Scroll 
        subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[1]])
        
    #Exiting Items menu
    subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[5]])
    
    print "Finished clearing bag"
    
    return

"""
Convenience function, it has to verify if current image contains one of the
items that we want to delete from the bag
Parameters:
    img - current screenshot
    items - mask specifying which items we are checking
    images - template images
Returns:
    list of resutl matches - if at leas one match was found
    each element of the result is a tuple that consist of:
        - Index of the element that matched
        - original result from the match template function
    None - all other cases
"""
def is_items_visible(img, items, images):
    result = list()

    if items & pgconst.DEL_ITEMS_POKEYBALL:
        r = match_template(img, images[0], pgconst.MIN_RECOGNITION_VAL * 0.1)
        if r[0]:
            result.append((pgconst.DEL_ITEMS_POKEYBALL, r))
    
    if items & pgconst.DEL_ITEMS_RAZZ_BERRY:
        r = match_template(img, images[1], pgconst.MIN_RECOGNITION_VAL * 0.1)
        if r[0]:
            result.append((pgconst.DEL_ITEMS_RAZZ_BERRY, r))
        
    if items & pgconst.DEL_ITEMS_NANAB_BERRY:
        r = match_template(img, images[2], pgconst.MIN_RECOGNITION_VAL * 0.1)
        if r[0]:
            result.append((pgconst.DEL_ITEMS_NANAB_BERRY, r))
        
    if items & pgconst.DEL_ITEMS_POTION:
        r = match_template(img, images[3], pgconst.MIN_RECOGNITION_VAL * 0.1)
        if r[0]:
            result.append((pgconst.DEL_ITEMS_POTION, r))
        
    if items & pgconst.DEL_ITEMS_REVIVE:
        r = match_template(img, images[4], pgconst.MIN_RECOGNITION_VAL * 0.1)
        if r[0]:
            result.append((pgconst.DEL_ITEMS_REVIVE, r))
    
    if len(result) > 0:
        return result

    return None
    
"""
Convenience function, store array as image for later analysis
""" 
def save_array_as_png(img, path, file_name):
    png = Image.fromarray(img)
    tmp = file_name + "_" + str(int(time.time())) + '.png'
    f = os.path.join(path, tmp)
    png.save(f)
    print "Image saved: " + tmp
    return


"""
Generate coordinates for the touch events that have to happen
within some logical sector. Parameters:
    - center - (x, y) of the sector's center
    - r0 - what is the start radius of the sector - not dots close to the center then that value
    - r1 - what is the end radius of the sector, how far from center to go
    - a0 - start angle of the sector in degrees
    - a1 - end angle of the sector in degrees
Returns: list of the 9 dots coordinates. Each coordinate as (x,y) tuple
For example parameters: (100, 100), 50, 200, 0, 30, should generate 9 dots that are 'evenly' distributed in the sector
that has center at (100, 100), its radius is between 50 and 200 and sector starts from 0 degrees to 30 degrees.
""" 
def get_sector_dots(center, r0, r1, a0, a1):
    result = list()
    c = 3 #this is into how many logical circles we will be splitting sector into
    
    step = (r1 - r0) / c #length of the step
    da = a1 - a0 # total angle value 
    b = a0 + (da / 2) # this is bisector of the provided angle
    
    for i in range(0, c):
        #calculate first dot that resides on bisector  
        d = r0 + step * i #distance from the center
        dx = int(d * math.sin(math.radians(b)))
        dy = int(d * math.cos(math.radians(b)))
        dot = (center[0] + dx, center[1] - dy)
        result.append(dot) # new dot coordinates in the phones coordinate system

        #print ("i=%d, d=%d, dx=%d, dy=%d, a=%d, dot=(%d;%d)") % (i, d, dx, dy, b, dot[0], dot[1])
        
        if i == 0:
            continue
        
        #calculate dots that resides on bisector plus/minus some angle from bisector
        b1 = (da / i) / 2
        for j in range (1, i + 1):
            a = b - (b1 * j) # angle for given dot
            dx = int(d * math.sin(math.radians(a)))
            dy = int(d * math.cos(math.radians(a)))
            
            dot = (center[0] + dx, center[1] - dy)
            result.append(dot) # new dot coordinates in the phones coordinate system 
            
            #print ("j=%d, b1=%d, dx=%d, dy=%d, a=%d, dot=(%d;%d)") % (j, b1, dx, dy, a, dot[0], dot[1])
            
            a = b + (b1 * j)
            dx = int(d * math.sin(math.radians(a)))
            dy = int(d * math.cos(math.radians(a)))
            dot = (center[0] + dx, center[1] - dy)
            result.append(dot) # new dot coordinates in the phones coordinate system
            
            #print ("j=%d, b1=%d, dx=%d, dy=%d, a=%d, dot=(%d;%d)") % (j, b1, dx, dy, a, dot[0], dot[1])

    print result
                
    return result
    

    
def click_sector(templates, center, r0, r1, a0, a1):
    script = templates[pgconst.TEMPLATE_MAIN_MAP][3]
    
    #get dots within specified sector
    dots = get_sector_dots(center, r0, r1, a0, a1)
    
    #click selected dots
    for dot in dots:
        #Click delete button for the given item, r[2][1] should give y of the center of the match region 
        subprocess.call(['/usr/bin/adb', 'shell', 'sh', script, str(dot[0]), str(dot[1])])    
                        
                        
def click_donut(templates, center, r0, r1, count):
    da = 360/count #this is angle of each sector
    a0 = 0
    for i in range (0, count):
        a1 = a0 + da
        click_sector(templates, center, r0, r1, a0, a1)
        a0 = a1
        
        
def look_around(templates):
    #click around center
    click_donut(templates, (540, 960), 50, 500, 3)
    
    #get screen
    img = get_screen_as_array()
    
    #identify screen
    result = identify_screen(img, templates)
    
    #do actions based on the screen
    if result is None:
        #we got unknown scren, save it
        save_array_as_png(img, "/tmp", "unknown")
        
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
    
        
        
        
    