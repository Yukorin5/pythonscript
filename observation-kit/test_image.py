#!/usr/bin/env python3

from observational_data import *
import datetime

t=datetime.datetime(2011,1,1)

img = get_sun_image(t,211)
plot_sun_image(img, "test-aia0211.png",211,vmax=100)
