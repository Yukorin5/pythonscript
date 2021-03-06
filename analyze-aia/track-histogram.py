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


time_begin = time.Time("2014-10-24 00:00:00").datetime
time_end = time.Time("2014-10-24 02:00:00").datetime

def cut_goes(t0):
    xs = []
    ys = []
    for i in range(-86400, 86400, 60):
        t = t0 + datetime.timedelta(seconds=i)
        xs.append(t)
        ys.append(obs.goes(t))
    return (xs,ys)

# return goes one-day future max lightcurve
def goes_1day_futuremax(t0):
    xs = []
    ys = []
    for i in range(-86400, 86400, 60):
        t = t0 + datetime.timedelta(seconds=i)
        xs.append(t)
        ys.append(obs.goes_max(t ,  datetime.timedelta(days=1) ))
    return (xs,ys)


dt = datetime.timedelta(seconds=720)
t = time_begin-dt
while t <= time_end:
    t += dt
    pngfn = pngdir + '/' + t.strftime('%Y-%m-%d-%H%M.png')
    print "plotting histogram: ", pngfn
    img = obs.aia193(t)

    if img is None:
        continue

    plt.rcParams['figure.figsize'] = (12.0,6.0)

    # plot AIA histogram
    f,axs = plt.subplots(2)
    ax=axs[0]
    one_frame = ax.hist(img.flat, range(0,20000,200), log = True, color='blue')
    ax.set_title('AIA(193) Pixel Brightness Histogram at ' + t.strftime('%Y-%m-%d %H:%M'))
    ax.set_xlim([0,20000])
    ax.set_ylim([1,1e8])

    # plot GOES flux
    ax=axs[1]
    ax.set_yscale('log')

    xs, ys = cut_goes(t)
    ax.plot(xs, ys, 'b')

    xs, ys = goes_1day_futuremax(t)
    ax.plot(xs, ys, color='b', linestyle='--')


    ax.plot([t, t], [1e-7, 1e-3], color='k', linestyle='-', linewidth=2)




    days    = mdates.DayLocator()  # every day
    daysFmt = mdates.DateFormatter('%Y-%m-%d')
    hours   = mdates.HourLocator()
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)
    ax.xaxis.set_minor_locator(hours)
    ax.grid()
    f.autofmt_xdate()
    ax.set_title('GOES Flux')
    ax.set_xlabel('International Atomic Time')
    ax.set_ylabel(u'GOES Long[1-8Å] Xray Flux')



    # generate image
    plt.savefig(pngfn, dpi=100)
    plt.close('all')


print "creating animation."

cmd('convert -loop 1 -delay 20 {}/*.png aia.mp4'.format(pngdir))
