import cv2
import numpy as np

import os
import sys
import ast
from PIL import Image
import time
import math
import struct

from pg import pgconst
from pg import phoneSettings

"""
Verify if image contains template.
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
    __read_coord(config, "coords", pgconst.COORDS_EXIT_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_ITEMS_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_DELETE_ITEM, coords)
    __read_coord(config, "coords", pgconst.COORDS_DISCARD_PLUS_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_DISCARD_YES_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_CLOSE_ITEMS_MENU_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_LEAVE_CATCH_POKEMON_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_TOP_CP_POKEMON, coords)
    __read_coord(config, "coords", pgconst.COORDS_ANDROID_EXIT_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_ANDROID_HOME_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_ANDROID_BACK_BUTTON, coords)
    __read_coord(config, "coords", pgconst.COORDS_ANDROID_CLOSE_ALL_BUTTON, coords)
    
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
    __get_events_from_file(config, "swipes", path, pgconst.SCRIPT_ZOOM_OUT, scripts)
    
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
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_POKEY_STOP, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_EXIT_BUTTON, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_REVIVE_DELETE, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_POKE_BALL_DELETE, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_RAZZ_BERRY_DELETE, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_NANAB_BERRY_DELETE, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_POTION_DELETE, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_CATCH_POKEMON_OK_BUTTON, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_CATCH_POKEMON_STATS_SCREEN, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_GYM_MAIN_SCREEN, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_CATCH_POKEMON_SCREEN_DAY, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_CATCH_POKEMON_SCREEN_NIGHT, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_CATCH_POKEMON_SCREEN_DAY_SNOW, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_GYM_TOO_FAR, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_PASSENGER, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_EXIT_BUTTON_SHOP, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_EXIT_BUTTON_DARK, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_GYM_JOIN_BUTTON, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_POKEMONS_SELECTION, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_CONFIRM_GYM_YES_BUTTON, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_EXIT_YES_BUTTON, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_ANDROID_PHONE_ICON, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_ANDROID_PG_ICON, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_BATTLE_BUTTON, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_NO_POKEBALLS, templates)
    __get_templ_img(config, "templates", path, pgconst.TEMPLATE_BUY_EXTRA_POKEBALLS, templates)

    return templates

"""
Read all phone specific settings from the INI 
"""
def read_phone_settings(config):
    path = config.get("main", "path")
  
    coords = read_coords(config)
    scripts = read_scripts(config, path)
    templates = read_templates(config, path)
    
    ps = phoneSettings.PhoneSettings(coords, scripts, templates)
    
    skipPokemons = config.getboolean("main", "skipPokemons")
    ps.skipPokemons = skipPokemons

    clearBagCount = config.getint("main", "clearBagCount")
    ps.clearBagCount = clearBagCount
    
    zonesCount = config.getint("main", "zonesCount")
    ps.zonesCount = zonesCount
    
    dotsCount = config.getint("main", "dotsCount")
    ps.dotsCount = dotsCount
    
    zonesWidth = config.getint("main", "zonesWidth")
    ps.zonesWidth = zonesWidth
    
    zonesHeight = config.getint("main", "zonesHeight")
    ps.zonesHeight = zonesHeight
    
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
    min_val - 0 (not used in that method)
    center - 0 (not used in that method)
    min_loc - 0 (not used in that method)
"""
def is_inside_pokestop(img, ps):
    r = is_same_color_by_mask(img, ps.getTemplate(pgconst.TEMPLATE_POKEY_STOP))
    return r
    

def is_inside_gym(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_GYM_MAIN_SCREEN), pgconst.MIN_RECOGNITION_VAL)
    if not r[0]:
        r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_BATTLE_BUTTON), pgconst.MIN_RECOGNITION_VAL) 
    return r

def does_have_exit_button(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_EXIT_BUTTON), pgconst.MIN_RECOGNITION_VAL)
    if not r[0]:
        r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_EXIT_BUTTON_DARK), pgconst.MIN_RECOGNITION_VAL)
    return r

