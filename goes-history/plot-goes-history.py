#!/usr/bin/env python
import matplotlib as mpl
mpl.use('Agg')
import astropy.time as time
import glob
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import os
import pickle
import sys

full_plot_mode = True
pickle_file = "final/history.pickle"
def load_goes(fn):
    sys.stderr.write("reading {}...\n".format(fn))
    ret = {}
    with (open(fn, "r")) as fp:
        while True:
            con = fp.readline()
            if con[0:5] == 'data:':
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
            if con == '':
                break
            ws = con.split(',')
            # t = time.Time(ws[0].split()[0]).datetime
            t = time.Time(ws[0]).datetime
            if fmt_mode == "oldls":
                if len(ws) > 1:
                    ret[t] = float(ws[1])
            elif fmt_mode == "oldsl":
                if len(ws) > 2:
                    ret[t] = float(ws[2])
            elif fmt_mode == "new":
                if len(ws) > 6:
                    ret[t] = float(ws[6])
            else:
                raise Exception("unknown format codename " + fmt_mode)
    return ret


history = {}

files = sorted(glob.glob("goes-data/xray-*.csv"))

if full_plot_mode:
    files2 = []
else:
    files2 = files
    for fn in files:
        if "1996" in fn:
            files2.append(fn)
if full_plot_mode and os.path.exists(pickle_file):
    with open(pickle_file, "rb") as fp:
        history = pickle.load(fp)
else:
    for fn in files2:
        h = load_goes(fn)
        for t, x in h.items():
            if t not in history:
                history[t] = x
            else:
                history[t] = max(x, history[t])

    with open("history.pickle", "wb") as fp:
        pickle.dump(history, fp, protocol=-1)

plt.rcParams['figure.figsize'] = (120, 6)

daysFmt = mdates.DateFormatter('%Y-%m-%d')
yearLoc = mdates.YearLocator()
monthLoc = mdates.MonthLocator()
plt.gca().xaxis.set_major_locator(yearLoc)
plt.gca().xaxis.set_major_formatter(daysFmt)
plt.gca().xaxis.set_minor_locator(monthLoc)
plt.gca().grid()
plt.gcf().autofmt_xdate()
plt.gca().set_title('GOES Flux')
plt.gca().set_xlabel('International Atomic Time')
plt.gca().set_ylabel(u'GOES Long[1-8Å] Xray Flux')
plt.gca().set_yscale('log')


plt.scatter(list(history.keys()), list(history.values()),
            marker='.', edgecolors="face")
plt.ylim([1e-9, 1e-3])
plt.savefig("history-of-goes.png", dpi=100)
plt.close('all')

# Watch out for following error
#
# reading xray-2010-06-goes14.csv...
# Traceback (most recent call last):
#   File "plot-goes-history.py", line 60, in <module>
#     h = load_goes(fn)
#   File "plot-goes-history.py", line 44, in load_goes
#     ret[t] = float(ws[6])
# IndexError: list index out of range
#
# The file is truncated!
#
# Full plot requires 180 minutes.
