#!/usr/bin/env python

import os
import subprocess

subprocess.call("mkdir -p data" ,shell=True)
os.chdir("data/")

subprocess.call("curl -O http://jsoc.stanford.edu/doc/data/hmi/harpnum_to_noaa/all_harps_with_noaa_ars.csv", shell=True)

for y in range(1990,2017):
    subprocess.call("curl -O https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/sunspot-regions/usaf_mwl/usaf_solar-region-reports_{}.txt".format(y), shell=True)
    subprocess.call("curl -O https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/goes-xrs-report_{}.txt".format(y), shell=True)
