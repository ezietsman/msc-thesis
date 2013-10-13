# try to flatten lightcurves using Fourier Filter

import scipy.signal as sci
import pylab as pl
import os


X = pl.load('speclc_Ha.dat')
x = X[:,0]
y = X[:,1]



fft = sci.fft(y-pl.average(y))

l = len(fft)
dt = x[1]-x[0]

# kill the negative frequencies
#fft[l/2:] = 0.0

# kill the low frequency bits > ~ 1hour
k = int(24.0*l*dt)
print k

fft[0:5] = 0.0
fft[-5:] = 0.0

yy = sci.ifft(fft)


pl.subplot(311)
pl.plot(x,y,'.')

pl.subplot(312)
pl.plot(x,yy,'-')

pl.subplot(313)
pl.plot(x,y-yy,'.')

pl.show()

temp = []
temp.append(x)
temp.append(yy)
temp.append(y-yy)

pl.save('HaFF.dat',pl.array(temp).transpose())


