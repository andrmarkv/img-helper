import datetime
import os
from PIL import Image
import numpy as np
from pg import pgutil

score = 0;
MIN_RECOGNITION_VAL = 0.01; #if we get below that value indicates that we found template
count = 0

def check_image(img, template):
    global score
    global count
    
    t0 = datetime.datetime.now()
    
    r = pgutil.match_template(img, template, MIN_RECOGNITION_VAL)
    
    t1 = datetime.datetime.now()
    result = (r[1], r[2][0], r[2][1], str(t1 - t0));
            
    return result

template = np.array(Image.open('../conf/redmi3_720_1280/template_pokeyball_map_screen1.png').convert('L'))            

image = np.array(Image.open('/tmp/wrong_main_screen_1498591220.png'))

results = list();

result = check_image(image, template);

print result

#print ("OK   min_val=%.6f, min_loc=(%04d,%04d), time=%s, file: %s" % (min_val, min_loc[0], min_loc[1], str(t1 - t0), image))