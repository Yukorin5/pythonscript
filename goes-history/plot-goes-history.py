import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import astropy.time as time
import glob
import os
import sys


def load_goes(fn):
    sys.stderr.write("reading {}...\n".format(fn))
    ret = {}
    with (open(fn, "r")) as fp:
        while True:
            con = fp.readline()
            if con[0:5]=='data:':
                break
        fmtstr = fp.readline()

        if "time_tag,xl,xs" in fmtstr:
            fmt_mode = "oldls"
        elif "time_tag,xs,xl" in fmtstr:
            fmt_mode = "oldsl"
        elif "time_tag,A_QUAL_FLAG,A_NUM_PTS,A_AVG,B_QUAL_FLAG,B_NUM_PTS,B_AVG" in fmtstr:
            fmt_mode = "new"
        else:
            raise Exception("unknown fmt {} {}".format(fn, fmtstr))

        while True:
            con = fp.readline()
            if con=='':
                break
            ws = con.split(',')
            t = time.Time(ws[0]).datetime
            if fmt_mode == "oldls":
                ret[t] = float(ws[1])
            elif fmt_mode == "oldsl":
                ret[t] = float(ws[2])
            elif fmt_mode == "new":
                ret[t] = float(ws[6])
            else:
                raise Exception("unknown format codename " + fmt_mode)
    return ret

history = {}

files = sorted(glob.glob("xray-*.csv"))

files2 = [files[0], files[-1]]

for fn in files2:
    h = load_goes(fn)
    for t,x in h.items():
        if t not in history:
            history[t] = x
        else:
            history[t] = max(x, history[t])



plt.rcParams['figure.figsize'] = (20,1)

daysFmt  = mdates.DateFormatter('%Y-%m-%d')
yearLoc  = mdates.YearLocator()
monthLoc = mdates.MonthLocator()
plt.gca().xaxis.set_major_locator(yearLoc)
plt.gca().xaxis.set_major_formatter(daysFmt)
plt.gca().xaxis.set_minor_locator(monthLoc)
plt.gca().grid()
plt.gcf().autofmt_xdate()
plt.gca().set_title('GOES Flux')
plt.gca().set_xlabel('International Atomic Time')
plt.gca().set_ylabel(u'GOES Long[1-8Å] Xray Flux')

plt.savefig(fn_png, dpi=600)
plt.close('all')
