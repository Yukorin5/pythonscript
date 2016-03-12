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
fn = "data/goes/g15_xrs_1m_20141001_20141031.csv"

goes_xs = []
goes_ys = []

with (open(fn, "r")) as fp:
    while True:
        con = fp.readline()
        if con[0:5]=='data:':
            break
    fp.readline()

    while True:
        con = fp.readline()
        if con=='':
            break
        ws = con.split(',')
        t = time.Time(ws[0]).datetime
        goes_xs.append(t)
        goes_ys.append(float(ws[6]))


global cutted_xs, cutted_ys, cutted_i
cutted_xs = []
cutted_ys = []
cutted_i = 0
# return the goes light curve from (t - 1day, t + 1day)
def cut_goes(t):
    global cutted_xs, cutted_ys, cutted_i
    aday = datetime.timedelta(seconds=86400)
    t0 = t - aday
    t1 = t + aday
    while len(cutted_xs)>0 and cutted_xs[0] < t0:
        cutted_xs=cutted_xs[1:]
        cutted_ys=cutted_ys[1:]

    while cutted_i < len(goes_xs):
        tpp = goes_xs[cutted_i]
        if tpp <= t1:
            cutted_xs.append(goes_xs[cutted_i])
            cutted_ys.append(goes_ys[cutted_i])
            cutted_i+=1
        else:
            break
    return (cutted_xs,cutted_ys)

dt = datetime.timedelta(seconds=720)
t = time_begin-dt
while t <= time_end:
    t += dt
    pngfn = pngdir + '/' + t.strftime('%Y-%m-%d-%H%M.png')
    print "plotting histogram: ", pngfn
    img = obs.aia193(t)

    plt.rcParams['figure.figsize'] = (12.0,6.0)

    # plot AIA histogram
    f,axs = plt.subplots(2)
    ax=axs[0]
    one_frame = ax.hist(img.flat, range(0,20000,200), log = True, color='blue')
    ax.set_title('AIA(193) Pixel Brightness Histogram at ' + fn.replace('.fits', ''))
    ax.set_xlim([0,20000])
    ax.set_ylim([1,1e8])

    # plot GOES flux
    ax=axs[1]
    ax.set_yscale('log')

    xs, ys = cut_goes(t)
    ax.plot(xs, ys, 'r')
    ax.plot([t, t], [1e-7, 1e-4], color='k', linestyle='-', linewidth=2)

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
