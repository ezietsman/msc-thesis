#!/usr/bin/python

# fold spectra on selected period. Calculates phase of observation and 
# plot a trailed spectrogram of spectrum vs phase
# subtract running mean from each wavelength bin use average of 3 spectra
import pylab as pl
import pyfits as pf
import scipy.interpolate as sci
import scipy.stats as stats
import os

files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)



# start with lpDNO @ 829 c/d. check if this is the actual frequency
# calculate phase for every spectrum and assign number to it
period = 86400.0/23.74 #1.0/3636.9
t0 = float(pf.getheader(ff[0])['HJD'])
phase = []

print 'Calculating phase...\n'
for i in range(len(ff)):
    temp = ((float(pf.getheader(ff[i])['HJD']) - t0)/period) % 1
    phase.append(temp)
print '...Done!\n'


# now get the phases, sort them and find the order of numbers.
phase,argsort = stats.fastsort(pl.array(phase))

im = pl.array([pf.getdata(ff[i]) for i in argsort])
#im = pl.array([allspec[i].count for i in range(len(allspec))])

# phases are not equispaced, need to interpolate im on to regular phase grid.

#l,w = pl.shape(im)

#x = pl.linspace(0.0,1.0,l)
#im2 = 1.0*pl.zeros((l,w))

#print '\nInterpolating to regular grid...\n'
#for i in range(w):
    #temp = im[:,i]
    #tck = sci.splrep(pl.array(phase),temp,k=1,s=0.0)
    #im2[:,i] = sci.splev(x,tck)
#print '\nDone...\n'



# bin spectra together in 0.1 phase bins
#im3 = []
#klist = []
#k = 0
#temp = pl.zeros(3072,dtype=float)
#for i in range(0,10):
    #for j in range(len(allspec)):
        #if phase[j] >= i*0.1 and phase[j] < (i+1)*0.1:
             #temp += allspec[argsort[j]].count
             #k+=1
    #ave = pl.average(temp)
    #im3.append(temp/ave)
    #temp = pl.zeros(3072,dtype=float)
    #klist.append(k)
    #k = 0

#print sum(klist)
#print len(klist)




pl.figure()
#pl.gray()
pl.imshow(im, interpolation='nearest', aspect='auto',cmap=pl.cm.jet)
#ax = pl.axes()
#yt = ax.yaxis.get_ticklocs()
#ylabels = [str(round(i/10.0,1)) for i in range(-1,11,2)]
#ax.set_yticklabels(ylabels)
pl.ylabel('Phase')
pl.xlabel('Wavelength bins')
pl.colorbar()
pl.title('Folded spectrum on 3636.9 c/d DNO')


pl.show()
