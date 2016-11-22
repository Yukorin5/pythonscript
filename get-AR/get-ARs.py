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

url =  "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=hmi.sharp_720s[2][]&op=rs_list&key=T_REC,CRPIX1,CRPIX2,CROTA2,CDELT1&seg=magnetogram"
url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=hmi.sharp_720s[1449][2012.03.06_23:29:06_TAI]&op=rs_list&key=CRPIX1,CRPIX2,CROTA2,CDELT1&seg=magnetogram"

response = urllib.urlopen(url)
data = json.loads(response.read())
for i in range( len(data['segments'][0]['values'])):
    t = data['keywords'][0]['values'][i]
    print t
    print type(t)
    print data['segments'][0]['dims'][i]
    print data['segments'][0]
