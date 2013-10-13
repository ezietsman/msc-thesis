# correct the spectroscopy using the smoothed lightcurve


import pylab as pl
import pyfits as pf
import os
import scipy.interpolate as sci

# read the spectra
files = os.listdir(os.curdir)
files.sort()
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)
        
# load the smoothed lightcurve
#X = pl.load('run2FF.dat')
X = pl.load('S7655_FF.dat')



x = X[:,0] - int(X[:,0][0])
y = X[:,2]


t = []
mag = []
mag2 = []

for f in ff:
    data = pf.getdata(f)
    head = pf.getheader(f)
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    wav = start + pl.arange(0,length)*step
    low = wav < 6040
    high = wav > 4980
    # mag contains V-band flux, mag2 contains total spec flux
    mag.append(data[high*low].sum())
    mag2.append(data.sum())
    t.append(float(head['HJD']))
    print f
    



mag = pl.array(mag)
# subtract Julian date integer
t = pl.array(t)-int(pl.array(t)[0])

# fit spline to smoothed lightcurve
tck = sci.splrep(x,y,k=3)
# calculate spline values at times of spectra
magnew = sci.splev(t,tck)


# get the scale factor between mnew and mag
#mnewflux = 10.0**(magnew/(-2.5))
#mnewflux = magnew
scale = mag/magnew







# now correct every spectrum and write to new fits file

os.system('rm -v corEC*')

for i in range(len(ff)):
    print 'Writing to %s' % ('cor'+ff[i])
    data = pf.getdata(ff[i])
    data /= scale[i]
    head = pf.getheader(ff[i])
    pf.writeto('cor'+ff[i],data,header=head)


# make some plots for the presentation

#scale = mag - magnew

pl.figure(figsize=(9,6))
T0 = 2453964.3307097
P = 0.1545255
x = (x+2453965.0-T0)/P

t = ((t + 2453965.0)-T0)/P
pl.plot(x,y,'.',label='Phot lightcurve')
pl.plot(t,mag2/scale,'r.',label='Total spec lightcurve')
pl.legend()

#yl = pl.ylim()
#pl.ylim(yl[1],yl[0])

pl.figure(figsize=(9,6))
pl.plot(x,y,'.',label='Phot lightcurve')
#pl.plot(t,-2.5*pl.log10(mag*scale),'r.')
pl.plot(t,mag/scale,'r.',label='V spec lightcurve')
pl.legend()
#yl = pl.ylim()
#pl.ylim(yl[1],yl[0])
pl.xlim(7.7,8.1)


pl.show()

