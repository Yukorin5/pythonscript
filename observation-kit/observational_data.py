#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import astropy.time as time
import datetime
import numpy as np
from astropy.io import fits
import sunpy.map
from sunpy.cm import color_tables as ct
import sunpy.wcs as wcs
import scipy.ndimage.interpolation as interpolation
import sys

global goes_raw_data_fast
goes_raw_data_fast = None
# 時刻t0におけるgoes X線フラックスの値を返します。
# １時間ごとの精度しかありませんが、高速です
def goes_flux(t0):
    global goes_raw_data_fast
    if goes_raw_data_fast is None:
        goes_raw_data_fast = {}
        with open("goes-data-12min.txt","r") as fp:
            for l in iter(fp.readline, ''):
                ws = l.split()
                t = datetime.datetime.strptime(ws[0],"%Y-%m-%dT%H:%M")
                x = float(ws[1])
                goes_raw_data_fast[t] = x
    t=datetime.datetime(t0.year,t0.month,t0.day,t0.hour)
    if t in goes_raw_data_fast:
        return goes_raw_data_fast[t]
    return 1e-8

# 時刻t0におけるgoes X線フラックスの値を返します。
# １時間ごとの精度しかありませんが、高速です
def goes_max(t, timedelta):
    ret = goes_flux(t)
    dt = datetime.timedelta(0)
    while dt <= timedelta:
        ret = max(ret, goes_flux(t + dt))
        dt += datetime.timedelta(minutes=12)
    return ret


def get_sun_image(time, wavelength, image_size = 1023):
    try:
        time_str = time.strftime("%Y/%m/%d/%H%M.fits")
        filename = "/work1/t2g-16IAS/aia{:04}/".format(wavelength) + time_str
        if wavelength == 'hmi':
            filename = "/work1/t2g-16IAS/hmi/" + time_str
        aia_image = fits.open(filename)

        aia_image.verify("fix")
        exptime = aia_image[1].header['EXPTIME']
        if exptime <= 0:
            print(time, "non-positive exposure",file=sys.stderr)
            return None

        quality = aia_image[1].header['QUALITY']
        if quality !=0:
            print(time, "bad quality",file=sys.stderr)
            return None

        original_width = aia_image[1].data.shape[0]
        return interpolation.zoom(aia_image[1].data, image_size / float(original_width)) / exptime
    except Exception as e:
        print(e,file=sys.stderr)
        return None

def plot_sun_image(img, filename, wavelength, title = '', vmin=0.0, vmax = 1.0):
    if wavelength == 'hmi':
        cmap = plt.get_cmap('hmimag')
    else:
        cmap = plt.get_cmap('sdoaia{}'.format(wavelength))
    plt.title(title)
    plt.imshow(img,cmap=cmap,origin='lower',vmin=vmin, vmax=vmax)
    plt.savefig(filename)
    plt.close("all")
