#!/usr/bin/env python
# -*- coding: utf-8 -*-

import astropy.time as time
import observational_data as obs
import datetime



t = time.Time("2014-10-22 00:00:00").datetime

print obs.goes_max(t, datetime.timedelta(days=1))
print obs.goes_max(t, datetime.timedelta(days=2))
print obs.goes_max(t, datetime.timedelta(days=3))
print obs.goes_max(t, datetime.timedelta(days=4))
print obs.goes_max(t, datetime.timedelta(days=5))

for i in range(10):
    print t, obs.goes(t)
    t+=datetime.timedelta(seconds=720)
