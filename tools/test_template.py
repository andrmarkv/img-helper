import cv2
from matplotlib import pyplot as plt
import datetime
import glob, os

score = 0;
MIN_RECOGNITION_VAL = 0.01; #if we get below that value indicates that we found template

def check_image(image, template):
    global score
    
    t0 = datetime.datetime.now()
    
    img = cv2.imread(image, 0)
    w, h = template.shape[::-1]
    
    method = cv2.TM_SQDIFF_NORMED
    #method = cv2.TM_SQDIFF
    
    result = None;
    
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    t1 = datetime.datetime.now()
    i = image.find("inside-pokestop")
    if i >= 0:
        if min_val < MIN_RECOGNITION_VAL:
            result = (min_val, min_loc[0], min_loc[1], str(t1 - t0), image, 'OK');
            print ("OK   min_val=%.6f, min_loc=(%04d,%04d), time=%s, file: %s" % (min_val, min_loc[0], min_loc[1], str(t1 - t0), image))
        else:
            result = (min_val, min_loc[0], min_loc[1], str(t1 - t0), image, 'FAIL');
            print ("FAIL min_val=%.6f, min_loc=(%04d,%04d), time=%s, file: %s" % (min_val, min_loc[0], min_loc[1], str(t1 - t0), image))
            score = score + 1
    else:
        if min_val < MIN_RECOGNITION_VAL:
            result = (min_val, min_loc[0], min_loc[1], str(t1 - t0), image, 'FAIL');
            print ("FAIL min_val=%.6f, min_loc=(%04d,%04d), time=%s, file: %s" % (min_val, min_loc[0], min_loc[1], str(t1 - t0), image))
            score = score + 1
        else:
            result = (min_val, min_loc[0], min_loc[1], str(t1 - t0), image, 'OK');
            print ("OK   min_val=%.6f, min_loc=(%04d,%04d), time=%s, file: %s" % (min_val, min_loc[0], min_loc[1], str(t1 - t0), image))
            
    return result
            
template = cv2.imread('../tests/31d53011/pokey_stop_button.png', 0)
#template = cv2.imread('tests/31d53011/pokeydex_button_menu.png', 0)
#template = cv2.imread('tests/31d53011/pokeyball_map_screen.png', 0)

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