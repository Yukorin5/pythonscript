#!/usr/bin/env python
import glob,sys,subprocess

paths = sys.argv[1:]

out_path = "".join(paths).replace("/","_")
subprocess.call(["mkdir","-p",out_path])

fnss = []
for p in paths:
    fnss.append(sorted(glob.glob(p+"/*.png")))

n = min([len(fns) for fns in fnss])

for i in range(n):
    out_fn = "{}/{:08}.png".format(out_path, i)
    i_fns = [fns[i] for fns in fnss]
    print i_fns
    subprocess.call(["convert"] + i_fns + ["+append", out_fn])


subprocess.call("ffmpeg -r 24 -i {}/%08d.png    -qscale 0 {}.mp4".format(out_path, out_path), shell=True)
