#!/usr/bin/env python3

import datetime
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint


class SolarRegionData:
    def __init__(self, century_year, l):
        t_year = century_year + int(l[2:4])
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


def read_solar_region_report(century_year, fn):
    ret = []
    with open(fn, "r") as fp:
        for l in fp.readlines():
            ret.append(SolarRegionData(century_year, l))
    return ret


class GoesFlareData:
    def __init__(self, century_year, l):
        t_year = century_year + int(l[5:7])
        t_month = int(l[7:9])
        t_day = int(l[9:11])
        try:
            t_hour = int(l[23:25])
            t_minute = int(l[25:27])
        except:
            t_hour = 0
            t_minute = 0

        self.datetime = datetime.datetime(
            t_year, t_month, t_day, t_hour, t_minute)

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
        self.class_string = flareclass + "{:02}".format(int(l[60:63]))


def read_goes_xrs_report(century_year, fn):
    ret = []
    with open(fn, "r") as fp:
        for l in fp.readlines():
            ret.append(GoesFlareData(century_year, l))
    return ret



class ActiveRegion:
    def __init__(self, noaa_arno, srdata):
        # NOAA Active Region Number
        self.noaa_arno = noaa_arno

        # The history of area by day
        daily_area = {}
        for r in srdata:
            # set t to be the beginning of that date
            t = r.datetime.date()
            t = datetime.datetime.combine(t, datetime.time())
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

    def time_begin(self):
        return min(self.area_history.keys())

    def time_end(self):
        return max(self.area_history.keys())

    def age_in_days(self):
        return (self.time_end() - self.time_begin()).days + 1

    def integrated_area(self, time_begin=None, time_end=None):
        # in units of millionths of solar hemisphere times day

        ret = 0
        for t, a in self.area_history.items():
            if time_begin is not None and t < time_begin:
                continue
            if time_end is not None and t > time_end:
                continue
            ret += a
        return ret

    def integrated_flare(self, time_begin=None, time_end=None):
        # in units of C-class flare equivalent counts
        ret = 0
        for f in self.flares:
            t = f.datetime
            if time_begin is not None and t < time_begin:
                continue
            if time_end is not None and t > time_end:
                continue
            ret += f.peak_flux
        return ret * 1e6

    def plot_size(self):
        return 20+4*len(self.flares)

    def plot_color(self):
        return self.plot_color_by_magnetic_class_history()

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
            return "lime"
        else:
            return "blue"


def read_active_region_data(year_begin, year_end):
    region_data = []
    flare_data = []

    # read the AR and flare observational data
    for y in range(year_begin, year_end):
        century_year = int(y/100)*100
        print("loading region", y)
        region_data += read_solar_region_report(century_year, "data/usaf_solar-region-reports_{}.txt".format(y))
        print("loading flare", y)
        flare_data += read_goes_xrs_report(century_year, "data/goes-xrs-report_{}.txt".format(y))

    # Sort the AR observation data and create `ar_data`,
    # which is the hash fron NOAA_ARNO to ActiveRegion
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

    # Append the flare data to their associated
    # active region
    for f in flare_data:
        if f.noaa_arno is not None and f.noaa_arno in ar_data:
            ar_data[f.noaa_arno].flares.append(f)

    return ar_data
