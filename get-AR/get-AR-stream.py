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



harp_num = 1449

url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=hmi.sharp_720s[{}][]&op=rs_list&key=T_REC,CRPIX1,CRPIX2,CROTA2,CDELT1&seg=magnetogram".format(harp_num)
response = urllib.urlopen(url)
data = json.loads(response.read())
filename = data['segments'][0]['values'][0]
url = "http://jsoc.stanford.edu"+filename
photosphere_image = fits.open(url)        # download the data

num_images = len(data['segments'][0]['values'])

for image_idx in range(num_images):
    T_REC      = data['keywords'][0]['values'][image_idx]
    CRPIX1_CCD = float(data['keywords'][1]['values'][image_idx])
    CRPIX2_CCD = float(data['keywords'][2]['values'][image_idx])
    CROTA2_CCD = float(data['keywords'][3]['values'][image_idx])
    CDELT1_CCD = float(data['keywords'][4]['values'][image_idx])
    XDIM_CCD = float(data['segments'][0]['dims'][image_idx].rsplit('x', 1)[0])
    YDIM_CCD = float(data['segments'][0]['dims'][image_idx].rsplit('x', 1)[1])

    print T_REC, XDIM_CCD, YDIM_CCD


    url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=aia.lev1[{}/12s][?WAVELNTH=1600?]&op=rs_list&key=T_REC,CROTA2,CDELT1,CDELT2,CRPIX1,CRPIX2,CRVAL1,CRVAL2&seg=image_lev1".format(T_REC.replace("00_TAI","06_TAI"))
    response = urllib.urlopen(url)
    data_aia = json.loads(response.read())
    filename = data['segments'][0]['values'][0]
    url = "http://jsoc.stanford.edu"+filename
    chromosphere_image = fits.open(url)   # download the data

    T_REC = data_aia['keywords'][0]['values'][0]
    CROTA2_AIA = float(data_aia['keywords'][1]['values'][0])
    CDELT1_AIA = float(data_aia['keywords'][2]['values'][0])
    CDELT2_AIA = float(data_aia['keywords'][3]['values'][0])
    CRPIX1_AIA = float(data_aia['keywords'][4]['values'][0])
    CRPIX2_AIA = float(data_aia['keywords'][5]['values'][0])
    CRVAL1_AIA = float(data_aia['keywords'][6]['values'][0])
    CRVAL2_AIA = float(data_aia['keywords'][7]['values'][0])

    map_aia = sunpy.map.Map(url)
    map_aia.plot()
    plt.savefig("frames/aia-{:06}.png".format(image_idx))
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
    plt.savefig("frames/aia-sub-{:06}.png".format(image_idx))
    plt.close("all")
