#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import datetime as T
import json, urllib, numpy as np, matplotlib.pylab as plt, matplotlib.ticker as mtick,cPickle as pickle,subprocess,sys
import sunpy.map
from astropy.io import fits
from sunpy.cm import color_tables as ct
import sunpy.wcs as wcs
import matplotlib.dates as mdates
import matplotlib.colors as mcol
import matplotlib.patches as ptc
from matplotlib.dates import *
import math


harp_num = int(sys.argv[1])
wavelengths=[94,193,1600]
channels=["hmi"]+wavelengths


def vmin_of_channel(c):
    if c=="hmi": return -300
    return 0

def vmax_of_channel(c):
    if c=="hmi": return 300
    if c==94: return 100
    if c==193: return 3000
    if c==1600: return 200
    return None


starting_index=0
if len(sys.argv)>=3:
    starting_index = int(sys.argv[2])



def archive_path_of_channel(c):
    if c=="hmi":
        return "HARP{}-hmi/".format(harp_num, c)
    return "HARP{}-aia{:04}/".format(harp_num, c)

archive_index = {}
for c in channels:
    print "loading",c
    archive_index[c] = pickle.load(open(archive_path_of_channel(c)+"index.pickle"))


for c in channels:
    movie_path = "frames-"+archive_path_of_channel(c)
    subprocess.call("mkdir -p " + movie_path, shell=True)

    image_idx = -1
    for frame in archive_index[c]:
        print c, image_idx
        image_idx += 1
        file_path = archive_path_of_channel(c) + frame["filename"]

        subdata = np.load(file_path)["img"]

        if c=="hmi":
            sdoaia_cmap = plt.get_cmap('hmimag')
        else:
            sdoaia_cmap = plt.get_cmap('sdoaia{}'.format(c))
        plt.imshow(subdata,cmap=sdoaia_cmap,origin='lower',vmin=vmin_of_channel(c),vmax=vmax_of_channel(c))
        print 'The dimensions of this image are',subdata.shape[0],'by',subdata.shape[1],'.'
        plt.title("HARP AR{} AIA {} Angstrom {}".format(harp_num, c, frame["t"]))
        cbaxes = plt.gcf().add_axes([0.8, 0.1, 0.03, 0.8])
        plt.colorbar(cax=cbaxes)
        plt.savefig(movie_path + "f{:06}.png".format(image_idx))
        plt.close("all")
