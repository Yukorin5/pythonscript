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
import os

harp_num = int(sys.argv[1])
wavelengths=[94,193,1600]
channels=["hmi"]+wavelengths
ufcorin_bigdata_path = os.environ.get("ufcorin_bigdata_path")
plt.rcParams['figure.figsize']=(16.0, 9.0)

def name_of_channel(c):
    if c=="hmi": return "hmi"
    return "aia{:04}".format(c)

def vmin_of_channel(c):
    if c=="hmi": return -300
    return 0

def vmax_of_channel(c):
    if c=="hmi": return 300
    if c==94: return 30
    if c==193: return 3000
    if c==1600: return 200
    return None


starting_index=0
if len(sys.argv)>=3:
    starting_index = int(sys.argv[2])



def archive_path_of_channel(c):
    if c=="hmi":
        return ufcorin_bigdata_path + "/harp/{}/hmi/".format(harp_num)
    return ufcorin_bigdata_path + "/harp/{}/aia{:04}/".format(harp_num,c)

archive_index = {}
for c in channels:
    print "loading",c
    archive_index[c] = pickle.load(open(archive_path_of_channel(c)+"index.pickle"))


for c in channels:
    movie_path = "/scr/uframes/" # archive_path_of_channel(c) + "/frames/"
    subprocess.call("rm -rf " + movie_path, shell=True)
    subprocess.call("mkdir -p " + movie_path, shell=True)
    # path 0: determine the maximum frame size
    canvas_x = 0
    canvas_y = 0

    for frame in archive_index[c]:
        file_path = archive_path_of_channel(c) + frame["filename"]
        try:
            subdata = np.load(file_path)["img"]
        except:
            print sys.exc_info()
            print "file broken: ", file_path
            continue

        ssx, ssy = subdata.shape
        print 'The dimensions of this image are',ssx," by ",ssy,'.'
        canvas_x = max(canvas_x, ssx)
        canvas_y = max(canvas_y, ssy)


    # path 1: render the frames
    canvas=np.ndarray((canvas_x,canvas_y))
    image_idx = 0
    for frame in archive_index[c]:
        
        print c, image_idx
        file_path = archive_path_of_channel(c) + frame["filename"]
        
        try:
            subdata = np.load(file_path)["img"]
        except:
            print sys.exc_info()
            print "file broken: ", file_path
            continue

        canvas[:,:] = 0
        ssx, ssy = subdata.shape
        x = (canvas_x-ssx)/2
        y = (canvas_y-ssy)/2
        canvas[x:x+ssx,y:y+ssy] = subdata

        if c=="hmi":
            sdoaia_cmap = plt.get_cmap('hmimag')
        else:
            sdoaia_cmap = plt.get_cmap('sdoaia{}'.format(c))
        imaxes = plt.gcf().add_axes([0.1, 0.1, 0.7, 0.8])
        plt.axes(imaxes)
        plt.imshow(canvas,cmap=sdoaia_cmap,origin='lower',vmin=vmin_of_channel(c),vmax=vmax_of_channel(c))
        plt.title("HARP AR{} AIA {} Angstrom {}".format(harp_num, c, frame["t"]))
        cbaxes = plt.gcf().add_axes([0.85, 0.1, 0.03, 0.8])
        plt.colorbar(cax=cbaxes)
        frame_fn = movie_path + "f{:06}.png".format(image_idx)
        print frame_fn
        plt.savefig(frame_fn)
        plt.close("all")

        image_idx += 1
        """
        End of the loop for creating movie frames.
        """

    subprocess.call("ffmpeg -y -r 24 -i /scr/uframes/f%06d.png  -qscale 0 /work1/t2g-16IAS/harp-movie/harp-{}-{}.mp4".format(harp_num,name_of_channel(c)),shell=True)

