#!/usr/bin/env python

import math, sys

def sin(deg):
    return math.sin(deg / 180.0 * math.pi)
def cos(deg):
    return math.cos(deg / 180.0 * math.pi)
def acos(x):
    return math.acos(x) / math.pi * 180.0


spacecraft_lon, spacecraft_lat, cme_lon, cme_lat = [float(s) for s in sys.argv[1:]]

spacecraft_x = cos(spacecraft_lat) * cos(spacecraft_lon)
spacecraft_y = cos(spacecraft_lat) * sin(spacecraft_lon)
spacecraft_z = sin(spacecraft_lat)


cme_x = cos(cme_lat) * cos(cme_lon)
cme_y = cos(cme_lat) * sin(cme_lon)
cme_z = sin(cme_lat)

inner_prod = spacecraft_x * cme_x +  spacecraft_y * cme_y +  spacecraft_z * cme_z

print 90 - acos(inner_prod)
