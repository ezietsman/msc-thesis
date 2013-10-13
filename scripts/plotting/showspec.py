# plot the extracted spectra as trailed spectrogram and as a lightcurve. For testing

import pyfits as p
import os
import pylab as pl

files = os.listdir(os.curdir)
del files[len(files)-1]

pl.figure(figsize=(12,12))

i = 0
pl.figure(1)
pl.figure(2)
pl.figure(3)

image = pl.zeros((336,1024))
lc = []

for fits in files:
    name, ext = os.path.splitext(fits)
    
    if ext == '.fits':
        im = p.getdata(fits)
        lc.append(sum(im[0,:]))
        pl.plot(im[0,:])
        image[i,:] = im[0,:]
        i += 1

pl.figure(1)
pl.gray()
pl.imshow(image,vmin=0,vmax=600)


pl.figure(2)
pl.plot(lc)


pl.show()