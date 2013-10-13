#!/usr/bin/python

# Plot lightcurves and fourier transforms from spectra and photmetry
import pylab as pl
import pyfits as pf
import os
import astronomy as ast
import scipy.io as io
import scipy.stats as sci


files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)

big = []
t = []
t2 = []

for i in range(len(ff)):
    print 'Plotting , ',i+61
##    w = allspec[i].wave > 5000
##    w2 = allspec[i].wave < 6000
    big.append(pf.getdata(ff[i]).sum())
    t.append(float(pf.getheader(ff[i])['HJD']))
    
    ##print time between exposures
    #if i >= 1 and i <len(allspec):
        #t2.append((allspec[i].HJD -allspec[i-1].HJD)*86400.0) 


t = pl.array(t)
big = pl.array(-2.5*pl.log10(big))


#read the flattened spectroscopy lightcurve
temp = pl.load('output.dat')
t = temp[:,0]
big = temp[:,1]


# select times to use. make photometry and spectroscopy use the same HJD's for calcs
t_start = t[0] - int(t[0])

# read flattened lightcurve
temp = pl.load('run2_flat.dat')
x = temp[:,0] 
y = temp[:,1]
z = temp[:,2]

x = x - int(x[0])
times_0 = x >= t_start
times_1 = x <= max(t - int(t[0]))

x = x[times_0*times_1]
y = y[times_0*times_1]


# Some cool plots

pl.figure(figsize=(10,10))

pl.subplot(221)
pl.plot(pl.array(t-int(t[0])),pl.array(big))
ylo,yhi = pl.ylim()
pl.ylim(yhi,ylo)
#pl.xlim(0.3,0.6)
pl.title('Spectrum lightcurve')
pl.xlabel('HJD')
pl.ylabel('Total spectrum Mag')

pl.subplot(222)
f,a = ast.signal.dft(t,big,3000,3934,0.1)
pl.title('Spectrum periodogram')
pl.xlabel('Frequency [Cycles/Day]')
pl.ylabel('Amplitude [mag]')
pl.plot(f,a,'g-')
sorted,argsort = sci.fastsort(a)
print 'Max amplitude of %s at %s cycles/day' % (sorted[-1],f[argsort[-1]])
pl.subplot(223)
pl.plot(x,y,'.')
pl.title('Photometry lightcurve')
ylo,yhi = pl.ylim()
pl.ylim(yhi,ylo)
pl.xlabel('HJD')
pl.ylabel('Relative Magnitude')

pl.subplot(224)
f,a = ast.signal.dft(x,y,0,3934,0.1)
pl.title('Photometry periodogram')
pl.xlabel('Frequency [Cycles/Day]')
pl.ylabel('Amplitude [mag]')
pl.plot(f,a,'g-')


pl.show()


sorted,argsort = sci.fastsort(a)
print 'Max amplitude of %s at %s cycles/day' % (sorted[-1],f[argsort[-1]])

# write spectroscopy lightcurve to file
#speclc = [ [t[i], big[i]] for i in range(len(t))]

#speclc = pl.array(speclc)
#myfile = file('spec_lightcurve.dat','w')
#io.write_array(myfile,speclc,precision=10)
#myfile.close()


# encode the movie
#os.system("mencoder 'mf://*.png' -mf type=png:fps=25 -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o animation.mpg")



