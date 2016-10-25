#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, subprocess, pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from astropy import units as u
import numpy as np
import pandas as pd
import observational_data as obs


time_begin = datetime.datetime(2013,11,1,00,00)
time_end   = datetime.datetime(2013,12,1,00,00)

plot_x = []
plot_y = []

threshold_value = 3000

for t_day in pd.date_range(time_begin,time_end, freq=datetime.timedelta(days=1)):
    threshold_integral_file = obs.data_path + t_day.strftime('/aia0193_work/%Y/%m/%d/TI.pickle')
    with open(threshold_integral_file,"r") as fp:
        ti_data = pickle.load(fp)
    
    for t in pd.date_range(t_day,t_day+datetime.timedelta(days=1), freq=datetime.timedelta(minutes=12)):
        if t in ti_data:
            aia_ti_value = ti_data[t][threshold_value]
            goes_value = obs.get_goes_max(t, datetime.timedelta(days=1))
            
            plot_x.append(aia_ti_value)
            plot_y.append(goes_value)


print plot_x, plot_y

plt.rcParams['figure.figsize'] = (6.4,9.6)
plt.subplot2grid((2,1),(0,0), colspan=1, rowspan=1)
plt.plot(plot_x, plot_y, 'mo',markersize=2.0, markeredgecolor='r')
plt.gca().set_xscale('log')
plt.gca().set_yscale('log')
plt.gca().set_xlabel("AIA 193nm thresholded sum ({})".format(threshold_value))
plt.gca().set_ylabel("GOES 1-8A 24hour future max")
filename = "TI-vs-goes.png"


plt.savefig(filename, dpi=100)
plt.close("all")


exit()

# goes fluxをプロットします
plt.subplot2grid((6,10),(4,1),colspan=9)

plt.gca().set_yscale('log')
plt.plot(goes_flux_t,goes_flux_y,'b')
plt.gca().set_ylim([1e-7, 1e-3])
plt.gca().set_xlabel('Time (TAI)')
plt.gca().set_ylabel('GOES X-ray flux (W/m^2)')

dayLocator  = mdates.DayLocator()  
hourLocator = mdates.HourLocator()  
daysFmt = mdates.DateFormatter('%Y-%m-%d')
plt.gca().xaxis.set_major_locator(dayLocator)
plt.gca().xaxis.set_major_formatter(daysFmt)
plt.gca().xaxis.set_minor_locator(hourLocator)
plt.gca().grid()
plt.gcf().autofmt_xdate()

# AIA fluxをプロットします
plt.subplot2grid((6,10),(5,1),colspan=9)

# plt.gca().set_yscale('log')
plt.plot(aia_flux_t,aia_flux_y,'r')
plt.plot([t, t], [0, 1], color='k', linestyle='-', linewidth=2)
plt.gca().set_xlabel('Time (TAI)')
plt.gca().set_ylabel('AIA Thresholded integral')

dayLocator  = mdates.DayLocator()  
hourLocator = mdates.HourLocator()  
daysFmt = mdates.DateFormatter('%Y-%m-%d')
plt.gca().xaxis.set_major_locator(dayLocator)
plt.gca().xaxis.set_major_formatter(daysFmt)
plt.gca().xaxis.set_minor_locator(hourLocator)
plt.gca().grid()
plt.gcf().autofmt_xdate()
