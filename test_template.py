import cv2
from matplotlib import pyplot as plt
import datetime
import glob, os

score = 0

def check_image(image, template):
    global score
    img = cv2.imread(image, 0)
    w, h = template.shape[::-1]
    
    method = cv2.TM_SQDIFF_NORMED
    #method = cv2.TM_SQDIFF
    
    t0 = datetime.datetime.now()
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    t1 = datetime.datetime.now()
    i = image.find("inside-pokestop")
    if i >= 0:
        if min_val < 0.01:
            print ("OK   min_val=%.6f, min_loc=(%04d,%04d), time=%s, file: %s" % (min_val, min_loc[0], min_loc[1], str(t1 - t0), image))
        else:
            print ("FAIL min_val=%.6f, min_loc=(%04d,%04d), time=%s, file: %s" % (min_val, min_loc[0], min_loc[1], str(t1 - t0), image))
            score = score + 1
    else:
        if min_val < 0.01:
            print ("FAIL min_val=%.6f, min_loc=(%04d,%04d), time=%s, file: %s" % (min_val, min_loc[0], min_loc[1], str(t1 - t0), image))
            score = score + 1
        else:
            print ("OK   min_val=%.6f, min_loc=(%04d,%04d), time=%s, file: %s" % (min_val, min_loc[0], min_loc[1], str(t1 - t0), image))
            
template = cv2.imread('tests/31d53011/pokey_stop_button.png', 0)

path = "tests/31d53011/screens/"
#path = "tests/d0b760087cf3/"
 
for file in os.listdir(path):
    check_image(os.path.join(path, file), template)

print "score=%d" % score

# All the 6 methods for comparison in a list
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# methods = ['cv2.TM_SQDIFF_NORMED']
# 
# for meth in methods:
#     t0 = datetime.datetime.now()
#     img = img2.copy()
#     method = eval(meth)
# 
#     # Apply template Matching
#     res = cv2.matchTemplate(img,template,method)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
# 
#     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
#     if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#         top_left = min_loc
#     else:
#         top_left = max_loc
#     bottom_right = (top_left[0] + w, top_left[1] + h)
#     
#     print (min_val, min_loc)
# 
# #     cv2.rectangle(img,top_left, bottom_right, 255, 2)
# # 
# #     plt.subplot(121),plt.imshow(res,cmap = 'gray')
# #     plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
# #     plt.subplot(122),plt.imshow(img,cmap = 'gray')
# #     plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
# #     plt.suptitle(meth)
#     
#     t1 = datetime.datetime.now()
#     print("Matching time: " + str(t1 - t0))
# 
# #     plt.show()