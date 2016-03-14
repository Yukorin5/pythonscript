#!/usr/bin/env python
# -*- coding: utf-8 -*-

import astropy.time as time
import math, random, os, sys, re, subprocess, datetime
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import observational_data as obs

from astropy.io import fits

def cmd(str):
    print str
    subprocess.call(str, shell = True)


pngdir = 'frames'
cmd('mkdir -p ' + pngdir)
cmd('rm {}/*'.format(pngdir))


t = time.Time("2011-01-01 00:00:00").datetime
now = datetime.datetime.now()

xs = []
ys = []
while t < now:
    print t
    xs.append(t)
    ys.append(obs.goes(t))
    t += datetime.timedelta(days=1)


plt.rcParams['figure.figsize'] = (16.0,12.0)

# plot AIA histogram
f,axs = plt.subplots(1)

# plot GOES flux
ax=axs[0]
ax.set_yscale('log')

ax.plot(xs, ys, 'b')


years   = mdates.YearLocator()  # every day
daysFmt = mdates.DateFormatter('%Y-%m-%d')
months  = mdates.MonthLocator()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(daysFmt)
ax.xaxis.set_minor_locator(months)
ax.grid()
f.autofmt_xdate()
ax.set_title('GOES Flux')
ax.set_xlabel('International Atomic Time')
ax.set_ylabel(u'GOES Long[1-8Å] Xray Flux')



# generate image
plt.savefig("goes-long-lightcurve.png", dpi=100)
plt.close('all')
