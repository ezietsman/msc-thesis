# Calculates the average of the lightcurves in the 'lightcurves' file 
# Time units are orbital phase

import pylab as pl
import string

files = open('lightcurves','r').readlines()
# Dict to hold ephemerides. '1' -> Archive,   '2' -> August, 'P' -> Period
ephemeris = {}
ephemeris['1'] = 2452525.374416
ephemeris['2'] = 2453964.330709

pl.figure()

xx = []
yy = []

for f in files:
    print 'Reading %s ' % f
    name, eph = string.split(f)
    T0 = ephemeris[eph]
    P = 0.154525
    X = pl.load(name)
    x = (X[:,0] - T0)/P
    xx.append(x - int(x[0]))
    yt = X[:,1] + X[:,2]
    yt -= pl.average(yt)
    yy.append(yt)

# now sort observations in terms of orbital phase
xx = pl.array([i for i in pl.flatten(xx)])
yy = pl.array([i for i in pl.flatten(yy)])
arg = xx.argsort()
xx = xx[arg]
yy = yy[arg]

# limit orb phase to [0.8,1.2]
lt = xx < 1.2
gt = xx > 0.8
xx = xx[lt*gt]
yy = yy[lt*gt]

# average lightcurve in N bins
N = 40

# try-except block takes away points at the end of the array if array cannot be split in N equal parts
try:
    xx = pl.average(pl.split(xx,N),1)
    yy = pl.average(pl.split(yy,N),1)
except:
    l = int(len(xx)/N)*N
    xx = pl.average(pl.split(xx[0:l],N),1)
    yy = pl.average(pl.split(yy[0:l],N),1)

# save the lightcurve
temp = []
temp.append(xx)
temp.append(yy)
pl.save('ave_lightcurve.dat',pl.array(temp).transpose())

pl.plot(xx,yy,'.')
pl.show()


