#!/usr/bin/env python
# -*- coding: utf-8 -*-

import astropy.time as time
import math, random, os, sys, re, subprocess, datetime
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from astropy.io import fits

def system_call(cmd):
    print cmd
    subprocess.call(cmd, shell = True)

pngdir = 'frames'
system_call('mkdir -p ' + pngdir)
system_call('rm {}/*'.format(pngdir))



time_begin = time.Time("2013-11-01 00:00:00").datetime
time_end = time.Time("2013-11-01 02:00:00").datetime
dt = datetime.timedelta(seconds=720)
t = time_begin-dt
while t <= time_end:
    t += dt

    fn=t.strftime('%Y/%m/%d/%H%M.fits')
    if not(os.path.exists(fn)):
        continue

    pngfn = pngdir + '/' + fn.replace('.fits', '.png').replace('/','-')
    print "plotting histogram: ", fn , '->' , pngfn

    h = fits.open(fn)
    h[1].verify('fix')
    exptime = h[1].header['EXPTIME']
    if exptime <=0:
        print "Warning: non-positive EXPTIME: ", h[1].header['EXPTIME']
        exptime = 2.0

    # adjust the pixel luminosity with the exposure time.
    img = h[1].data / exptime
    fig,ax = plt.subplots()

    one_frame = plt.hist(img.flat, range(0,20000,200), log = True, color='blue')
    ax.set_title(fn)
    ax.set_xlim([0,20000])
    ax.set_ylim([1,1e8])
    plt.savefig(pngfn, dpi=100)
    plt.close('all')


print "creating animation."

system_call('convert -loop 1 -delay 20 {}/*.png aia.gif'.format(pngdir))
