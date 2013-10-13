#!/usr/bin/python

# fold spectra on selected period. Calculates phase of observation and 
# plot a trailed spectrogram of spectrum vs phase
import pylab as pl
import pyfits as pf
import astronomy as ast
import scipy.interpolate as sci
import scipy.stats as stats
import os

# read spectrum
files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)



# start with DNO @ 3636.95 c/d. 
# calculate phase for every spectrum and assign number to it
period = 1.0/3567.2
t0 = float(pf.getheader(ff[0])['HJD'])
phase = []

print 'Calculating phase...\n'
for i in range(len(ff)):
    phasetemp = ((float(pf.getheader(ff[i])['HJD']) - t0)/period) % 1
    print phasetemp
    phase.append(phasetemp)
print '...Done!\n'

head = pf.getheader(ff[0])
start = head['CRVAL1']
step = head['CDELT1']
length = head['NAXIS1']
x = start + pl.arange(0,length)*step
hi = x > 6500
low = x < 6625
xx = hi*low


# now get the phases, sort them and find the order of numbers.
phase,argsort = stats.fastsort(pl.array(phase))



im = pl.array([pf.getdata(ff[i])[xx]-pl.median(pf.getdata(ff[i])[xx]) for i in argsort])

print im
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
im3 = []
klist = []
k = 0
temp = pl.zeros(len(pf.getdata(ff[0])[xx]),dtype=float)

for i in range(0,100):
    for j in range(len(ff)):
        if phase[j] >= i*0.01 and phase[j] < (i+1)*0.01:
             temp += pf.getdata(ff[i])[xx]-pl.median(pf.getdata(ff[i])[xx])#pf.getdata(ff[argsort[j]])
             k+=1
    ave = pl.average(temp)
    im3.append(temp)
    temp = pl.zeros(len(pf.getdata(ff[0])[xx]),dtype=float)
    klist.append(k)
    k = 0

#print sum(klist)
#print len(klist)




pl.figure()
pl.gray()
pl.imshow(im3, interpolation='nearest', aspect='auto',cmap=pl.cm.gray_r,extent=(6500,6625,1,0))
#ax = pl.axes()
#yt = ax.yaxis.get_ticklocs()
#ylabels = [str(round(i/10.0,1)) for i in range(-1,11,2)]
#ax.set_yticklabels(ylabels)
pl.ylabel('Phase')
pl.xlabel('Wavelength bins')
pl.colorbar()
pl.title('Folded spectrum on 3636.95 c/d DNO')


pl.show()
