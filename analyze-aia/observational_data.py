#!/usr/bin/env python
# module for loading observational data.

import datetime

def cmd(str):
    print str
    subprocess.call(str, shell = True)


def aia193(t):
    ymd = t.strftime('%Y/%m/%d')
    datapath = "data/" + ymd
    fn=datapath + t.strftime('/%H%M.fits')

    if not(os.path.exists(data_path)):
        cmd('aws s3 sync s3://sdo/aia193/720s/{}/ {}/ --region=us-west-2'.format(ymd,datapath))
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
