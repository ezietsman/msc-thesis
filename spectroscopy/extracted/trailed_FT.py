#!/usr/bin/python

# Make a FT of every wavelength (column pixel) 
import pylab as pl
import pyfits as pf
import astronomy as ast
import os

files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)

specgram = []
t = []
trailed_ft = []

for spec in ff[:-2]:
    
    head = pf.getheader(spec)
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    xx = start + pl.arange(0,length)*step
    # hydrogen alpha 
    w1 = xx > 6523
    w2 = xx < 6603
    data = pf.getdata(spec)
    t.append(head['HJD'])
    specgram.append(pf.getdata(spec)[w1*w2])
    

allspec = None

specgram = pl.array(specgram)
t = pl.array(t)

print pl.shape(specgram)
for i in range(pl.shape(specgram)[1]):
    x = specgram[:,i]
    f,a = ast.signal.dft(t,x,0.0,4000.0,1.0)
    trailed_ft.append(a)
    print i 


pl.figure()
pl.imshow(trailed_ft,aspect='auto',vmin=0,vmax=0.03e-14,\
cmap=pl.cm.jet,extent=(0.0,4000.0,6523,6603),origin='lower')
#pl.gray()
pl.colorbar()
pl.xlabel('Frequency (c/d)')
pl.ylabel('Wavelength')
pl.title('Trailed Fourier Transform')



pl.savefig('trailed_ft2.png')
pl.show()