import calendar
import datetime
import urllib.request as request

print("yyyy | mm | active goes")
for y in range(1986,2017):
    for m in range(1,13):
        buf = "{} | {:02} |".format(y,m)
        for goes_id in range(6,16):
            t0 = datetime.datetime(y,m,1,0,0,0)
            day31 = calendar.monthrange(t0.year,t0.month)[1]
            fn = 'g{gid:02}_xrs_1m_{y:4}{m:02}{d:02}_{y:4}{m:02}{d31:02}.csv'.format(y=t0.year, m=t0.month, d=1, d31=day31, gid = goes_id)
            url = 'http://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/{y}/{m:02}/goes{gid:02}/csv/'.format(y=t0.year, m=t0.month, gid = goes_id) + fn
            req = None
            try:
                req = request.urlopen(url)
                buf += " {}".format(goes_id)
            except:
                pass
            if req is not None:
                with open("xray-{}-{:02}-goes{:02}.csv".format(y,m,goes_id),"w") as fp:
                    fp.buffer.write(req.read())
        print(buf)
