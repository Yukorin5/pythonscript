#!/usr/bin/env python

import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from astropy import units as u

from observational_data import *

#img = get_aia_image(193, datetime.datetime(2014,12,20,00,36))
img = get_aia_image(193, datetime.datetime(2014,12,19,23,00))


print "image shape = ", img.data.shape
print "exposure time = ", img.exposure_time
print "data type =",  type(img.data)

img.data = img.data / (img.exposure_time / u.second)

print "min pixel brightness = ", np.min(img.data)
print "max pixel brightness = ", np.max(img.data)


img.plot()
plt.colorbar()
plt.clim(0,10000)
plt.savefig('example-image.png')
