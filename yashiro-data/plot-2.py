#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import sunpy.io.fits as fits
from sunpy.cm import color_tables as ct
import sunpy.wcs as wcs
import datetime
import os
import sys


# t = Time('2014-10-21T00:00:00',format='isot',scale="tai")

t = datetime.datetime(2014,10,21,0,0)
frame_ctr=-1

while t < datetime.datetime(2014,10,28,0,0):
    t += datetime.timedelta(minutes=12)

    print(t)
    fn_aia = "cdaw.gsfc.nasa.gov/pub/yashiro/misc/.muranushi/12192/aia/aia.sharp_cea_720s.{:04}{:02}{:02}_{:02}{:02}_0094.fits".format(t.year, t.month, t.day, t.hour, t.minute)
    fn_hmi = "cdaw.gsfc.nasa.gov/pub/yashiro/misc/.muranushi/12192/hmi/hmi.sharp_cea_720s.{:04}{:02}{:02}_{:02}{:02}00_TAI.Br.fits".format(t.year, t.month, t.day, t.hour, t.minute)
    if (not os.path.exists(fn_aia)):
        continue
    if (not os.path.exists(fn_hmi)):
        continue

    frame_ctr+=1

    data = fits.read(fn_hmi)
    img = data[1][0]

    plt.title("HMI + AIA94 {}".format(t))
    plt.imshow(img,cmap=plt.get_cmap('hmimag'),origin='lower',vmin=-300, vmax=300)

    data = fits.read(fn_aia)
    img = data[0][0]

    plt.imshow(img,cmap=plt.get_cmap('sdoaia94'),alpha=0.5, origin='lower',vmin=0,vmax=100)

    plt.savefig("frames/{:06}.png".format(frame_ctr))
    plt.close("all")
