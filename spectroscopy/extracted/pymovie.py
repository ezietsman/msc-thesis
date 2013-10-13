# make movie of the spectra :-)

import pyfits as pf
import pylab as pl



for i in range(61,395):
    print i
    data = pf.getdata('fec2117_%04d.fits'%i)
    head = pf.getheader('fec2117_%04d.fits'%i)
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    
    x = start + pl.arange(0,length)*step
    pl.plot(x,data)
    pl.ylim(0,5e-14)
    pl.savefig('png%04d.png'%i)
    pl.clf()




import os
# encode the movie
os.system("mencoder 'mf://*.png' -mf type=png:fps=15 -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o animation.mpg")