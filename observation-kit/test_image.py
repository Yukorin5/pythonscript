#!/usr/bin/env python3

from observational_data import *
import datetime
import numpy as np

t=datetime.datetime(2012,1,1)

img = get_sun_image(t,211)

print(type(img))
print(img.shape)
print(img.dtype)
print(img)

img = np.log(np.maximum(1, img))

plot_sun_image(img, "test-aia0211.png",211,vmax=10)
