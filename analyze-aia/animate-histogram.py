#!/usr/bin/env python

import math, random, os, sys, re, subprocess
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

if len(sys.argv) <= 1:
    print "usage: {} FOLDER_NAMES".format(sys.argv[0])
    exit()

workdir = sys.argv[1]

# list all files in the workdir.
allfns = os.listdir(workdir)

fns = []

# append filenames to list variable fns,
for fn in allfns:
    # for only fn that ends with '.fits' .
    if re.search('\.fits$', fn):
        fns.append(workdir + '/' +fn)

# sort the files alphabetically.
fns =  sorted(fns)

for fn in fns:
    pngfn = re.sub('\.fits$', '.png', fn)
    print "plotting histogram: ", fn , '->' , pngfn

    h = fits.open(fn)
    h[1].verify('fix')
    exptime = h[1].header['EXPTIME']
    if exptime <=0:
        print "Warning: non-positive EXPTIME: ", h[1].header['EXPTIME']
        exptime = 2.0

    # adjust the pixel luminosity with the exposure time.
    img = h[1].data / exptime
    fig,ax = plt.subplots()

    one_frame = plt.hist(img.flat, range(0,20000,200), log = True, color='blue')
    ax.set_title(fn)
    ax.set_xlim([0,20000])
    plt.savefig(pngfn, dpi=100)
    plt.close('all')

print "creating animation."
subprocess.call('convert -loop 1 -delay 20 {}/*.png aia.mpeg'.format(workdir),shell = True)
