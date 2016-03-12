#!/usr/bin/env python

import astropy.time as time
import observational_data as obs

t = time.Time('2015-01-02 00:02:12')
print obs.goes(t)