def is_catching_pokemon(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_CATCH_POKEMON_SCREEN_DAY), pgconst.MIN_RECOGNITION_VAL)
    if not r[0]: 
        r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_CATCH_POKEMON_SCREEN_NIGHT), pgconst.MIN_RECOGNITION_VAL)
    if not r[0]: 
        r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_CATCH_POKEMON_SCREEN_DAY_SNOW), pgconst.MIN_RECOGNITION_VAL)
    return r

def is_gym_too_far(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_GYM_TOO_FAR), pgconst.MIN_RECOGNITION_VAL)
    return r

def is_cougth_pokemon_popup(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_CATCH_POKEMON_OK_BUTTON), pgconst.MIN_RECOGNITION_VAL * 0.1)
    return r

def is_pokemon_stats_popup(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_CATCH_POKEMON_STATS_SCREEN), pgconst.MIN_RECOGNITION_VAL)
    return r

def is_passenger_popup(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_PASSENGER), pgconst.MIN_RECOGNITION_VAL)
    return r

def is_shop_screen(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_BUY_EXTRA_POKEBALLS), pgconst.MIN_RECOGNITION_VAL)
    return r

def is_no_pokeballs_screen(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_NO_POKEBALLS), pgconst.MIN_RECOGNITION_VAL)
    return r

def is_gym_join_button(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_GYM_JOIN_BUTTON), pgconst.MIN_RECOGNITION_VAL)
    return r

def is_pokemos_selection_screen(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_POKEMONS_SELECTION), pgconst.MIN_RECOGNITION_VAL * 0.01)
    return r

def is_gym_confirm_screen(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_CONFIRM_GYM_YES_BUTTON), pgconst.MIN_RECOGNITION_VAL)
    return r

def is_android_home_screen(img, ps):
    r = match_template(img, ps.getTemplate(pgconst.TEMPLATE_ANDROID_PHONE_ICON), pgconst.MIN_RECOGNITION_VAL)
    return r

