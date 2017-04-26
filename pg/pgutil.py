import cv2

import os
import sys
import ast
import subprocess
import StringIO
from PIL import Image
import numpy as np

from pg import pgconst

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
    
    __get_templ_img(images, config, pgconst.TEMPLATE_CLEAR_BAG, path, "template_potion_delete")
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
        r[0]=pgconst.SCREEN_MAIN_MAP
        return r
    
    r = is_inside_pokestop(img, templates)
    if r[0]:
        r[0]=pgconst.SCREEN_MAIN_MAP
        return r
    
    r = is_menu(img, templates)
    if r[0]:
        r[0]=pgconst.SCREEN_MAIN_MENU
        return r
    
    return None


"""
Clear bag main function. It has to start from the main screen (map).
Parameters:
    items - mask of the items that needs to be deleted, see DEL_ITEMS_*
    templates - dictionary of populated templates
"""
def clear_bag(items, templates):
    #Check if we are on the main screen
    img = get_screen_as_array()
                    
    if img is None:
        print "clear_bag Error! Can't capture the screen."
        return
    
    if is_main_map(img, templates)[0]:
        print "clear_bag Error! wrong start screen."
        return
    
    images = templates[pgconst.TEMPLATE_CLEAR_BAG][0]
    scripts = templates[pgconst.TEMPLATE_CLEAR_BAG][1]
    
    subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[0]])
    
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
                subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[2]], str(r[2][1])) 
                
                #Click select how many items 
                subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[3]])
                
                #Click confirm deletion 
                subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[4]])
        
        #Scroll 
        subprocess.call(['/usr/bin/adb', 'shell', 'sh', scripts[1]])
    

"""
Convenience function, it has to verify if current image contains one of the
items that we want to delete from the bag
Parameters:
    img - current screenshot
    items - mask specifying which items we are checking
    images - template images
Returns:
    list of resutl matches - if at leas one match was found
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
    