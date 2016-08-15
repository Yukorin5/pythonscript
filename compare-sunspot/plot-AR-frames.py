#!/usr/bin/env python
import datetime, StringIO, urllib, sys, subprocess,os,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab
import numpy as np
from astropy.io import fits
from astropy import units as u

import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import sunpy.map


img_type = sys.argv[1]
ar_no = int(sys.argv[2])
cadence = datetime.timedelta(seconds = int(sys.argv[3]))

omega = 2 * math.pi  / 28 / 86400

if ar_no == 12135:
    time_begin=datetime.datetime(2014,8,5)
    time_end=datetime.datetime(2014,8,5)
    Ax = 900
    Ay = 100
    x0 = 0
    y0 = 200
    t0 = datetime.datetime(2014,8,11,15,46)
elif ar_no == 12297:
    time_begin=datetime.datetime(2015,3,4)
    time_end=datetime.datetime(2015,3,21)
    Ax = 850
    Ay = 120
    x0 = 0
    y0 = -300
    t0 = datetime.datetime(2015,3,13,1,22)
else:
    print "unknown AR #", ar_no
    exit(1)

t = t0 - cadence
frame_ctr = -1
while True:
    t += cadence
    frame_ctr += 1
    if t >= time_end:
        exit(0)


    fnbody,ext = os.path.splitext(fn)

    if '193.image' in fn:
        img_type = 'aia193'
    elif '94.image' in fn:
        img_type = 'aia94'
    elif 'hmi' in fn:
        img_type = 'hmi'
    else:
        print "Unknown image type:" , fn
        exit(0)


    fullmap = sunpy.map.Map(fn)

    length = 250 * u.arcsec
    x0 = -700 * u.arcsec
    y0 = -250 * u.arcsec

    # Create a SunPy Map, and a second submap over the region of interest.

    img = fullmap.submap(u.Quantity([x0 - length, x0 + length]),
                         u.Quantity([y0 - length, y0 + length]))


    print img.data.shape
    print "dt = ", img.exposure_time
    print type(img.data)


    #img.data = img.data / (img.exposure_time / u.second)

    if img_type=='hmi':
        pass
    elif img_type=='aia193':
        img.data = img.data / (img.exposure_time / u.second)
    elif img_type=='aia94':
        img.data = img.data / (img.exposure_time / u.second)
    print np.nanmin(img.data)
    print np.nanmax(img.data)


    #pylab.rcParams['figure.figsize'] = (6.4,6.4)



    img.plot()
    plt.colorbar()
    if img_type=='hmi':
        plt.clim(-300,300)
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()
    elif img_type=='aia193':
        plt.clim(0,3000)
    elif img_type=='aia94':
        plt.clim(0,100)

    plt.savefig(img_type + '.png')
    plt.close('all')
