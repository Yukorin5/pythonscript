#!/usr/bin/env python

import math, random, os, sys, re, subprocess
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

def system_call(cmd):
    print cmd
    subprocess.call(cmd, shell = True)

if len(sys.argv) <= 1:
    print "usage: {} FOLDER_NAMES".format(sys.argv[0])
    exit()

workdirs = sys.argv[1:]

fns = []

pngdirs = []

# list all files in the workdir.
for workdir in workdirs:
    for root, dirnames, filenames in os.walk(workdir):
        for fn in filenames:
            if re.search('\.fits$', fn):
                fns.append(root + '/' +fn)
                if root not in pngdirs:
                    pngdirs.append(root)

pngdirs = sorted(pngdirs)
print "pngdirs:", pngdirs

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
    ax.set_xlim([1,1e8])
    plt.savefig(pngfn, dpi=100)
    plt.close('all')

print "creating animation."

target_file_patterns = [dir + '/*.png' for dir in pngdirs]
system_call('convert -loop 1 -delay 20 {} aia.mpeg'.format(' '.join(target_file_patterns)))
