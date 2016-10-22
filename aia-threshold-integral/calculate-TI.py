#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, subprocess, pickle
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


time_begin = datetime.datetime(2013,11,26,0,00)
time_end   = datetime.datetime(2013,11,27,0,00)
dt = datetime.timedelta(minutes=12)


global data_path
work_dir = data_path + time_begin.strftime('/aia0193_work/%Y/%m/%d')
subprocess.call("mkdir -p " + work_dir, shell=True)
work_file = work_dir + "TI.pickle"



t = time_begin-dt
ret = {}
while True:
    t += dt
    if t > time_end:
        break

    img = get_aia_image(193, t)
    if img is None:
        continue
    img.data = img.data / (img.exposure_time / u.second)
    

    threshold_integrals = {}
    for threshold in xrange(0,10000,100):
        y = np.sum(np.maximum(0, img.data - threshold))
        threshold_integrals[threshold] = float(y)
    print t, threshold_integrals

    ret[t] = threshold_integrals

print ret
with open(work_file,"w") as fp:
    pickle.dump(ret, fp, -1)
