# plot the spectrum lightcurves

import pylab as pl


pl.figure()

X = pl.load('speclc_blue.dat')
pl.plot(X[:-2,0],X[:-2,1],'b.',label='Blue CCD')
X = pl.load('speclc_yellow.dat')
pl.plot(X[:-2,0],X[:-2,1],'g.',label='Yellow CCD')
X = pl.load('speclc_red.dat')
pl.plot(X[:-2,0],X[:-2,1],'r.',label='Red CCD')
yl = pl.ylim()
pl.ylim(yl[1],yl[0])
pl.ylabel('Magnitude')
pl.xlabel('Fractional Day')
pl.legend()
pl.show()