# script to make flux lightcurve plots

import pylab as pl
import astronomy as ast

# ephemeris
T0 = 2453964.3307097
P = 0.1545255

X = pl.load('speclightcurve_FF.dat')
x = X[:,0]
p = (x-T0)/P
y = X[:,1]


pl.figure(figsize=(6,4))
pl.subplots_adjust(hspace=0.4,left=0.15,bottom=0.12)
pl.subplot(211)
pl.plot(p,y,'kx')
pl.xlabel('Orbital Phase')
pl.ylabel('Intensity')

pl.subplot(212)
f,a = ast.signal.dft(x,y,0,4000,1)
pl.plot(f,a,'k-')
pl.xlabel('Frequency (c/d)')
pl.ylabel('Amplitude')
pl.ylim(0.0,0.01)


pl.savefig('fluxlightcurve.png')

pl.show()