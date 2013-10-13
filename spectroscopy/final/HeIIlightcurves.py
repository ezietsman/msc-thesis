import pyfits as pf
import pylab as pl
import os
import astronomy as ast
import scipy.stats as stats
import scipy.signal as sci
#import astronomy as ast

# Read the spectra from the disk
files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)


# Get the wavelength to pixel info from the first fits header
head = pf.getheader(ff[0])
start = float(head['CRVAL1'])
step = float(head['CDELT1'])
length = float(head['NAXIS1'])
x = start + pl.arange(length)*step


T0 = 2453964.3307097
P = 0.1545255

date = []
phase = []

# read the julian dates and convert to orbital phase
print 'Calculating phase...\n'
for i in range(len(ff[:-2])):
    temp = float(pf.getheader(ff[i])['HJD'])
    date.append(temp)
    phase.append((temp-T0)/P)
print '...Done!\n'

phase = pl.array(phase)
date = pl.array(date)

flux = []
        

        
for i in range(len(date)):
    lt = x < 4687
    gt = x > 4686
    flux.append((pf.getdata(ff[i])[lt*gt]).sum())
    


flux = pl.array(flux)

temp = []
temp.append(date)
temp.append(phase)
temp.append(flux)

pl.save('HeIIlightcurve.dat',pl.array(temp).transpose())

lt = phase < 7.9

date = date[lt]
flux = pl.array(flux)[lt]
phase = pl.array(phase)[lt]
# flatten lightcurve using fourier method
fft = sci.fft(flux)
fft[0:4] = 0.0
fft[-4:] = 0.0
flux = sci.ifft(fft)

f,a = ast.signal.dft(date,flux,0,4000,1)
pl.figure()
pl.subplot(211)
pl.plot(phase,flux)
#pl.ylim(-5e-8,5e-8)
pl.subplot(212)
pl.plot(f,a)
sort,argsort = stats.fastsort(a)
print 'Max amplitude of %s at %s' % (a[argsort[-1]],f[argsort[-1]])
#print 'Second highest amplitude of %s at %s' % (a[argsort[-2]],f[argsort[-2]])
pl.show()


