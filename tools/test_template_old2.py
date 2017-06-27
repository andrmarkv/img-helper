import cv2
from matplotlib import pyplot as plt
import datetime
import glob, os
from PIL import Image
import numpy as np
from pg import pgutil

score = 0;
MIN_RECOGNITION_VAL = 0.01; #if we get below that value indicates that we found template
count = 0

def check_image(image, template):
    global score
    global count
    
    t0 = datetime.datetime.now()
    
    img = np.array(Image.open(image).convert('L'))
    
    r = pgutil.match_template(img, template, MIN_RECOGNITION_VAL)
    
    t1 = datetime.datetime.now()
    i = image.find("inside-pokestop")
    if i >= 0:
        if r[0] :
            result = (r[1], r[2][0], r[2][1], str(t1 - t0), image, 'OK');
        else:
            result = (r[1], r[2][0], r[2][1], str(t1 - t0), image, 'FAIL');
            score = score + 1
    else:
        if r[0]:
            result = (r[1], r[2][0], r[2][1], str(t1 - t0), image, 'FAIL');
            score = score + 1
        else:
            result = (r[1], r[2][0], r[2][1], str(t1 - t0), image, 'OK');
    
    count = count + 1        
    print 'processed: ' + str(count)
            
    return result
            
#template = cv2.imread('tests/31d53011/pokey_stop_button.png', 0)
#template = cv2.imread('tests/31d53011/pokeydex_button_menu.png', 0)
#template = cv2.imread('tests/31d53011/pokeyball_map_screen.png', 0)
template = np.array(Image.open('../tests/31d53011/pokey_stop_button.png').convert('L'))

path = "../tests/31d53011/screens/"
#path = "tests/d0b760087cf3/"
#path = "tests/081b350300edbe7c/"

results = list();

for file in os.listdir(path):
    result = check_image(os.path.join(path, file), template);
    if (result != None):
        results.append(result)

print "score=%d" % score

results.sort()

for r in results:
    print r
    #print ("OK   min_val=%.6f, min_loc=(%04d,%04d), time=%s, file: %s" % (min_val, min_loc[0], min_loc[1], str(t1 - t0), image))