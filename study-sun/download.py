#!/usr/bin/env python
import datetime, os, sys, subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab
import numpy as np
from astropy.io import fits
from astropy import units as u

import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import sunpy.map

from observational_data import *

nums = [int(i) for i in sys.argv[1:]]

t_begin = datetime.datetime(*nums)
t = t_begin

while t < t_begin + datetime.timedelta(days=16):
    print t
#    img = get_hmi_image(t)
    img = get_aia_image(131, t)
    img = get_aia_image(171, t)
    img = get_aia_image(211,t )
#    img = get_aia_image3("35, t)
#    img = get_aia_image(, t)
#    img = get_aia_image(4500, t)

    t += datetime.timedelta(minutes=60)

