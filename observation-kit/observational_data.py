#!/usr/bin/env python
# -*- coding: utf-8 -*-

import astropy.time as time
import calendar, datetime, os, re, requests, subprocess,urllib, sys, StringIO
import numpy as np
from astropy.io import fits


global goes_raw_data_fast
goes_raw_data_fast = None
# 時刻t0におけるgoes X線フラックスの値を返します。
# １時間ごとの精度しかありませんが、高速です
def goes_flux(t0):
    global goes_raw_data_fast
    if goes_raw_data_fast is None:
        goes_raw_data_fast = {}
        with open("goes-data-12min.txt","r") as fp:
            for l in iter(fp.readline, ''):
                ws = l.split()
                t = datetime.datetime.strptime(ws[0],"%Y-%m-%dT%H:%M")
                x = float(ws[1])
                goes_raw_data_fast[t] = x
    t=datetime.datetime(t0.year,t0.month,t0.day,t0.hour)
    if t in goes_raw_data_fast:
        return goes_raw_data_fast[t]
    return 1e-8

# 時刻t0におけるgoes X線フラックスの値を返します。
# １時間ごとの精度しかありませんが、高速です
def goes_max(t, timedelta):
    ret = goes_flux(t)
    dt = datetime.timedelta(0)
    while dt <= timedelta:
        ret = max(ret, goes_flux(t + dt))
        dt += datetime.timedelta(minutes=12)
    return ret



