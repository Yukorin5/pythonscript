#!/usr/bin/env python

import subprocess

while True:
    with open("harps.txt","r") as fp:
        txt=fp.read()
    harps = txt.split()

    if len(harps) == 0:
        print "done!"
        exit()

    harp = harps[0]
    remains = harps[1:]

    with open("harps.txt","w") as fp:
        for h in remains:
            fp.write(h+"\n")

    subprocess.call(["python", "get-AR-stable.py", harp])
    subprocess.call("scp -r harp/* tsubame:/work1/t2g-16IAS/harp/",shell=True)
    subprocess.call("rm -rf harp/*",shell=True)

