#!/usr/bin/python

# Make a FT of every wavelength (column pixel) 
import pylab as pl
import pyfits as pf
import astronomy as ast
import scipy.signal as sci
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
    s1 = 6000
    s2 = 7000
    w1 = xx > s1
    w2 = xx < s2
    data = pf.getdata(spec)
    t.append(head['HJD'])
    specgram.append(pf.getdata(spec)[w1*w2])
    

allspec = None

specgram = pl.array(specgram)
t = pl.array(t)

print pl.shape(specgram)
for i in range(pl.shape(specgram)[1]):
    x = specgram[:,i]
    # flatten lightcurve using fourier method
    #fft = sci.fft(x)
    #fft[0:5] = 0.0
    #fft[-5:] = 0.0
    #x = sci.ifft(fft)
    f,a = ast.signal.dft(t,x,3000.,4000.0,1.0)
    trailed_ft.append(a)
    print i 


trailed_ft = pl.array(trailed_ft)
# get average and sigma of image then use those values to clip colortable
ave = trailed_ft.mean()
std = pl.std(trailed_ft)



pl.figure()
pl.imshow(trailed_ft,aspect='auto',\
cmap=pl.cm.jet,vmin=0,vmax=ave+5*std,extent=(0.0,4000.0,s1,s2),origin='lower')
#pl.gray()
pl.colorbar()
pl.xlabel('Frequency (c/d)')
pl.ylabel('Wavelength')
pl.title('Trailed Fourier Transform')



pl.savefig('trailed_ft2.png')
pl.show()