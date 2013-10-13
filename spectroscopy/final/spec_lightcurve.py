# Read output files and make lightcurve


import pylab as pl
import pyfits as pf
import os
import astronomy as ast 


# Read the spectra from the current directory
files = os.listdir(os.curdir)
files.sort()
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)


# calculate phase based on eclipse ephemeris
T0 = 2453964.3307097
P = 0.1545255


HJD = []
flux = []
for i in ff[:-2]:
    data = pf.getdata(i)
    head = pf.getheader(i)
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    x = start + pl.arange(0,length)*step
    w1 = x >= 3000
    w2 = x <= 8000
    HJD.append(head['HJD'])
    flux.append(data[w1*w2].sum())
    print i

HJD = pl.array(HJD)
p = (HJD-T0)/P
flux = pl.array(flux)
flux/=flux.mean()


pl.figure()
pl.subplot(211)
pl.plot(p,flux,'.')
pl.xlabel('Orbital Phase')
pl.ylabel('Flux (normalised)')

pl.subplot(212)
f,a = ast.signal.dft(HJD,flux,0,4000,1)
pl.plot(f,a)
pl.xlabel(r'Frequency $(Day^{-1})$')
pl.ylabel('Amplitude (intensity)')
pl.ylim(0,0.05)
#pl.savefig('specgram_full.png')


pl.save('speclightcurve.dat',pl.array([HJD,flux]).transpose())

pl.show()





