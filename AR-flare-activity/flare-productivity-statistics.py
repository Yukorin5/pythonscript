#!/usr/bin/env python3

import datetime
import matplotlib.pyplot as plt
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
        self.magnetic_class = l[20:24].strip()

        arno_str = l[33:38]
        if arno_str == " ////":
            self.noaa_arno = None
        else:
            self.noaa_arno = int(arno_str)

        self.area = float(l[48:52])


def read_solar_region_report(fn):
    ret = []
    with open(fn, "r") as fp:
        for l in fp.readlines():
            ret.append(SolarRegionData(l))
    return ret


class GoesFlareData:
    def __init__(self, l):
        arno_str = l[80:85]
        if arno_str.strip() == "":
            self.noaa_arno = None
        else:
            self.noaa_arno = int(arno_str)

        flareclass = l[59:60]
        peak_flux_base = {
            "A": 1e-8, "B": 1e-7, "C": 1e-6, "M": 1e-5, "X": 1e-4}
        peak_flux_modifier = float(l[60:63]) / 10.0

        self.peak_flux = peak_flux_base[flareclass] * peak_flux_modifier


def read_goes_xrs_report(fn):
    ret = []
    with open(fn, "r") as fp:
        for l in fp.readlines():
            ret.append(GoesFlareData(l))
    return ret



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

        self.magnetic_classes = set()
        self.magnetic_class_count = {}
        for r in srdata:
            c = r.magnetic_class
            self.magnetic_classes.add(c)
            if c in self.magnetic_class_count:
                self.magnetic_class_count[c] += 1
            else:
                self.magnetic_class_count[c] = 1

        self.magnetic_class_majority = max([(n,c) for c,n in self.magnetic_class_count.items()])[1]

        self.flares = []

    def total_area(self):
        # in units of millionths of solar hemisphere times day

        ret = 0
        for _, a in self.area_history.items():
            ret += a
        return ret

    def total_flare(self):
        # in units of C-class flare equivalent counts
        ret = 0
        for f in self.flares:
            ret += f.peak_flux
        return ret * 1e6

    def plot_size(self):
        return 20+4*len(self.flares)

    def plot_color(self):
        return self.plot_color_by_magnetic_class_majority()

    def plot_color_by_magnetic_class_history(self):
        for c in self.magnetic_classes:
            if "D" in c:
                return "red"
        for c in self.magnetic_classes:
            if "G" in c:
                return "yellow"
        for c in self.magnetic_classes:
            if "B" in c:
                return "lime"
        return "blue"

    def plot_color_by_magnetic_class_majority(self):
        c = self.magnetic_class_majority
        if "D" in c:
            return "red"
        if "G" in c:
            return "yellow"
        if "B" in c:
            return "lime"
        return "blue"


    def plot_color_by_flare_class(self):
        biggest = max([0] + [f.peak_flux for f in self.flares])
        if biggest >= 1e-4:
            return "red"
        elif biggest >= 1e-5:
            return "green"
        else:
            return "blue"


region_data = read_solar_region_report("usaf_solar-region-reports_2014.txt")

# # debug print the region data read
# for r in region_data:
#     pprint(vars(r))

flare_data = read_goes_xrs_report("goes-xrs-report_2014.txt")

# # debug print the region data read
# for r in flare_data:
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

# # debug print AR
# for noaa_arno, ar in sorted(ar_data.items()):
#     print("NOAA_ARNO: ", noaa_arno)
#     pprint(vars(ar))

for f in flare_data:
    if f.noaa_arno is not None:
        ar_data[f.noaa_arno].flares.append(f)

ar_list = [ar for _,ar in sorted(ar_data.items()) if ar.total_area()>0 and ar.total_flare() > 0]

xs = [ar.total_area() for ar in ar_list]
ys = [ar.total_flare() for ar in ar_list]
sizes = [ar.plot_size() for ar in ar_list]
colors = [ar.plot_color() for ar in ar_list]
plt.gca().set_xscale("log")
plt.gca().set_yscale("log")
plt.gca().set_xlabel("AR area in uSH day")
plt.gca().set_ylabel("Total Flares in C-class equivalent")
plt.scatter(xs,ys,sizes, colors, picker=True)

def onpick(event):
    for i in event.ind:
        ar = ar_list[i]
        for f in ar.flares:
            pprint(vars(f))
    for i in event.ind:
        ar = ar_list[i]
        print('NOAA_ARNO:', ar.noaa_arno, "area:", ar.total_area(), "flare:", ar.total_flare())
        print(ar.magnetic_class_count)

plt.gcf().canvas.mpl_connect('pick_event', onpick)

plt.show()
