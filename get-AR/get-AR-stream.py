#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import json, urllib, numpy as np, matplotlib.pylab as plt, matplotlib.ticker as mtick,sys
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


harp_num = int(sys.argv[1])
wavelengths=[94,193,1600]

def cadence_of_wavelength(w):
    # c.f. http://jsoc.stanford.edu/new/AIA/AIA_lev1.html
    if w < 1000:
        return 12
    if w <= 1700:
        return 24
    return 3600

def vmax_of_wavelength(w):
    if w==94: return 100
    if w==193: return 3000
    if w==1600: return 200
    return None


url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=hmi.sharp_720s[{}][]&op=rs_list&key=T_REC,CRPIX1,CRPIX2,CROTA2,CDELT1&seg=magnetogram".format(harp_num)

# url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=hmi.sharp_720s[1449][2012.03.06_23:29:06_TAI]&op=rs_list&key=T_REC,CRPIX1,CRPIX2,CROTA2,CDELT1&seg=magnetogram"

response = urllib.urlopen(url)
data = json.loads(response.read())
filename = data['segments'][0]['values'][0]
url = "http://jsoc.stanford.edu"+filename
photosphere_image = fits.open(url)        # download the data

num_images = len(data['segments'][0]['values'])

starting_index=0
if len(sys.argv)>=3:
    starting_index = int(sys.argv[2])

for image_idx in range(starting_index,num_images):
    print image_idx, "/", num_images

    T_REC      = data['keywords'][0]['values'][image_idx]
    CRPIX1_CCD = float(data['keywords'][1]['values'][image_idx])
    CRPIX2_CCD = float(data['keywords'][2]['values'][image_idx])
    CROTA2_CCD = float(data['keywords'][3]['values'][image_idx])
    CDELT1_CCD = float(data['keywords'][4]['values'][image_idx])
    XDIM_CCD = float(data['segments'][0]['dims'][image_idx].rsplit('x', 1)[0])
    YDIM_CCD = float(data['segments'][0]['dims'][image_idx].rsplit('x', 1)[1])

    print T_REC, XDIM_CCD, YDIM_CCD
    for wavelength in wavelengths:
        cadence = cadence_of_wavelength(wavelength)
        url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=aia.lev1[{t}/{c}s][?WAVELNTH={w}?]&op=rs_list&key=T_REC,CROTA2,CDELT1,CDELT2,CRPIX1,CRPIX2,CRVAL1,CRVAL2&seg=image_lev1".format(t=T_REC, w=wavelength, c = cadence)

        try:
            response = urllib.urlopen(url)
            data_aia = json.loads(response.read())
        except Exception as e:
            print "Error loading AIA metadata for WL = ", wavelength, "T = ", T_REC
            print e.message
            continue


        if not 'segments' in data_aia:
            print "No data for WL = ", wavelength, "T = ", T_REC
            continue

        filename = data_aia['segments'][0]['values'][0]
        url = "http://jsoc.stanford.edu"+filename
        try:
            chromosphere_image = fits.open(url)   # download the data
        except Exception as e:
            print "Error loading AIA for WL = ", wavelength, "T = ", T_REC
            print e.message
            continue

        T_REC = data_aia['keywords'][0]['values'][0]
        CROTA2_AIA = float(data_aia['keywords'][1]['values'][0])
        CDELT1_AIA = float(data_aia['keywords'][2]['values'][0])
        CDELT2_AIA = float(data_aia['keywords'][3]['values'][0])
        CRPIX1_AIA = float(data_aia['keywords'][4]['values'][0])
        CRPIX2_AIA = float(data_aia['keywords'][5]['values'][0])
        CRVAL1_AIA = float(data_aia['keywords'][6]['values'][0])
        CRVAL2_AIA = float(data_aia['keywords'][7]['values'][0])

        ratio = (CDELT1_CCD)/(CDELT1_AIA)
        print "The ratio of the HMI:AIA platescales is",ratio

        chromosphere_image.verify("fix")
        exptime = chromosphere_image[1].header['EXPTIME']
        if exptime <=0:
            print "Non-positive exptime for WL = ", wavelength, "T = ", T_REC
            continue

        print "WL = ", wavelength, "T = ", T_REC, "EXPTIME = ", exptime
        chromosphere_image[1].data /= exptime

        if (CROTA2_AIA > 5.0):
            print "The AIA camera rotation angle is",CROTA2_AIA,". Rotating AIA image."
            chromosphere_image[1].data = np.rot90(chromosphere_image[1].data,2)
        subdata = chromosphere_image[1].data[(2048. + CRPIX2_CCD*(ratio) - YDIM_CCD*(ratio)) : (2048. + CRPIX2_CCD*(ratio)),(2048. + CRPIX1_CCD*(ratio) - XDIM_CCD*(ratio)) : (2048. + CRPIX1_CCD*(ratio))]


        sdoaia_cmap = plt.get_cmap('sdoaia{}'.format(wavelength))
        plt.imshow(subdata,cmap=sdoaia_cmap,origin='lower',vmin=0,vmax=vmax_of_wavelength(wavelength))
        print 'The dimensions of this image are',subdata.shape[0],'by',subdata.shape[1],'.'
        plt.title("HARP AR{} AIA {} Angstrom {}".format(harp_num, wavelength, T_REC))
        cbaxes = plt.gcf().add_axes([0.8, 0.1, 0.03, 0.8])
        plt.colorbar(cax=cbaxes)
        plt.savefig("frames/HARP{}-aia{:04}-f{:06}.png".format(harp_num, wavelength, image_idx))
        plt.close("all")