"""
Tghat is very important function. It has to be able to identify display screen in different situations.
Ideally it should cover all possible situations.
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
def identify_screen(img, ps):
    r = is_main_map(img, ps)
    if r[0]:
        return (pgconst.SCREEN_MAIN_MAP, r)

    r = is_gym_join_button(img, ps)
    if r[0]:
        return (pgconst.SCREEN_HAS_GYM_JOIN, r)
    
    r = is_inside_gym(img, ps)
    if r[0]:
        return (pgconst.SCREEN_INSIDE_GYM, r)
    
    r = is_gym_too_far(img, ps)
    if r[0]:
        return (pgconst.SCREEN_GYM_TOO_FAR, r)
    
    r = is_inside_pokestop(img, ps)
    if r[0]:
        return (pgconst.SCREEN_INSIDE_POKESTOP, r)
    
    r = is_menu(img, ps)
    if r[0]:
        return (pgconst.SCREEN_MAIN_MENU, r)

    r = is_catching_pokemon(img, ps)
    if r[0]:
        return (pgconst.SCREEN_CATCHING_POKEMON, r)
    
    r = is_pokemon_stats_popup(img, ps)
    if r[0]:
        return (pgconst.SCREEN_POKEMON_STATS_POPUP, r)
    
    r = is_passenger_popup(img, ps)
    if r[0]:
        return (pgconst.SCREEN_PASSENGER, r)
    
    #Check if we are out of pokeballs
    r = is_no_pokeballs_screen(img, ps)
    if r[0]:
        return (pgconst.SCREEN_NO_POKEBALLS, r)
    
    #Check if we got to shop screen
    r = is_shop_screen(img, ps)
    if r[0]:
        return (pgconst.SCREEN_SHOP, r)
    
    
    #That check has to be the last as it is generic verification
    r = does_have_exit_button(img, ps)
    if r[0]:
        return (pgconst.SCREEN_HAS_EXIT_BUTTON, r)
    

    
    #Verify if application was stopped and we got to the android home screen
    r = is_android_home_screen(img, ps)
    if r[0]:
        return (pgconst.SCREEN_ANDROID_HOME, r)
    
    return None


"""
helper method to show which screen was detected
"""
def print_identified_screen(result):
    if result is None:
        print "screen is: NONE"
        return
    
    screen_id, r = result

    if screen_id == pgconst.SCREEN_MAIN_MAP: 
        print "screen is: SCREEN_MAIN_MAP"
    elif screen_id == pgconst.SCREEN_MAIN_MENU: 
        print "screen is: SCREEN_MAIN_MENU"
    elif screen_id == pgconst.SCREEN_INSIDE_POKESTOP: 
        print "screen is: SCREEN_INSIDE_POKESTOP";
    elif screen_id == pgconst.SCREEN_INSIDE_GYM: 
        print "screen is: SCREEN_INSIDE_GYM";
    elif screen_id == pgconst.SCREEN_HAS_EXIT_BUTTON: 
        print "screen is: SCREEN_HAS_EXIT_BUTTON";
    elif screen_id == pgconst.SCREEN_CATCHING_POKEMON: 
        print "screen is: SCREEN_CATCHING_POKEMON";
    elif screen_id == pgconst.SCREEN_CAUGTH_POKEMON_POPUP: 
        print "screen is: SCREEN_CAUGTH_POKEMON_POPUP";
    elif screen_id == pgconst.SCREEN_POKEMON_STATS_POPUP: 
        print "screen is: SCREEN_POKEMON_STATS_POPUP";
    elif screen_id == pgconst.SCREEN_GYM_TOO_FAR: 
        print "screen is: SCREEN_GYM_TOO_FAR";
    elif screen_id == pgconst.SCREEN_PASSENGER: 
        print "screen is: SCREEN_PASSENGER";
    elif screen_id == pgconst.SCREEN_SHOP: 
        print "screen is: SCREEN_SHOP";
    elif screen_id == pgconst.SCREEN_HAS_GYM_JOIN: 
        print "screen is: SCREEN_HAS_GYM_JOIN";
    elif screen_id == pgconst.SCREEN_POKEMONS_SELECTION: 
        print "screen is: SCREEN_POKEMONS_SELECTION";
    elif screen_id == pgconst.SCREEN_GYM_CONFIRM_BUTTON: 
        print "screen is: SCREEN_GYM_CONFIRM_BUTTON";
    elif screen_id == pgconst.SCREEN_ANDROID_HOME: 
        print "screen is: SCREEN_ANDROID_HOME";
    else: 
        print "screen is: UNKNOWN";
        
    return


"""
Handle catching pokemon situations function. It has to be able to identify display screen in different situations.
Ideally it should cover all possible situations.
Parameters:
    clientAndroid - client to handle Android requests
    ps - phone specific settings
Returns:
    tuple (True/False, min_val, center, min_loc)
    where - True - if match was found/False - all other cases
    min_val - minimum value
    center - center of the identified minimum
    min_loc - top left corner of the identified minimum
"""
def identify_catch_screen(clientAndroid, ps):
    img = clientAndroid.get_screen_as_array()
    
    r = is_cougth_pokemon_popup(img, ps)
    if r[0]:
        #save_array_as_png(img, ps.saveDir, "cougth_pokemon_popup_")
        return (pgconst.SCREEN_CAUGTH_POKEMON_POPUP, r)
    
    r = is_pokemon_stats_popup(img, ps)
    if r[0]:
        return (pgconst.SCREEN_POKEMON_STATS_POPUP, r)
    
    r = is_catching_pokemon(img, ps)
    if r[0]:
        return (pgconst.SCREEN_CATCHING_POKEMON, r)
    
    r = is_menu(img, ps)
    if r[0]:
        return (pgconst.SCREEN_MAIN_MENU, r)
    
    r = is_main_map(img, ps)
    if r[0]:
        return (pgconst.SCREEN_MAIN_MAP, r)
    
    r = is_no_pokeballs_screen(img, ps)
    if r[0]:
        return (pgconst.SCREEN_NO_POKEBALLS, r)
    
    #That check has to be the last as it is generic verification
    r = does_have_exit_button(img, ps)
    if r[0]:
        return (pgconst.SCREEN_HAS_EXIT_BUTTON, r)
    
    #That check has to be the last as it is generic verification
    r = is_shop_screen(img, ps)
    if r[0]:
        return (pgconst.SCREEN_SHOP, r)
    
    return None

"""
Handle process of joining to the gym. It has to be able to identify display screen in different situations.
Ideally it should cover all possible situations.
Parameters:
    clientAndroid - client to handle Android requests
    ps - phone specific settings
