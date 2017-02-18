#!/bin/python
import Image, time
import numpy 

"""
Function that compares two images.
It subtracts region defined by diagonal p1, p2 from each image
and verify if regions are exactly the same in both images
"""
def img_compare(img1, img2, p1, p2):
    #crop images
    imc1 = img1.crop((p1[0], p1[1], p2[0], p2[1]))
    imc2 = img2.crop((p1[0], p1[1], p2[0], p2[1]))
    imc1.save('tests/1.png')
    imc2.save('tests/2.png')

    #convert images to 3D arrays    
    a1 = numpy.array(imc1)
    a2 = numpy.array(imc2)
    
    same = numpy.array_equal(a1, a2)
    return same


im1 = Image.open('tests/screen1.png')
im2 = Image.open('tests/screen2.png')
# w,h = im.size

x1 = [90, 1280]
x2 = [265, 1470]

same = img_compare(im1, im2, x1, x2)
print same


x1 = [90, 1080]
x2 = [265, 1270]

same = img_compare(im1, im2, x1, x2)
print same

