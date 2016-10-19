#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from astropy import units as u

from observational_data import *

#img = get_aia_image(193, datetime.datetime(2014,12,20,00,36))


subprocess.call(['mkdir', '-p','frames'])

filenames = []
counter = 0


# time_begin = datetime.datetime(2014,10,24,00,00)
# time_end   = datetime.datetime(2014,10,27,00,00)

time_begin = datetime.datetime(2013,11,04,00,00)
time_end   = datetime.datetime(2013,11,04,01,00)
dt = datetime.timedelta(minutes=2)


goes_flux_t = []
goes_flux_y = []

t = time_begin
while True:
    t += dt
    if t > time_end:
        break
    y = get_goes_flux_fast(t)

    print t,y

    goes_flux_t.append(t)
    goes_flux_y.append(y)


t = time_begin
while True:
    t += dt
    if t > time_end:
        break

    img = get_aia_image(193, t)
    if img is None:
        continue

    print t
    print "image shape = ", img.data.shape
    print "exposure time = ", img.exposure_time
    print "data type =",  type(img.data)
    
    img.data = img.data / (img.exposure_time / u.second)
    
    print "min pixel brightness = ", np.min(img.data)
    print "max pixel brightness = ", np.max(img.data)
    
    
    plt.rcParams['figure.figsize'] = (6.4,9.6)


    # 画面を(2,1)に分割して1番目にAIAの画像をプロットします
    plt.subplot2grid((2,1),(0,0), colspan=1, rowspan=1)

    img.plot()
    plt.title(img.name, y=1.08) # move the titles up
    cbar =plt.colorbar(ticks = [0,1000,3000,10000])
    cbar.ax.set_yticklabels(['0','1000','3000','10000'])
    plt.clim(0,10000)

    # goes fluxをプロットします
    plt.subplot2grid((3,10),(2,1),colspan=9)
    
    plt.gca().set_yscale('log')
    plt.plot(goes_flux_t,goes_flux_y,'b')
    plt.gca().set_ylim([1e-7, 1e-3])
    plt.plot([t, t], [1e-7, 1e-3], color='k', linestyle='-', linewidth=2)
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


    filename = 'frames/{:08}.png'.format(counter)
    counter+=1
    plt.savefig(filename, dpi=100)

    filenames.append(filename)
    plt.close('all')

str = "test"
subprocess.call('ffmpeg -y -r 24 -i frames/%08d.png -qscale 0  -pix_fmt yuv420p -c:v libx264 movie-{}.mp4'.format(str), shell=True)
