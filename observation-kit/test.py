#!/usr/bin/env python3

import matplotlib as mpl
mpl.use('Agg')
import astropy.time as time
import glob
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime
import observational_data as O



plt.rcParams['figure.figsize'] = (60, 6)


time_begin = datetime.datetime(2011,1,1)
time_end   = datetime.datetime(2011,2,1)

t = time_begin

data_t = []
data_goes = []
data_goes_max = []

while True:
    print(t)
    if t > time_end:
        break
    data_t.append(t) 
    data_goes.append(O.goes_flux(t) )
    data_goes_max.append(O.goes_max(t, datetime.timedelta(hours=24)) )
    t += datetime.timedelta(minutes=12)

plt.plot(data_t, data_goes, color="b")
plt.plot(data_t, data_goes_max, color="r")

daysFmt = mdates.DateFormatter('%Y-%m-%d')
yearLoc = mdates.YearLocator()
monthLoc = mdates.MonthLocator()
plt.gca().xaxis.set_major_locator(yearLoc)
plt.gca().xaxis.set_major_formatter(daysFmt)
plt.gca().xaxis.set_minor_locator(monthLoc)
plt.gca().grid()
plt.gcf().autofmt_xdate()
plt.gca().set_title('GOES Flux')
plt.gca().set_xlabel('International Atomic Time')
plt.gca().set_ylabel(u'GOES Long[1-8A] Xray Flux')
plt.gca().set_yscale('log')

        
plt.ylim([1e-9, 1e-3])
plt.savefig("history-of-goes.png", dpi=100)
plt.close('all')
