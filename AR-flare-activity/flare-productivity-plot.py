#!/usr/bin/env python3

import csv
import argparse
import datetime
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint
from solarreport import read_active_region_data

argparser = argparse.ArgumentParser(description='Analyze active region statistics')
argparser.add_argument("--productivity-mode",
                       action='store',
                       type=str,
                       default="qc",
                       help='{nc|nm|qc|qm}')

argparser.add_argument('--interactive',
    action='store_true',
    default=False,
    help='Perform interactive analysis')

argparser.add_argument('-x',
                       action='store',
                       type=str,
                       default="i-area",
                       help='X axis component')

argparser.add_argument('-y',
                       action='store',
                       type=str,
                       default="i-flare",
                       help='Y axis component')


args = argparser.parse_args()

ar_data = read_active_region_data(2010, 2016)

noaa_arno_to_harpnum_hash = {}

with open('data/all_harps_with_noaa_ars.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        h = int(row[0])
        for n in row[1:]:
            noaa_arno_to_harpnum_hash[int(n)] = h

def noaa_arno_to_harpnum(n):
    if n not in noaa_arno_to_harpnum_hash:
        return None
    return noaa_arno_to_harpnum_hash[n]

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



class Data:
    def __init__(self, data, label, scale = "log"):
        self.data = data
        self.label = label
        self.scale = scale


def make_plot(xaxis_tag, yaxis_tag, productivity_mode):
    # Utility function for picking data
    def onpick(event):
        for i in event.ind:
            ar = ar_list[i]

            print(
                'HARPNUM', noaa_arno_to_harpnum(ar.noaa_arno),
                'NOAA_ARNO:', ar.noaa_arno,
                "area:", ar.integrated_area(),
                "flare:", ar.integrated_flare(productivity_mode))
            print(ar.magnetic_class_count)
            print(",".join([f.class_string for f in ar.flares]))


    ar_list = [ar for _,ar in sorted(ar_data.items()) if ar.integrated_area()>0 and ar.integrated_flare(productivity_mode) > 0]

    def get_biggest(ar):
        return max([0] + [f.peak_flux for f in ar.flares])

    ar_list = sorted(ar_list, key = get_biggest)

    plt.rcParams["font.size"] = 24

    data_dict = {}
    data_dict["area"] = Data(
        [ar.integrated_area() / ar.age_in_days() for ar in ar_list],
        "AR area (uSH)"
    )
    data_dict["i-area"] = Data(
        [ar.integrated_area() for ar in ar_list],
        "AR area (uSH・day)"
    )
    data_dict["flare"] = Data(
        [ar.integrated_flare(productivity_mode) / ar.age_in_days() for ar in ar_list],
        "Flare productivity ({} flares / day)".format(productivity_mode)
    )
    data_dict["i-flare"] = Data(
        [ar.integrated_flare(productivity_mode) for ar in ar_list],
        "Flare productivity ({} flares)".format(productivity_mode)
    )
    data_dict["flare-1"] = Data(
        [half_productivity(ar,productivity_mode,True) for ar in ar_list],
        "First-half flare productivity\n({} flare/uSH/day)".format(productivity_mode)
    )
    data_dict["flare-2"] = Data(
        [half_productivity(ar,productivity_mode,False) for ar in ar_list],
        "Second-half flare productivity\n({} flare/uSH/day)".format(productivity_mode)
    )

    sizes = [ar.plot_size()/2 for ar in ar_list]
    colors = [ar.plot_color_by_flare_class() for ar in ar_list]

    x_data = data_dict[xaxis_tag]
    y_data = data_dict[yaxis_tag]

    plt.gca().set_xscale(x_data.scale)
    plt.gca().set_yscale(y_data.scale)
    plt.gca().set_xlabel(x_data.label)
    plt.gca().set_ylabel(y_data.label)
    plt.scatter(x_data.data,y_data.data,sizes, colors, picker=True)
    plt.gcf().canvas.mpl_connect('pick_event', onpick)
    plt.grid()
    plt.tight_layout()

    fn_str = "-".join([xaxis_tag, yaxis_tag, productivity_mode])

    if args.interactive:
        plt.show()
    else:
        plt.savefig("figure/{}.pdf".format(fn_str),format="pdf")
    plt.close("all")



"""
MAIN
"""

if args.interactive:
    make_plot(args.x, args.y, args.productivity_mode)
