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

url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=aia.lev1[2012.03.06_23:29:06_TAI/12s][?WAVELNTH=1600?]&op=rs_list&key=T_REC,CROTA2,CDELT1,CDELT2,CRPIX1,CRPIX2,CRVAL1,CRVAL2&seg=image_lev1"
response = urllib.urlopen(url)
data = json.loads(response.read())
filename = data['segments'][0]['values'][0]
url = "http://jsoc.stanford.edu"+filename
chromosphere_image = fits.open(url)   # download the data

T_REC = data['keywords'][0]['values'][0]
CROTA2_AIA = float(data['keywords'][1]['values'][0])
CDELT1_AIA = float(data['keywords'][2]['values'][0])
CDELT2_AIA = float(data['keywords'][3]['values'][0])
CRPIX1_AIA = float(data['keywords'][4]['values'][0])
CRPIX2_AIA = float(data['keywords'][5]['values'][0])
CRVAL1_AIA = float(data['keywords'][6]['values'][0])
CRVAL2_AIA = float(data['keywords'][7]['values'][0])

map_aia = sunpy.map.Map(url)
map_aia.plot()
plt.savefig("aia.png")
plt.close("all")



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
plt.savefig("sharp-image.png")
print 'The dimensions of this image are',photosphere_image[1].data.shape[0],'by',photosphere_image[1].data.shape[1],'.'
plt.close("all")

ratio = (CDELT1_CCD)/(CDELT1_AIA)
print "The ratio of the HMI:AIA platescales is",ratio

chromosphere_image.verify("fix")
if (CROTA2_AIA > 5.0):
    print "The AIA camera rotation angle is",CROTA2_AIA,". Rotating AIA image."
    chromosphere_image[1].data = np.rot90(chromosphere_image[1].data,2)
subdata = chromosphere_image[1].data[(2048. + CRPIX2_CCD*(ratio) - YDIM_CCD*(ratio)) : (2048. + CRPIX2_CCD*(ratio)),(2048. + CRPIX1_CCD*(ratio) - XDIM_CCD*(ratio)) : (2048. + CRPIX1_CCD*(ratio))]


sdoaia1600 = plt.get_cmap('sdoaia1600')
plt.imshow(subdata,cmap=sdoaia1600,origin='lower',vmin=0,vmax=400)
print 'The dimensions of this image are',subdata.shape[0],'by',subdata.shape[1],'.'
plt.savefig("aia-subimage.png")
plt.close("all")
