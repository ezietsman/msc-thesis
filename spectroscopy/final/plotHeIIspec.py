# try to see the diagnoal striations  in the HeII line between phase 7.8 and 7.9

import pylab as pl
import pyfits as pf
import os

files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)



# calculate phase based on eclipse ephemeris
T0 = 2453964.3307097
P = 0.1545255



imHa = []
imHb = []
imHe = []
phase = []
ave = pf.getdata('aveEC2117.fits')


# calculate phase for every spectrum and assign number to it
print 'Calculating phase...\n'
phase = pl.array([((float(pf.getheader(ff[i])['HJD']) - T0)/P) for i in range(len(ff))[:-2]])
print '...Done!\n'

section = phase < 10
v = 10000
c = 2.99792458e5



head = pf.getheader(ff[0])
start = head['CRVAL1']
step = head['CDELT1']
length = head['NAXIS1']
x = start + pl.arange(0,length)*step

dl = v/c*4686
w1 = x > 4686 - dl
w2 = x < 4686 + dl

for i in range(len(ff))[:-2]:
    print i
    if phase[i] < 7.9:
        pl.plot(x[w1*w2],pf.getdata(ff[i])[w1*w2]+i*0.5e-8,'k-')
        #pl.savefig('HeII%04d.png'%i)
        #pl.clf()

pl.show()
