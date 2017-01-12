#!/usr/bin/env python3

import datetime
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint
from solarreport import read_active_region_data


ar_data = read_active_region_data(2010, 2016)


# Utility function for computing productivity for AR's half life
def half_productivity(ar, productivity_mode, zenhan):
    dt = ar.time_end() - ar.time_begin()
    if zenhan:
        t0 = ar.time_begin()
        t1 = ar.time_begin() + dt/2
    else:
        t0 = ar.time_begin() + dt/2
        t1 = ar.time_end()
    ret = ar.integrated_flare(productivity_mode, t0, t1) / ar.integrated_area(t0, t1)
    return max(1e-5, ret)

# Utility function for picking data
def onpick(event):
    for i in event.ind:
        ar = ar_list[i]
        print('NOAA_ARNO:', ar.noaa_arno, "area:", ar.integrated_area(), "flare:", ar.integrated_flare())
        print(ar.magnetic_class_count)
        print(",".join([f.class_string for f in ar.flares]))

interactive_mode = False

for productivity_mode in ["nc","nm","qc","qm"]:
    ar_list = [ar for _,ar in sorted(ar_data.items()) if ar.integrated_area()>0 and ar.integrated_flare(productivity_mode) > 0]

    plt.rcParams["font.size"] = 24

    # Plot the ARs' area and flare/day
    xs = [ar.integrated_area() / ar.age_in_days() for ar in ar_list]
    ys = [ar.integrated_flare(productivity_mode) / ar.age_in_days() for ar in ar_list]
    sizes = [ar.plot_size()/2 for ar in ar_list]
    colors = [ar.plot_color_by_flare_class() for ar in ar_list]

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
        plt.savefig("figure/{}-area_vs_flareperday.pdf".format(productivity_mode),format="pdf")

    plt.close("all")

    # Plot the ARs' area*day and flare
    xs = [ar.integrated_area() for ar in ar_list]
    ys = [ar.integrated_flare(productivity_mode) for ar in ar_list]
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
        plt.savefig("figure/{}-volume_vs_flares.pdf".format(productivity_mode),format="pdf")

    plt.close("all")

    # Plot the ARs' productivity and area
    xs = [ar.integrated_area() / ar.age_in_days() for ar in ar_list]
    ys = [ar.integrated_flare(productivity_mode) / ar.integrated_area() for ar in ar_list]
    sizes = [ar.plot_size()/2 for ar in ar_list]
    colors = [ar.plot_color_by_flare_class() for ar in ar_list]

    plt.gca().set_xscale("log")
    plt.gca().set_yscale("log")
    plt.gca().set_xlabel("AR area (uSH)")
    plt.gca().set_ylabel("Flare productivity\n(C-class flare/uSH/day)")
    plt.scatter(xs,ys,sizes, colors, picker=True)
    plt.gcf().canvas.mpl_connect('pick_event', onpick)
    plt.grid()
    plt.tight_layout()

    if interactive_mode:
        plt.show()
    else:
        plt.savefig("figure/{}-area_vs_productivity.pdf".format(productivity_mode),format="pdf")

    plt.close("all")


    # Plot the ARs' productivity and being specific class
    for c_letter in "ABGD":
        xs = [ar.magnetic_class_fraction(c_letter) for ar in ar_list]
        ys = [ar.integrated_flare(productivity_mode) / ar.integrated_area() for ar in ar_list]
        sizes = [ar.plot_size()/2 for ar in ar_list]
        colors = [ar.plot_color_by_flare_class() for ar in ar_list]

        plt.gca().set_xscale("linear")
        plt.xlim([-0.01,1])
        plt.gca().set_yscale("log")
        plt.gca().set_xlabel("The class({}) fraction".format(c_letter))
        plt.gca().set_ylabel("Flare productivity\n(C-class flare/uSH/day)")
        plt.scatter(xs,ys,sizes, colors, picker=True)
        plt.gcf().canvas.mpl_connect('pick_event', onpick)
        plt.grid()
        plt.tight_layout()

        if interactive_mode:
            plt.show()
        else:
            plt.savefig("figure/{}-class_{}_fraction_vs_productivity.pdf".format(productivity_mode,c_letter),format="pdf")

        plt.close("all")


    # Plot the AR's half productivity
    def get_biggest(ar):
        return max([0] + [f.peak_flux for f in ar.flares])

    ar_list2 = sorted(ar_list, key = get_biggest)

    xs = [half_productivity(ar,productivity_mode,True) for ar in ar_list2]
    ys = [half_productivity(ar,productivity_mode,False) for ar in ar_list2]
    sizes = [ar.plot_size() for ar in ar_list2]
    colors = [ar.plot_color_by_flare_class() for ar in ar_list2]



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
        plt.savefig("figure/{}-productivity_fist_vs_second.pdf".format(productivity_mode),format="pdf")
    plt.close("all")
