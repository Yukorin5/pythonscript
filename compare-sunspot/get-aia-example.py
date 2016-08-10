#!/usr/bin/env python
import argparse,subprocess
import astropy.time as time
import datetime


parser = argparse.ArgumentParser(description='JSOC Downloader and converter')
parser.add_argument('--mail-address', '-m', type=str,
                    help='mail address registered at JSOC')
args = parser.parse_args()


t_begin = time.Time('2015-05-09 00:00',scale='tai', format='iso').datetime

series_name = "aia.lev1_euv_12s"
#series_name = "hmi.M_720s_nrt"

#wavelnths='[94,131,171,193,211,304,335]'
wavelnths='[94,193]'

batch_days=3
query = series_name + '[{}/{}d@720s]{}'.format(t_begin.strftime('%Y.%m.%d_%H:%M:%S'),batch_days,wavelnths)


command = "./exportfile.csh '"+query+ "' " + args.mail_address

print command