Returns:
    tuple (True/False, min_val, center, min_loc)
    where - True - if match was found/False - all other cases
    min_val - minimum value
    center - center of the identified minimum
    min_loc - top left corner of the identified minimum
"""
def identify_join_gym_screen(clientAndroid, ps):
    img = clientAndroid.get_screen_as_array()
    
    r = is_gym_join_button(img, ps)
    if r[0]:
        return (pgconst.SCREEN_HAS_GYM_JOIN, r)
    
    r = is_pokemos_selection_screen(img, ps)
    if r[0]:
        return (pgconst.SCREEN_POKEMONS_SELECTION, r)
    
    r = is_gym_confirm_screen(img, ps)
    if r[0]:
        return (pgconst.SCREEN_GYM_CONFIRM_BUTTON, r)
    
    r = does_have_exit_button(img, ps)
    if r[0]:
        return (pgconst.SCREEN_HAS_EXIT_BUTTON, r)
    
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
    
    if(not os.path.isdir(path)):
        os.makedirs(path)
        
    tmp = file_name + "_" + str(int(time.time())) + '.png'
    f = os.path.join(path, tmp)
    png.save(f)
    print "Image saved: " + tmp
    return


"""
Generate coordinates for the touch events that have to happen
within some logical sector. Parameters:
    - center - (x, y) of the sector's center
    - r0 - what is the start radius of the sector (there will no be any dot close to the center then that value)
    - r1 - what is the end radius of the sector, how far from center to go
    - a0 - start angle of the sector in degrees
    - a1 - end angle of the sector in degrees
Returns: list of the 9 dots coordinates. Each coordinate as (x,y) tuple
For example parameters: (100, 100), 50, 200, 0, 30, should generate 9 dots that are 'evenly' distributed in the sector
that has center at (100, 100), its radius is between 50 and 200 and sector starts from 0 degrees to 30 degrees.
""" 
def get_sector_dots(center, r0, r1, a0, a1):
    result = list()
    c = 4 #this is into how many logical circles we will be splitting sector into
    
    da = a1 - a0 # total angle value 
    b = a0 + (da / 2) # this is bisector of the provided angle
    density = 1
    scale = 1
    
    #adjust d for bottom and top sectors
    if b > 150 and b < 210:
        scale = scale * 0.8 # for the bottom is shorter
        density = int(density / 2) 
    
    if (b > 0 and b < 30) or (b > 330 and b < 360):
        scale = scale * 1.5 # for the top is longer
        density = int(density * 2)
        
    loops_count = int(c * scale)
    step = (r1 - r0) / loops_count #length of the step
    
    for i in range(0, loops_count):
        #calculate first dot that resides on bisector  
        d = (r0 + step * i) * scale #distance from the center
        
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

    #print "Got dots coordinates: " + result
                
    return result


"""
Generate coordinates for the touch events that have to happen
within some logical sector. Parameters:
    - center - (x, y) of the sector's center
    - r - radius of the circle
    - count - how many dots to generate
Returns: list of the dots coordinates
""" 
def get_circle_dots(center, r, count):
    result = list()
    
    b = int(360 / count)
    
    for i in range(0, b):
        dx = int(r * math.sin(math.radians(i * b)))
        dy = int(r * math.cos(math.radians(i * b)))
        dot = (center[0] + dx, center[1] - dy)
        result.append(dot) # new dot coordinates in the phones coordinate system

    return result

"""
Generate coordinates for the touch events that have to happen
within some logical rectangular. Parameters:
    - (x0, y0) bottom left corner of the rectangular
    - (x1, y1) top right corner of the rectangular
    - count - how many dots to generate over each axis
