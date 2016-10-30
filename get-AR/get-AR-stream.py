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
plot_mode = False

def cadence_of_wavelength(w):
    # c.f. http://jsoc.stanford.edu/new/AIA/AIA_lev1.html
    if w < 1000:
        return 12
    if w <= 1700:
        return 24
    return 3600

def vmax_of_wavelength(w):
    if w==94: return 100
    if w==193: return 3000
    if w==1600: return 200
    return None


url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=hmi.sharp_720s[{}][]&op=rs_list&key=T_REC,CRPIX1,CRPIX2,CROTA2,CDELT1&seg=magnetogram".format(harp_num)

response = urllib.urlopen(url)
sharp_data = json.loads(response.read())
num_images = len(sharp_data['segments'][0]['values'])

starting_index=0
if len(sys.argv)>=3:
    starting_index = int(sys.argv[2])

subdata_archive = {}
for c in channels:
    subdata_archive[c] = []
def archive_path_of_channel(c):
    if c=="hmi":
        return "HARP{}-hmi/".format(harp_num, c)
    return "HARP{}-aia{:04}/".format(harp_num, c)


hmi_archive_path = archive_path_of_channel("hmi")
subprocess.call("mkdir -p " + hmi_archive_path, shell=True)


for image_idx in range(starting_index,num_images):
    print image_idx, "/", num_images

    T_REC      = sharp_data['keywords'][0]['values'][image_idx]
    CRPIX1_CCD = float(sharp_data['keywords'][1]['values'][image_idx])
    CRPIX2_CCD = float(sharp_data['keywords'][2]['values'][image_idx])
    CROTA2_CCD = float(sharp_data['keywords'][3]['values'][image_idx])
    CDELT1_CCD = float(sharp_data['keywords'][4]['values'][image_idx])
    XDIM_CCD = float(sharp_data['segments'][0]['dims'][image_idx].rsplit('x', 1)[0])
    YDIM_CCD = float(sharp_data['segments'][0]['dims'][image_idx].rsplit('x', 1)[1])

    ccd_x1 = int(2048. + CRPIX2_CCD - YDIM_CCD)
    ccd_x2 = int(2048. + CRPIX2_CCD)
    ccd_y1 = int(2048. + CRPIX1_CCD - XDIM_CCD)
    ccd_y2 = int(2048. + CRPIX1_CCD)
    time_recorded = T.datetime.strptime(T_REC, '%Y.%m.%d_%H:%M:%S_TAI')

    for c in ["hmi"]:
        filename = sharp_data['segments'][0]['values'][image_idx]
        url = "http://jsoc.stanford.edu"+filename
        try:
            photosphere_image = fits.open(url)        # download the data
        except Exception as e:
            print "Error downloading HMI image, ", T_REC
            print e.message
            continue
        if (CROTA2_CCD > 5.0):
            print "The HMI camera rotation angle is",CROTA2_CCD,". Rotating HMI images."
            photosphere_image[1].data = np.rot90(photosphere_image[1].data,2)

        subdata_filename = "f{:06}.npz".format(image_idx)
        subdata_frame = {
            't' : time_recorded,
            'x1' : ccd_x1,
            'x2' : ccd_x2,
            'y1' : ccd_y1,
            'y2' : ccd_y2,
            'filename' : subdata_filename
        }
        subdata_archive["hmi"].append(subdata_frame)
        file_path = hmi_archive_path + subdata_filename
        subdata = np.nan_to_num(photosphere_image[1].data).astype(np.float32)
        np.savez_compressed(file_path, img=subdata)
        # pickle.dump(subdata, fp, protocol=-1)



    for wavelength in wavelengths:
        archive_path = archive_path_of_channel(wavelength)
        subprocess.call("mkdir -p " + archive_path, shell=True)

        cadence = cadence_of_wavelength(wavelength)
        url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=aia.lev1[{t}/{c}s][?WAVELNTH={w}?]&op=rs_list&key=T_REC,CROTA2,CDELT1,CDELT2,CRPIX1,CRPIX2,CRVAL1,CRVAL2&seg=image_lev1".format(t=T_REC, w=wavelength, c = cadence)

        try:
            response = urllib.urlopen(url)
            aia_data = json.loads(response.read())
        except Exception as e:
            print "Error loading AIA metadata for WL = ", wavelength, "T = ", T_REC
            print e.message
            continue


        if not 'segments' in aia_data:
            print "No data for WL = ", wavelength, "T = ", T_REC
            continue

        filename = aia_data['segments'][0]['values'][0]
        url = "http://jsoc.stanford.edu"+filename
        try:
            aia_image = fits.open(url)   # download the data
        except Exception as e:
            print "Error loading AIA for WL = ", wavelength, "T = ", T_REC
            print e.message
            continue

        T_REC_AIA = aia_data['keywords'][0]['values'][0]
        CROTA2_AIA = float(aia_data['keywords'][1]['values'][0])
        CDELT1_AIA = float(aia_data['keywords'][2]['values'][0])
        CDELT2_AIA = float(aia_data['keywords'][3]['values'][0])
        CRPIX1_AIA = float(aia_data['keywords'][4]['values'][0])
        CRPIX2_AIA = float(aia_data['keywords'][5]['values'][0])
        CRVAL1_AIA = float(aia_data['keywords'][6]['values'][0])
        CRVAL2_AIA = float(aia_data['keywords'][7]['values'][0])

        ratio = (CDELT1_CCD)/(CDELT1_AIA)

        aia_image.verify("fix")
        exptime = aia_image[1].header['EXPTIME']
        if exptime <=0:
            print "Non-positive exptime for WL = ", wavelength, "T = ", T_REC_AIA
            continue

        aia_image[1].data /= exptime

        if (CROTA2_AIA > 5.0):
            print "The AIA camera rotation angle is",CROTA2_AIA,". Rotating AIA image."
            aia_image[1].data = np.rot90(aia_image[1].data,2)
        ccd_x1 = int(2048. + CRPIX2_CCD*(ratio) - YDIM_CCD*(ratio))
        ccd_x2 = int(2048. + CRPIX2_CCD*(ratio)+1)
        ccd_y1 = int(2048. + CRPIX1_CCD*(ratio) - XDIM_CCD*(ratio))
        ccd_y2 = int(2048. + CRPIX1_CCD*(ratio)+1)
        subdata = aia_image[1].data[ccd_x1:ccd_x2, ccd_y1:ccd_y2]

        time_recorded = T.datetime.strptime(T_REC_AIA, '%Y-%m-%dT%H:%M:%SZ')

        print "WL = ", wavelength, "T = ", time_recorded, "EXPTIME = ", exptime, "({}:{} , {}:{})".format(ccd_x1,ccd_x2, ccd_y1, ccd_y2)

        subdata_filename = "f{:06}.npz".format(len(subdata_archive[wavelength]))

        subdata_frame = {
            't' : time_recorded,
            'x1' : ccd_x1,
            'x2' : ccd_x2,
            'y1' : ccd_y1,
            'y2' : ccd_y2,
            'filename' : subdata_filename
        }
        subdata_archive[wavelength].append(subdata_frame)

        file_path = archive_path + subdata_filename
        np.savez_compressed(file_path, img=subdata)

        if plot_mode:
            sdoaia_cmap = plt.get_cmap('sdoaia{}'.format(wavelength))
            plt.imshow(subdata,cmap=sdoaia_cmap,origin='lower',vmin=0,vmax=vmax_of_wavelength(wavelength))
            print 'The dimensions of this image are',subdata.shape[0],'by',subdata.shape[1],'.'
            plt.title("HARP AR{} AIA {} Angstrom {}".format(harp_num, wavelength, T_REC_AIA))
            cbaxes = plt.gcf().add_axes([0.8, 0.1, 0.03, 0.8])
            plt.colorbar(cax=cbaxes)
            plt.savefig("frames/HARP{}-aia{:04}-f{:06}.png".format(harp_num, wavelength, image_idx))
            plt.close("all")

for c in channels:
    fn = archive_path_of_channel(c) + "index.pickle"
    with open(fn,"w") as fp:
        pickle.dump(subdata_archive[c], fp, protocol=-1)
