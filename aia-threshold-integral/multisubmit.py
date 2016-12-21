import subprocess

for t in range(0,10000,100):
    subprocess.call("./submit.sh {}".format(t), shell=True)
