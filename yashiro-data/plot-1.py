#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import sunpy.io.fits as fits
from sunpy.cm import color_tables as ct
import sunpy.wcs as wcs

# from astropy.io import fits
import sys


fn_hmi = "hmi.sharp_cea_720s.20141021_000000_TAI.Br.fits"

data = fits.read(fn_hmi)
img = data[1][0]

plt.title("HMI + AIA94")
plt.imshow(img,cmap=plt.get_cmap('hmimag'),origin='lower')

fn_aia = "aia.sharp_cea_720s.20141021_0002_0094.fits"

data = fits.read(fn_aia)
img = data[0][0]

plt.imshow(img,cmap=plt.get_cmap('sdoaia94'),alpha=0.5, origin='lower')

plt.savefig("hmi+aia94.png")
plt.close("all")
