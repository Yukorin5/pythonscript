#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import sunpy.io.fits as fits
from sunpy.cm import color_tables as ct
import sunpy.wcs as wcs
from astropy.time import Time
import sys


t = Time('2014-10-21T00:00:00',format='isot',scale="tai")
