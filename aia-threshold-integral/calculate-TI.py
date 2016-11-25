#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, subprocess, pickle,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

from astropy import units as u

import observational_data as obs

obs.offline_mode = True


time_epoch = datetime.datetime(2011,1,1,0,00)
if len(sys.argv)>1:
     time_epoch = datetime.datetime.strptime(sys.argv[1],"%Y-%m-%d")



for day_add in xrange(366*6):
    
    time_begin = time_epoch + datetime.timedelta(days=day_add)
    time_end   = time_begin + datetime.timedelta(days=1)
        
    print time_begin

    dt = datetime.timedelta(minutes=12)
    
    
    work_dir = obs.data_path + time_begin.strftime('/aia0193_work/%Y/%m/%d/')
    subprocess.call("mkdir -p " + work_dir, shell=True)
    work_file = work_dir + "TI.pickle"
    
    t = time_begin-dt
    ret = {}
    while True:
        t += dt
        if t > time_end:
            break
    
        img = obs.get_aia_image(193, t)
        if img is None:
            continue
        img.data = img.data / (img.exposure_time / u.second)
        
    
        threshold_integrals = {}
        for threshold in xrange(0,10000,100):
            y = np.sum(np.maximum(0, img.data - threshold))
            threshold_integrals[threshold] = float(y) 
       print t, threshold_integrals
    
        ret[t] = threshold_integrals
    
    with open(work_file,"w") as fp:
        pickle.dump(ret, fp, -1)
