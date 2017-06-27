import cv2

import os
import sys
import ast
import subprocess
from PIL import Image
import time
import math
import struct

from pg import pgconst
from time import sleep

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
Private helper method to read one coord value from the INI file
"""
def __read_coord(config, section, name, coords):
    tmp = config.get(section, name)
    coord = ast.literal_eval(tmp)
    coords[name] = coord

"""
Read coords section of the INI file
"""
def read_coords(config):
    coords = dict()
    
    __read_coord(config, "coords", pgconst.COORDS_CENTER, coords)
    __read_coord(config, "coords", pgconst.COORDS_MAIN_MENU_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_CLOSE_POKE_STOP, coords)
    __read_coord(config, "coords", pgconst.COORDS_ITEMS_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_DELETE_ITEM, coords)
    __read_coord(config, "coords", pgconst.COORDS_DISCARD_PLUS_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_DISCARD_YES_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_CLOSE_ITEMS_MENU_BUTTON, coords)
    
    return coords

"""
Private method to simplify reading of the swipe events.
It does some basic checking and exits script if verification fails
"""        
def __get_events_from_file(config, section, path, name, scripts):
    fname = os.path.join(path, config.get(section, name))
    buf = get_events_from_file(fname)
    scripts[name] = buf

"""
Read section of the INI file that swite scriipts.
"""
def read_scripts(config, path):
    scripts = dict()
    
    __get_events_from_file(config, "swipes", path, pgconst.SCRIPT_SWIPE_POKESTOP, scripts)
    __get_events_from_file(config, "swipes", path, pgconst.SCRIPT_THROW_BALL_NORMAL, scripts)
    __get_events_from_file(config, "swipes", path, pgconst.SCRIPT_THROW_BALL_LONG, scripts)
    __get_events_from_file(config, "swipes", path, pgconst.SCRIPT_THROW_BALL_SHORT, scripts)
    __get_events_from_file(config, "swipes", path, pgconst.SCRIPT_SCROLL_ITEMS, scripts)
    
    return scripts

"""
Private method to simplify reading of the template images.
It does some basic checking and exits script if verification fails
"""
def __get_templ_img(config, section, path, name, images):
    fname = os.path.join(path, config.get(section, name))
    tmp = cv2.imread(fname, 0)
    if tmp is not None:
        images[name] = tmp
    else:
        print "ERROR! can't read template: " + section + " " + name
        sys.exit()


"""
Read section of the INI file that describes image templates.
"""
def read_templates(config, path):
    templates = dict()
    
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_POKEYDEX_BUTTON_MENU, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_POKEYBALL_MAP_SCREEN, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_POKEY_STOP_BUTTON, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_POKE_BALL_DELETE, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_RAZZ_BERRY_DELETE, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_NANAB_BERRY_DELETE, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_POTION_DELETE, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_REVIVE_DELETE, templates)
    
    return templates

"""
Convenience function, it has to verify if current image is a main map of the game
Parameters:
    img - current screenshot
    ps - phone specific settings
Returns:
    tuple (True/False, min_val, center, min_loc)
    where - True - if match was found/False - all other cases
    min_val - minimum value
    center - center of the identified minimum
    min_loc - top left corner of the identified minimum 
"""
def is_main_map(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_POKEYBALL_MAP_SCREEN), pgconst.MIN_RECOGNITION_VAL)
    return r

"""
Convenience function, it has to verify if current image is a main menu of the game
Parameters:
    img - current screenshot
    ps - phone specific settings
Returns:
    tuple (True/False, min_val, center, min_loc)
    where - True - if match was found/False - all other cases
    min_val - minimum value
    center - center of the identified minimum
    min_loc - top left corner of the identified minimum
"""
def is_menu(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_POKEYDEX_BUTTON_MENU), pgconst.MIN_RECOGNITION_VAL)
    return r

"""
Convenience function, it has to verify if current image is inside pokestop screen
Parameters:
    img - current screenshot
    ps - phone specific settings
Returns:
    tuple (True/False, min_val, center, min_loc)
    where - True - if match was found/False - all other cases
    min_val - minimum value
    center - center of the identified minimum
    min_loc - top left corner of the identified minimum
"""
def is_inside_pokestop(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_POKEY_STOP_BUTTON), pgconst.MIN_RECOGNITION_VAL)
    return r
    

def identify_screen(img, ps):
    r = is_main_map(img, ps)
    if r[0]:
        return (pgconst.SCREEN_MAIN_MAP, r)
    
    r = is_inside_pokestop(img, ps)
    if r[0]:
        return (pgconst.SCREEN_INSIDE_POKESTOP, r)
    
    r = is_menu(img, ps)
    if r[0]:
        return (pgconst.SCREEN_MAIN_MENU, r)
    
    return None

"""
Convenience function, it has to verify if current image contains one of the
items that we want to delete from the bag
Parameters:
    img - current screenshot
    items - mask specifying which items we are checking
    ps - phone specific settings
Returns:
    list of resutl matches - if at leas one match was found
    each element of the result is a tuple that consist of:
        - Index of the element that matched
        - original result from the match template function
    None - all other cases
"""
def is_items_visible(img, items, ps):
    result = list()

    if items & pgconst.DEL_ITEMS_POKEYBALL:
        r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_POKE_BALL_DELETE), pgconst.MIN_RECOGNITION_VAL * 0.1)
        if r[0]:
            result.append((pgconst.DEL_ITEMS_POKEYBALL, r))
    
    if items & pgconst.DEL_ITEMS_RAZZ_BERRY:
        r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_RAZZ_BERRY_DELETE), pgconst.MIN_RECOGNITION_VAL * 0.1)
        if r[0]:
            result.append((pgconst.DEL_ITEMS_RAZZ_BERRY, r))
        
    if items & pgconst.DEL_ITEMS_NANAB_BERRY:
        r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_NANAB_BERRY_DELETE), pgconst.MIN_RECOGNITION_VAL * 0.1)
        if r[0]:
            result.append((pgconst.DEL_ITEMS_NANAB_BERRY, r))
        
    if items & pgconst.DEL_ITEMS_POTION:
        r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_POTION_DELETE), pgconst.MIN_RECOGNITION_VAL * 0.1)
        if r[0]:
            result.append((pgconst.DEL_ITEMS_POTION, r))
        
    if items & pgconst.DEL_ITEMS_REVIVE:
        r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_REVIVE_DELETE), pgconst.MIN_RECOGNITION_VAL * 0.1)
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
        
def get_events_from_file(file_name):
    buf = ''
    f = open(file_name, 'r')
    lcount = 0
    
    
    for line in f:
        if len(line) <= 3:
            continue
        tokens = line.split(' ')

        if len(tokens) != 3:
            print "Got wrong line: " + line
            continue
        
        lcount = lcount + 1
                    
        for t in tokens:
            v = int(t.rstrip(), 16)
            u32 = v % 2**32
            buf = buf + struct.pack("<I", u32)
    
    f.close()
    
    print('lcount: %d, bufLen: %d') % (lcount, len(buf))
    
    return buf        
        
    