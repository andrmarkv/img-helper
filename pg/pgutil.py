import cv2

import os
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
Convenience function, it has to verify if current image is a main map of the game
Parameters:
    img - current screenshot
    templates - dictionary of populated templates
Returns:
    True - if match was found
    False - all other cases
"""
def is_main_map(img, templates):
    r = match_template(img, templates[pgconst.TEMPLATE_MAIN_MAP], pgconst.MIN_RECOGNITION_VAL)
    if r[0]:
        return True
    
    return False

"""
Convenience function, it has to verify if current image is a main menu of the game
Parameters:
    img - current screenshot
    templates - dictionary of populated templates
Returns:
    True - if match was found
    False - all other cases
"""
def is_menu(img, templates):
    r = match_template(img, templates[pgconst.TEMPLATE_MENU], pgconst.MIN_RECOGNITION_VAL)
    if r[0]:
        return True
    
    return False


"""
Convenience function, it has to verify if current image is inside pokestop screen
Parameters:
    img - current screenshot
    templates - dictionary of populated templates
Returns:
    True - if match was found
    False - all other cases
"""
def is_inside_pokestop(img, templates):
    r = match_template(img, templates[pgconst.TEMPLATE_INSIDE_POKESTOP], pgconst.MIN_RECOGNITION_VAL)
    if r[0]:
        return True
    
    return False
