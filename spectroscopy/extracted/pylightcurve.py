# make movie of the spectra :-)

import pyfits as pf
import pylab as pl
import os
import astronomy as ast


files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:5] == 'corEC':
        ff.append(f)

head = pf.getheader(ff[0])
start = float(head['CRVAL1'])
step = float(head['CDELT1'])
length = float(head['NAXIS1'])
x = start + pl.arange(length)*step
hi = x > 5000
low = x < 6000
xx = hi*low


lc = []
time = []

for f in ff:
    lc.append(sum(pf.getdata(f)[xx]))
    time.append(float(pf.getheader(f)['HJD']))

lc = -2.5*pl.log10(pl.array(lc))
time = pl.array(time)

#pl.show()

pl.subplot(212)
f,a = ast.signal.dft(time,lc,0,4000,1)
pl.plot(f,a)

pl.subplot(211)
pl.plot(time,lc,'.')
yl = pl.ylim()
pl.ylim(yl[1],yl[0])

#lc = pl.array(-2.5*pl.log10(lc)-20.84)
#time = pl.array(time)

temp = pl.zeros((len(lc),2),dtype='float')
for i in range(len(lc)):
    temp[i,0] = time[i]
    temp[i,1] = lc[i]

pl.save('speclc_yellow.dat',temp)
pl.show()

