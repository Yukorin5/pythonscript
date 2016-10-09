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

time_begin = datetime.datetime(2013,11,04,00,00)
time_end   = datetime.datetime(2013,11,07,00,00)


t = time_begin

goes_curve_t = []
goes_curve_y = []


while True:
    t += datetime.timedelta(minutes=2)
    if t > time_end:
        break
    
    y = get_goes_flux(t)
    if y is None:
        continue

    goes_curve_t.append(t)
    goes_curve_y.append(y)

    print t,y

fig, ax = plt.subplots()
ax.set_yscale('log')

ax.plot(goes_curve_t, goes_curve_y, 'b')

days    = mdates.DayLocator()  # every day
daysFmt = mdates.DateFormatter('%Y-%m-%d')
hours   = mdates.HourLocator()
ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(daysFmt)
ax.xaxis.set_minor_locator(hours)
ax.grid()
fig.autofmt_xdate()
ax.set_title('GOES Forecast from {}(TAI)'.format(time_begin.strftime('%Y-%m-%d %H:%M:%S')))
ax.set_xlabel('International Atomic Time')
ax.set_ylabel(u'GOES Long[1-8Å] Xray Flux (W/m²)')
plt.text(time_end, 5e-4, 'X-class', rotation=90)
plt.text(time_end, 5e-5, 'M-class', rotation=90)
plt.text(time_end, 5e-6, 'C-class', rotation=90)
plt.text(time_end, 5e-7, 'B-class', rotation=90)
plt.ylim([1e-7,1e-3])
plt.savefig("sample-goes-flux.png", dpi=200)
plt.close('all')
