"""
=================
Template Matching
=================

In this example, we use template matching to identify the occurrence of an
image patch (in this case, a sub-image centered on a single coin). Here, we
return a single match (the exact same coin), so the maximum value in the
``match_template`` result corresponds to the coin location. The other coins
look similar, and thus have local maxima; if you expect multiple matches, you
should use a proper peak-finding function.

The ``match_template`` function uses fast, normalized cross-correlation [1]_
to find instances of the template in the image. Note that the peaks in the
output of ``match_template`` correspond to the origin (i.e. top-left corner) of
the template.

.. [1] J. P. Lewis, "Fast Normalized Cross-Correlation", Industrial Light and
       Magic.

"""
import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.feature import match_template
from skimage.color import rgb2gray

import os
from skimage.color.colorconv import rgb2grey

cur_dir = os.path.dirname(os.path.realpath(__file__)) + "/"


def img_cut(img, p1, p2):
    #crop images
    imc = img.crop((p1[0], p1[1], p2[0], p2[1]))
    imc.save('/tmp/1.png')

    #convert images to 3D arrays    
    a = np.array(imc)
    
    return a

coin = data.load(cur_dir + "tests/img1.png")
coin = rgb2gray(coin)
#image = data.load(cur_dir + "tests/31d53011/screen_1487610589.png")
#image = data.load(cur_dir + "tests/d0b760087cf3/screen2.png")
#image = data.load(cur_dir + "tests/31d53011/captured-pokemon.png")
image = data.load(cur_dir + "tests/31d53011/capture-screen.png")


image = rgb2grey(image)

result = match_template(image, coin)
ij = np.unravel_index(np.argmax(result), result.shape)
x, y = ij[::-1]


fig = plt.figure(figsize=(8, 3))
ax1 = plt.subplot(1, 3, 1)
ax2 = plt.subplot(1, 3, 2, adjustable='box-forced')
ax3 = plt.subplot(1, 3, 3, sharex=ax2, sharey=ax2, adjustable='box-forced')

ax1.imshow(coin)
ax1.set_axis_off()
ax1.set_title('template')

ax2.imshow(image)
ax2.set_axis_off()
ax2.set_title('image')
# highlight matched region
hcoin, wcoin = coin.shape
rect = plt.Rectangle((x, y), wcoin, hcoin, edgecolor='r', facecolor='none')
ax2.add_patch(rect)

ax3.imshow(result)
ax3.set_axis_off()
ax3.set_title('`match_template`\nresult')
# highlight matched region
ax3.autoscale(False)
ax3.plot(x, y, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)

plt.show()
