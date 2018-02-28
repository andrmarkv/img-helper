#!/usr/bin/python

import datetime
import os
import sys
from PIL import Image
import numpy as np
sys.path.append('../')
from pg import pgutil

score = 0;
MIN_RECOGNITION_VAL = 0.01; #if we get below that value indicates that we found template
count = 0

def check_image(img, template):
    t0 = datetime.datetime.now()
    
    r = pgutil.is_same_color_by_mask(img, template)
    
    t1 = datetime.datetime.now()
    result = (r, str(t1 - t0));
            
    return result


if (len(sys.argv) < 3):
    print "please specify template_mask_file and test_file"
    sys.exit(1) 


#template = np.array(Image.open('../conf/redmi3_720_1280/template_pokeyball_map_screen1.png').convert('L'))            
template = np.array(Image.open(sys.argv[1]).convert('L'))

image = np.array(Image.open(sys.argv[2]))
if (len(image.shape) == 3):
    image = np.array(Image.open(sys.argv[2]).convert('L'))

results = list();

result = check_image(image, template);

print result

#print ("OK   min_val=%.6f, min_loc=(%04d,%04d), time=%s, file: %s" % (min_val, min_loc[0], min_loc[1], str(t1 - t0), image))