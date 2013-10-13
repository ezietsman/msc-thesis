# Read output files and make spectrogram


import pylab as pl
import pyfits as pf
import os


#eP20060817%04d%s.0001.fits' % (i,ccd)


files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)

pl.figure(figsize=(12,12))
im = []
k = 0
for i in ff:
    data = pf.getdata(i)
    head = pf.getheader(i)
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    x = start + pl.arange(0,length)*step
    print i
    pl.plot(x,data+k,'k-')
    k += 1e-14
    

pl.show()

pf.writeto('specgram.fits',pl.array(im),clobber=True)



