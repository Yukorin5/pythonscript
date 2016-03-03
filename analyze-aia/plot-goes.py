#!/usr/bin/env python
# -*- coding: utf-8 -*-

import astropy.time as time
import sys
import datetime
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


fn = sys.argv[1]
fn_png=fn.replace('.csv','.png')

xs = []
ys = []

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
        xs.append(t)
        ys.append(float(ws[6]))


fig, ax = plt.subplots()
ax.set_yscale('log')

ax.plot(xs, ys, 'r')

days    = mdates.DayLocator()  # every day
daysFmt = mdates.DateFormatter('%Y-%m-%d')
hours   = mdates.HourLocator()
ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(daysFmt)
ax.xaxis.set_minor_locator(hours)
ax.grid()
fig.autofmt_xdate()
ax.set_title('GOES Flux')
ax.set_xlabel('International Atomic Time')
ax.set_ylabel(u'GOES Long[1-8Å] Xray Flux')

plt.savefig(fn_png, dpi=200)
plt.close('all')
