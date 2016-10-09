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
counter = 0

#time_begin = datetime.datetime(2014,12,18,00,00)
#time_end   = datetime.datetime(2014,12,21,00,00)
time_begin = datetime.datetime(2013,11,04,00,00)
time_end   = datetime.datetime(2013,11,07,00,00)

t = time_begin

while True:
    t += datetime.timedelta(minutes=2)
    if t > time_end:
        break

    img = get_aia_image(193, t)
    if img is None:
        continue

    print "image shape = ", img.data.shape
    print "exposure time = ", img.exposure_time
    print "data type =",  type(img.data)
    
    img.data = img.data / (img.exposure_time / u.second)
    
    print "min pixel brightness = ", np.min(img.data)
    print "max pixel brightness = ", np.max(img.data)
    
    
    img.plot()
    plt.colorbar()
    plt.clim(0,10000)
    filename = 'frames/{:08}.png'.format(counter)
    counter+=1
    plt.savefig(filename)

    filenames.append(filename)
    plt.close('all')

subprocess.call('ffmpeg -y -r 24 -i frames/%08d.png -qscale 0 example-movie.mp4', shell=True)
