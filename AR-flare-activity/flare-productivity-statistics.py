#!/usr/bin/env python3

import datetime
import numpy as np
from pprint import pprint

class SolarRegionData:
    def __init__(self, l):
        t_year = 2000 + int(l[2:4])
        t_month = int(l[4:6])
        t_day = int(l[6:8])
        t_hour = int(l[9:11])
        t_minute = int(l[11:13])

        self.datetime = datetime.datetime(
            t_year, t_month, t_day, t_hour, t_minute)
        self.magnetic_classification = l[20:24].strip()

        arno_str = l[33:38]
        if arno_str == " ////":
            self.noaa_arno = None
        else:
            self.noaa_arno = int(arno_str)


        self.area = float(l[48:52])

class ActiveRegion:
    def __init__(self, noaa_arno, srdata):
        # NOAA Active Region Number
        self.noaa_arno = noaa_arno

        # The history of area by day
        daily_area = {}
        for r in srdata:
            t = r.datetime.date()
            if t in daily_area:
                daily_area[t].append(r.area)
            else:
                daily_area[t] = [r.area]
        self.area_history = {}
        for t,xs in daily_area.items():
            self.area_history[t] = np.median(xs)

def read_solar_region_report(fn):
    ret = []
    with open(fn,"r") as fp:
        for l in fp.readlines():
            ret.append(SolarRegionData(l))
    return ret

region_data = read_solar_region_report("usaf_solar-region-reports_2014.txt")

# debug print the region data read
# for r in region_data:
#     pprint(vars(r))

# sort the data by NOAA_ARNO
data_by_arno = {}
for r in region_data:
    noaa_arno = r.noaa_arno
    if noaa_arno is None:
        continue
    if noaa_arno in data_by_arno:
        data_by_arno[noaa_arno].append(r)
    else:
        data_by_arno[noaa_arno] = [r]

ar_data = {}
for noaa_arno, data in data_by_arno.items():
    ar_data[noaa_arno] = ActiveRegion(noaa_arno, data)

for noaa_arno, ar in sorted(ar_data.items()):
    print("NOAA_ARNO: ", noaa_arno)
    pprint(vars(ar))