Returns: list of the dots coordinates
""" 
def get_rectangular_dots((x0, y0), (x1, y1), count):
    result = list()
    
    padX = int(((x1 - x0) / count) / 2) #half of the step 
    padY = int(((y0 - y1) / count) / 2) #half of the step
    stepX = int((x1 - x0) / count)
    stepY = int((y0 - y1) / count)
 
    x = x0 + padX  
    for i in range(0, count):
        y = y1 + padY
        for j in range(0, count):
            dot = (x, y)
            result.append(dot) # new dot coordinates in the phones coordinate system
            y = y + stepY
        x = x + stepX

    return result


"""
Generate coordinates for the touch events that have to happen
within some logical rectangular. Parameters:
    - (x0, y0) bottom left corner of the rectangular
    - (x1, y1) top right corner of the rectangular
    - count - how many zones to generate over each axis
Returns: list of the dots coordinates
""" 
def get_rectangular_zones((x0, y0), (x1, y1), count):
    result = list()
    
    stepX = int((x1 - x0) / (count))
    stepY = int((y0 - y1) / (count))
    
    x = x0
    for i in range(0, count):
        y = y1
        for j in range(0, count):
            zone = ((x, y + stepY), (x + stepX, y))
            result.append(zone) # new zone coordinates
            
            y = y + stepY
            
        x = x + stepX

    return result


"""
Sort generated dots based on the distance from center. Parameters:
    - center - center point of distribution
    - dots all generated dots
    - direction 1/2 - direction of the sorting (from/to center)
Returns: list of sorted dots
""" 
def sort_dots(center, dots, direction=1):
    #(math.pow((center[0] - tup[0]), 2) + math.pow((center[1] - tup[1]), 2))
    if direction == 1:
        dots.sort(key=lambda tup: (math.pow((center[0] - tup[0]), 2) + math.pow((center[1] - tup[1]), 2)), reverse=False)
    else:
        dots.sort(key=lambda tup: (math.pow((center[0] - tup[0]), 2) + math.pow((center[1] - tup[1]), 2)), reverse=True)
        
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

"""
Verify if all pixels specified by maskImg have save color
    - img - image to test
    - imgMask - image in the form of B/W mask - only non Black pixes will be checked for color
Returns: 
    - True if all pixels specified by non Black mask have same color
    - True if pixels for a smooth gradient, delta in color is less then 2
"""         
def is_same_color_by_mask(img, imgMask):
    if len(img.shape) != 2:
        print "WARNING! wrong image shape: " + str(img.shape)
        return
    
    # set all pixels marked by black color of the mask to zero 
    c = np.bitwise_and(img, imgMask)
    if len(c.shape) != 2:
        print "WARNING! wrong image mask shape: " + str(c.shape)
        return
    
    # extract all non zero pixels from the original image
    e = np.extract(c, img)
    if e is not None and len(e.shape) != 1:
        print "WARNING! wrong non zero pixels matrix: " + str(e.shape)
        return    
    
    # calculate average of the non zero pixels
    av = np.average(e)
    
    # image considered to have same color if average of non zero elements is equual to the first pixel
    if e[0] == int(av):
        return (True, 0, 0, 0);
    
    # next let's check if colors in the image form a smooth gradient
    # get unique numbers
    u = np.unique(e, return_counts=True)
    
    # if there are more then 10 color variations return false
    if np.size(u[0]) > 10:
        return (False, np.size(u[0]), np.min(u[0]), np.max(u[0]));
    
    # check if numbers differ for more then 2
    c0 = u[0][0]
    isGradient = True
    for color in u[0]:
        if color - c0 > 2:
            isGradient = False
            break
        c0 = color
        
    if isGradient:
        return (True, np.size(u[0]), np.min(u[0]), np.max(u[0]));
        
    return (False, np.size(u[0]), np.min(u[0]), np.max(u[0]));


"""
Crop image 
    - img - image to test
    - skipTop - how many pixels skip on the top
    - skipBottom - how many pixels skip on the bottom
    - skipLeft - how many pixels skip on the left
    - skipRight - how many pixels skip on the right
Returns: 
    - cropped image
"""
def crop(img, skipTop, skipBottom, skipLeft=0, skipRight=0):
    (h, w) = np.shape(img)
    a = img[skipTop:h - skipBottom, skipLeft:w - skipRight]
    return a

