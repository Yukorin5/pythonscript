#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import json, urllib, numpy as np, matplotlib.pylab as plt, matplotlib.ticker as mtick
import sunpy.map
from astropy.io import fits
from sunpy.cm import color_tables as ct
import sunpy.wcs as wcs
from datetime import datetime as dt_obj
import matplotlib.dates as mdates
import matplotlib.colors as mcol
import matplotlib.patches as ptc
from matplotlib.dates import *
import math

url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=hmi.M_720s[2012.03.06_23:29:06_TAI]&op=rs_list&seg=magnetogram"
response = urllib.urlopen(url)
data = json.loads(response.read())
filename = data['segments'][0]['values'][0]
url = "http://jsoc.stanford.edu"+filename
photosphere_full_image = fits.open(url)   # download the data

url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=hmi.sharp_720s[1449][2012.03.06_23:29:06_TAI]&op=rs_list&key=CRPIX1,CRPIX2,CROTA2,CDELT1&seg=magnetogram"
response = urllib.urlopen(url)
data = json.loads(response.read())
filename = data['segments'][0]['values'][0]
url = "http://jsoc.stanford.edu"+filename
photosphere_image = fits.open(url)        # download the data

keywords = data['keywords'][0]['values']
CRPIX1_CCD = float(data['keywords'][0]['values'][0])
CRPIX2_CCD = float(data['keywords'][1]['values'][0])
CROTA2_CCD = float(data['keywords'][2]['values'][0])
CDELT1_CCD = float(data['keywords'][3]['values'][0])
XDIM_CCD = float(data['segments'][0]['dims'][0].rsplit('x', 1)[0])
YDIM_CCD = float(data['segments'][0]['dims'][0].rsplit('x', 1)[1])

if (CROTA2_CCD > 5.0):
    print "The HMI camera rotation angle is",CROTA2_CCD,". Rotating HMI images."
    photosphere_full_image[1].data = np.rot90(photosphere_full_image[1].data,2)
    photosphere_image[1].data = np.rot90(photosphere_image[1].data,2)


hmimag = plt.get_cmap('hmimag')
print photosphere_image[1].data.shape
plt.imshow(photosphere_image[1].data)
plt.savefig("hmi-image.png")
print 'The dimensions of this image are',photosphere_image[1].data.shape[0],'by',photosphere_image[1].data.shape[1],'.'
