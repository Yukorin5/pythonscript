#!/usr/bin/env python
# module for loading observational data.

import calendar, datetime, os, subprocess
from astropy.io import fits

def cmd(str):
    print str
    subprocess.call(str, shell = True)

def aia193(t):
    ymd = t.strftime('%Y/%m/%d')
    data_path = "data/aia193/" + ymd
    fn=data_path + t.strftime('/%H%M.fits')

    if not(os.path.exists(data_path)):
        cmd('aws s3 sync s3://sdo/aia193/720s/{}/ {}/ --region=us-west-2'.format(ymd,data_path))
    if not(os.path.exists(fn)):
        return None

    h = fits.open(fn)
    h[1].verify('fix')
    exptime = h[1].header['EXPTIME']
    if exptime <=0:
        print "Warning: non-positive EXPTIME: ", h[1].header['EXPTIME']
        return None

    # adjust the pixel luminosity with the exposure time.
    return h[1].data / exptime

global goes_raw_data, goes_loaded_files
goes_raw_data = {}
goes_loaded_files = set()
def goes(t0):
    global goes_raw_data, goes_loaded_files
    if t0 in goes_raw_data:
        return goes_raw_data[t0]

    day31 = calendar.monthrange(t0.year,t0.month)[1]
    fn = 'g15_xrs_1m_{y:4}{m:02}{d:02}_{y:4}{m:02}{d31:02}.csv'.format(y=t0.year, m=t0.month, d=01, d31=day31)
    localpath = 'data/goes/' + fn
    if localpath in goes_loaded_files():
        return None

    if not(os.path.exist(localpath)):
        url = 'http://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/{y}/{m}/goes15/csv/'.format(y=t0.year, m=t0.month) + fn
        cmd('wget ' + url + ' -O ' + fn)
    if not(os.path.exist(localpath)):
        return None

    goes_loaded_files.add(localpath)
    with (open(localpath, "r")) as fp:
        while True:
            con = fp.readline()
            if con[0:5]=='data:':
                break
        fp.readline()

        while True:
            con = fp.readline()
            if con=='':
                break
            ws = con.split(',')
            t = time.Time(ws[0]).datetime
            goes_raw_data[t] = float(ws[6])

    return goes(t)
