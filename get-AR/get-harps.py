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

    print (["python", "get-AR-stream.py", harp])
    subprocess.call(["python", "get-AR-stream.py", harp])
    subprocess.call("scp -r harp/* tsubame:/work1/t2g-16IAS/harp/")
    subprocess.call("rm -rf harp/*")

    remains = harps[1:]

    with open("harps.txt","w") as fp:
        for h in remains:
            fp.write(h+"\n")
