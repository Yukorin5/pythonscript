#!/usr/bin/env python
import datetime, StringIO, urllib, sys, subprocess,os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab
import numpy as np
from astropy.io import fits
from astropy import units as u

import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import sunpy.map



for fn in sys.argv[1:]:
    fnbody,ext = os.path.splitext(fn)

    if '193.image' in fn:
        img_type = 'aia193'
    elif '94.image' in fn:
        img_type = 'aia94'
    elif 'hmi' in fn:
        img_type = 'hmi'
    else:
        print "Unknown image type:" , fn
        exit(0)


    img = sunpy.map.Map(fn)

    print img.data.shape
    print "dt = ", img.exposure_time
    print type(img.data)


    #img.data = img.data / (img.exposure_time / u.second)

    print np.nanmin(img.data)
    print np.nanmax(img.data)


    #pylab.rcParams['figure.figsize'] = (6.4,6.4)
    #pylab.clf()
    img.plot()
    plt.colorbar()

    if img_type=='hmi':
        plt.clim(-300,300)
    elif img_type=='aia193':
        plt.clim(0,1000)
    elif img_type=='aia94':
        plt.clim(0,1000)

    plt.savefig(fnbody + '.png')
    plt.close('all')
