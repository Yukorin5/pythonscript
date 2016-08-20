#!/usr/bin/env python
import datetime, StringIO, urllib, sys, subprocess,os,math,glob
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


sample_days = {
    'X': datetime.datetime(2013,11,5),
    'M': datetime.datetime(2015,10,1),
    'C': datetime.datetime(2014,5,1),
    'B': datetime.datetime(2016,8,3),
    'P': datetime.datetime(2016,8,17)}

credential = ""
for l,t in sample_days.iteritems():
    t2 = t - datetime.timedelta(days=17)
    print t2, t
exit(0)
    #print "./exportfile_AIA.csh 'hmi.M_720s[{}_00:00:00/17d@1d]' {} &".format(t2.strftime("%Y.%m.%d"), credential)

for label,t in sample_days.iteritems():
    frame_ctr = 0
    t2 = t - datetime.timedelta(days=17)
    is_nrt_str = "_nrt" if label == "P" else ""
    for i in range(17):
        t3 = t2 + datetime.timedelta(days=i)
        fn ="Uv-hmi/hmi.M_720s{}.{}_TAI.6173.0.magnetogram.fits".format(
            is_nrt_str, t3.strftime("%Y%m%d_%H%M%S"))
        print "? ", fn
        fns = glob.glob(fn)
        if len(fns) == 0:
            continue

        fn = fns[0]
        img = sunpy.map.Map(fn)
        print fn


        pylab.rcParams['figure.figsize'] = (6.4,6.4)

        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off') # labels along the bottom edge are off
        plt.tick_params(
            axis='y',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off') # labels along the bottom edge are off


        img.plot()
        plt.clim(-300,300)
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()
        plt.title('')
        plt.xlabel('')
        plt.ylabel('')
        plt.gca().get_xaxis().set_ticks([])
        plt.gca().get_yaxis().set_ticks([])

        frame_ctr += 1
        out_fn =  "Uv-hmi/{}-{:02}.png".format(label,frame_ctr)

        plt.savefig(out_fn)
        plt.close('all')
        img = sunpy.map.Map(fn)
