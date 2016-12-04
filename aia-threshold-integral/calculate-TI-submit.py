import subprocess


for y in range(2011,2017):
    for m in range(1,13):
        cmd = "t2sub -q U -W group_list=t2g-16IAS -et 1 -p 1 -l walltime=12:00:00 -l mem=23gb -v UFCORIN_JOB_EPOCH={}-{:02}-01 ./calculate-TI-job.sh".format(y,m)
        print cmd
        subprocess.call(cmd, shell = True)
# -et : extend time
# -p : priority

