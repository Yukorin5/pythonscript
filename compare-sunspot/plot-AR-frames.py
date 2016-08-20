#!/usr/bin/env python
import datetime, StringIO, urllib, sys, subprocess,os,math,glob
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

out_path = "f-{}-{}-{}/".format(img_type, ar_no, int(cadence.total_seconds()))
subprocess.call(["mkdir", "-p", out_path])


omega = 2 * math.pi  / 28 / 86400

if ar_no == 12135:
    time_begin=datetime.datetime(2014,8,5)
    time_end=datetime.datetime(2014,8,19)
    Ax = 900
    Ay = 100
    x0 = 0
    y0 = 200
    t0 = datetime.datetime(2014,8,11,15,46)
    data_path_head = "b-"
elif ar_no == 12297:
    time_begin=datetime.datetime(2015,3,4)
    time_end=datetime.datetime(2015,3,21)
    Ax = 850
    Ay = 120
    x0 = 0
    y0 = -180
    t0 = datetime.datetime(2015,3,13,1,22)
    data_path_head = "d-"
else:
    print "unknown AR #", ar_no
    exit(1)

t = time_begin - cadence
frame_ctr = -1
while True:
    t += cadence
    frame_ctr += 1
    if t >= time_end:
        exit(0)

    if img_type == "hmi":
        fn ="{}hmi/hmi.M_720s.{}_TAI.6173.0.magnetogram.fits".format(
            data_path_head, t.strftime("%Y%m%d_%H%M%S"))
    elif img_type == "aia94":
        fn = "{}aia/aia.lev1_euv_12s.{}??Z.94.image_lev1.fits".format(
            data_path_head, t.strftime("%Y-%m-%dT%H%M"))
    elif img_type == "aia193":
        fn = "{}aia/aia.lev1_euv_12s.{}??Z.193.image_lev1.fits".format(
            data_path_head, t.strftime("%Y-%m-%dT%H%M"))
    else:
        print "unknown image type: ", fn
        exit(0)
    fn = glob.glob(fn)[0]


    print "open file; " , fn
    fullmap = sunpy.map.Map(fn)

    length = 250 * u.arcsec
    t_i = (t-t0).total_seconds()
    x = u.arcsec * (Ax * math.cos(omega * t_i + 1.5*math.pi) + x0)
    y = u.arcsec * (Ay * math.cos(omega * t_i + 1.5*math.pi) + y0)

    # Create a SunPy Map, and a second submap over the region of interest.

    img = fullmap.submap(u.Quantity([x - length, x + length]),
                         u.Quantity([y - length, y + length]))


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
        plt.clim(-200,200)
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()
    elif img_type=='aia193':
        plt.clim(0,3000)
    elif img_type=='aia94':
        plt.clim(0,100)

    out_fn = out_path + "/{:08}.png".format(frame_ctr)

    plt.savefig(out_fn)
    plt.close('all')
