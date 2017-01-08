#!/usr/bin/env python3

import datetime
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint
from solarreport import read_active_region_data


ar_data = read_active_region_data(2010, 2016)
ar_list = [ar for _,ar in sorted(ar_data.items()) if ar.integrated_area()>0 and ar.integrated_flare() > 0]


# Utility function for computing productivity for AR's half life
def half_productivity(ar, zenhan):
    dt = ar.time_end() - ar.time_begin()
    if zenhan:
        t0 = ar.time_begin()
        t1 = ar.time_begin() + dt/2
    else:
        t0 = ar.time_begin() + dt/2
        t1 = ar.time_end()
    ret = ar.integrated_flare(t0, t1) / ar.integrated_area(t0, t1)
    return max(1e-5, ret)

# Utility function for picking data
def onpick(event):
    for i in event.ind:
        ar = ar_list[i]
        print('NOAA_ARNO:', ar.noaa_arno, "area:", ar.integrated_area(), "flare:", ar.integrated_flare())
        print(ar.magnetic_class_count)
        print(",".join([f.class_string for f in ar.flares]))

interactive_mode = False

plt.rcParams["font.size"] = 24

# Plot the ARs' area and flare/day
xs = [ar.integrated_area() / ar.age_in_days() for ar in ar_list]
ys = [ar.integrated_flare() / ar.age_in_days() for ar in ar_list]
sizes = [ar.plot_size()/2 for ar in ar_list]
colors = [ar.plot_color_by_flare_class() for ar in ar_list]

# if the layout won't work
# imaxes = plt.gcf().add_axes([0.2, 0.2, 0.7, 0.7])
# plt.axes(imaxes)
plt.gca().set_xscale("log")
plt.gca().set_yscale("log")
plt.gca().set_xlabel("AR area (uSH)")
plt.gca().set_ylabel("Flare rate (C-class flare/day)")
plt.scatter(xs,ys,sizes, colors, picker=True)
plt.gcf().canvas.mpl_connect('pick_event', onpick)
plt.grid()
plt.tight_layout()

if interactive_mode:
    plt.show()
else:
    plt.savefig("figure/area_vs_flareperday.pdf",format="pdf")

plt.close("all")

# Plot the ARs' area*day and flare
xs = [ar.integrated_area() for ar in ar_list]
ys = [ar.integrated_flare() for ar in ar_list]
sizes = [ar.plot_size()/2 for ar in ar_list]
colors = [ar.plot_color_by_flare_class() for ar in ar_list]

plt.gca().set_xscale("log")
plt.gca().set_yscale("log")
plt.gca().set_xlabel("AR area (uSH day)")
plt.gca().set_ylabel("Flare count (C-class flare)")
plt.scatter(xs,ys,sizes, colors, picker=True)
plt.gcf().canvas.mpl_connect('pick_event', onpick)
plt.grid()
plt.tight_layout()

if interactive_mode:
    plt.show()
else:
    plt.savefig("figure/volume_vs_flares.pdf",format="pdf")

plt.close("all")

# Plot the AR's half productivity
xs = [half_productivity(ar,True) for ar in ar_list]
ys = [half_productivity(ar,False) for ar in ar_list]
sizes = [ar.plot_size() for ar in ar_list]
colors = [ar.plot_color_by_magnetic_class_history() for ar in ar_list]

plt.gca().set_xscale("log")
plt.gca().set_yscale("log")
plt.gca().set_xlabel("First-half flare productivity\n(C-class flare/uSH/day)")
plt.gca().set_ylabel("Second-half flare productivity\n(C-class flare/uSH/day)")
plt.scatter(xs,ys,sizes, colors, picker=True)
plt.gcf().canvas.mpl_connect('pick_event', onpick)
plt.grid()
plt.tight_layout()

if interactive_mode:
    plt.show()
else:
    plt.savefig("figure/productivity_fist_vs_second.pdf",format="pdf")
