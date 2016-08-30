#!/usr/bin/env python

import datetime, subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from astropy import units as u

from observational_data import *

#img = get_aia_image(193, datetime.datetime(2014,12,20,00,36))


subprocess.call(['mkdir', '-p','frames'])

filenames = []

for i in range(60):
    t = datetime.datetime(2014,12,19,23,00) + datetime.timedelta(minutes=2*i)
    img = get_aia_image(193, t)

    print "image shape = ", img.data.shape
    print "exposure time = ", img.exposure_time
    print "data type =",  type(img.data)
    
    img.data = img.data / (img.exposure_time / u.second)
    
    print "min pixel brightness = ", np.min(img.data)
    print "max pixel brightness = ", np.max(img.data)
    
    
    img.plot()
    plt.colorbar()
    plt.clim(0,10000)
    filename = t.strftime('frames/%Y-%m-%d-%H-%M.png')
    plt.savefig(filename)

    filenames.append(filename)

subprocess.call(['convert','-delay','3'] + filenames + ['example-movie.mp4'])
