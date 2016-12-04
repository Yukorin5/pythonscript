#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, subprocess, pickle, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from astropy import units as u
import numpy as np
import pandas as pd
import observational_data as obs


time_begin = datetime.datetime(2014,10,01,00,00)
time_end   = datetime.datetime(2014,11,01,00,00)

plot_x = []
plot_y = []
plot_y_max = []

threshold_value = int(sys.argv[1])

for t_day in pd.date_range(time_begin,time_end, freq=datetime.timedelta(days=1)):
    try:
        threshold_integral_file = obs.data_path + t_day.strftime('/aia0193_work/%Y/%m/%d/TI.pickle')
        with open(threshold_integral_file,"r") as fp:
            ti_data = pickle.load(fp)
    except:
        # there was no file
        continue

    for t in pd.date_range(t_day,t_day+datetime.timedelta(days=1), freq=datetime.timedelta(minutes=12)):
        if t in ti_data:
            aia_ti_value = ti_data[t][threshold_value]
            goes_value = obs.get_goes_average(t, datetime.timedelta(days=1))
            goes_value_max = obs.get_goes_max(t, datetime.timedelta(days=1))
            plot_x.append(aia_ti_value)
            plot_y.append(goes_value)
            plot_y_max.append(goes_value_max)

plot_xy = []
for i in range(len(plot_x)):
    plot_xy.append((plot_x[i], plot_y[i]))

plt.rcParams['figure.figsize'] = (12.8,9.6)
plt.subplot2grid((1,1),(0,0), colspan=1, rowspan=1)
plt.plot(plot_x, plot_y, 'mo',markersize=1.0, markeredgecolor='r')
plt.gca().set_xscale('log')
plt.gca().set_yscale('log')
plt.gca().set_xlabel("AIA 193nm thresholded sum ({})".format(threshold_value))
plt.gca().set_ylabel("GOES 1-8A 24hour future average")
filename = "TI-vs-goes-average-{}.png".format(threshold_value)


plt.savefig(filename, dpi=100)
plt.close("all")

plt.rcParams['figure.figsize'] = (12.8,9.6)
plt.subplot2grid((1,1),(0,0), colspan=1, rowspan=1)
plt.plot(plot_x, plot_y_max, 'mo',markersize=1.0, markeredgecolor='r')
plt.gca().set_xscale('log')
plt.gca().set_yscale('log')
plt.gca().set_xlabel("AIA 193nm thresholded sum ({})".format(threshold_value))
plt.gca().set_ylabel("GOES 1-8A 24hour future max")
filename = "TI-vs-goes-max-{}.png".format(threshold_value)

plt.savefig(filename, dpi=100)
plt.close("all")

def tss_for_threshold(prediction_threshold, flare_threshold):
    n_tp = 0
    n_fp = 0
    n_fn = 0
    n_tn = 0

    for x,y in plot_xy:
        if x<prediction_threshold:
            if y<flare_threshold:
                n_tn+=1
            else:
                n_fn+=1
        else:
            if y<flare_threshold:
                n_fp+=1
            else:
                n_tp+=1
    tss = n_tp/(n_tp + n_fn+1e-16) - n_fp/(n_fp + n_tn+1e-16)
    return tss

def visualize_tss(flare_class, prediction_threshold, flare_threshold,tss):
    hits_x = []
    hits_y = []
    miss_x = []
    miss_y = []

    for x,y in plot_xy:
        if (x>=prediction_threshold) == (y>=flare_threshold):
            hits_x.append(x)
            hits_y.append(y)
        else:
            miss_x.append(x)
            miss_y.append(y)

    plt.rcParams['figure.figsize'] = (12.8,9.6)
    plt.subplot2grid((1,1),(0,0), colspan=1, rowspan=1)
    plt.plot(miss_x, miss_y, 'mo',markersize=1.0, markeredgecolor='r')
    plt.plot(hits_x, hits_y, 'mo',markersize=1.0, markeredgecolor='b')
    plt.gca().set_xscale('log')
    plt.gca().set_yscale('log')
    plt.gca().set_xlabel("AIA 193nm thresholded sum ({})".format(threshold_value))
    plt.gca().set_ylabel("GOES 1-8A 24hour future max")
    filename = "Flarepredict-{}-{}.png".format(flare_class, threshold_value)
    plt.title("{}-class flare prediction with TI({}) : TSS = {}".format(flare_class, threshold_value, tss))

    plt.savefig(filename, dpi=100)
    plt.close("all")

for flare_class, flare_threshold in [("C",1e-6), ("M",1e-5), ("X",1e-4)]:
    best_tss = -1; best_prediction_threshold = None

    for ptpower in range(0,700):
        prediction_threshold = 10.0 ** (ptpower/100.0)


        tss = tss_for_threshold(prediction_threshold, flare_threshold)
        print "testing: ", prediction_threshold, " TSS = ", tss
        if tss > best_tss:
            best_tss = tss
            best_prediction_threshold = prediction_threshold

    visualize_tss(flare_class, prediction_threshold, flare_threshold, tss)

exit()


def plot_horizontal_graph():
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
