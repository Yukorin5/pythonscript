#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from astropy import units as u

from observational_data import *

#img = get_aia_image(193, datetime.datetime(2014,12,20,00,36))


subprocess.call(['mkdir', '-p','frames'])

filenames = []
counter = 0

time_begin = datetime.datetime(2011,01,01,00,00)
time_end   = datetime.datetime(2016,12,01,00,00)

plt.rcParams['figure.figsize'] = (320.0,16.0)

t = time_begin

goes_curve_t = []
goes_curve_y = []

goes_max_curve_t = []
goes_max_curve_y = []


while True:
    dt = datetime.timedelta(hours=1)
    t += dt
    y_max = get_goes_max_fast(t, datetime.timedelta(days=1))
    if t > time_end:
        break
    if y_max is None:
        continue

    y = get_goes_flux_fast(t)

    goes_max_curve_t.append(t)
    goes_max_curve_y.append(y_max)
    goes_max_curve_t.append(t+dt)
    goes_max_curve_y.append(y_max)

    goes_curve_t.append(t)
    goes_curve_y.append(y)

    print t,y


fig, ax = plt.subplots()
ax.set_yscale('log')

ax.plot(goes_max_curve_t, goes_max_curve_y, 'r')
ax.plot(goes_curve_t, goes_curve_y, 'b')

years   = mdates.YearLocator()  # every year
months  = mdates.MonthLocator()  # every month
days    = mdates.DayLocator()  # every day
days.MAXTICKS = 10000
daysFmt = mdates.DateFormatter('%Y-%m-%d')
hours   = mdates.HourLocator()
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(daysFmt)
ax.xaxis.set_minor_locator(days)
ax.grid()
fig.autofmt_xdate()
ax.set_title('GOES 24h future max from {}(TAI)'.format(time_begin.strftime('%Y-%m-%d %H:%M:%S')))
ax.set_xlabel('International Atomic Time')
ax.set_ylabel(u'GOES Long[1-8 Angstrom] Xray Flux (W/m²)')
plt.text(time_end, 5e-4, 'X-class', rotation=90)
plt.text(time_end, 5e-5, 'M-class', rotation=90)
plt.text(time_end, 5e-6, 'C-class', rotation=90)
plt.text(time_end, 5e-7, 'B-class', rotation=90)
plt.ylim([1e-7,1e-3])
plt.savefig("goes-flux-history-fast.png", dpi=100)
plt.close('all')
