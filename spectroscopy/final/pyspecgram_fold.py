# Read output files and make spectrogram


import pylab as pl
import pyfits as pf
import os
#import scipy.stats as stats
import numpy as N
import scipy.signal as sig

#eP20060817%04d%s.0001.fits' % (i,ccd)


X = pl.load('ec2117ans_2_cc.dat')

files = os.listdir(os.curdir)
files.sort()
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)



# calculate phase based on eclipse ephemeris
T0 = 2453964.3307097
P = 0.1545255

# period to fold on
P2 = 25.0 / 86400.0
print 'P2 = ',P2


imHa = []
imHb = []
imHe = []
phase = []
date = []
ave = pf.getdata('Average.fits')


print 'Calculating orbital phase...\n'
for i in range(len(ff[:-3])):
    temp = (float(pf.getheader(ff[i])['HJD']))
    # block spectra after phase 7.9 - just use bright bits.
    phasetemp = (temp-T0)/P
    if phasetemp < 7.9:
        date.append(temp)
        phase.append((temp-T0)/P)
print '...Done!\n'


# now get the phases, sort them and find the order of numbers.
phase = pl.array(phase)
date = pl.array(date)


phase2 = ((date - date[0]) / P2) % 1
argsort = phase2.argsort()
phase2.sort()


# speed of light in km/s
c = 2.99792458e5
v = 750.0
#for i in range(len(phase)):
for i in argsort:
    print ff[i]
    #print ff[i]
    # subtract average from spectrum
    data = pf.getdata(ff[i])# - ave
    head = pf.getheader(ff[i])
    
    # write average subtracted spectrum to new fits file
    #pf.writeto('avesub%s'%i,data=data,header=head)
    
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    x = start + pl.arange(0,length)*step
    
    # hydrogen alpha
    dl = v/c*6563.0
    w1 = x > 6563 - dl
    w2 = x < 6563 + dl
    #calc continuum level to subtract it
    c1 = x > 6400
    c2 = x < 6600
    continuum = pl.median(data[c1*c2])
    imHa.append((data[w1*w2]-continuum))
    
    # hydrogen beta
    dl = v/c*4860.0
    w1 = x > 4860 - dl
    w2 = x < 4860 + dl
    c1 = x > 4700
    c2 = x < 4800
    continuum = pl.median(data[c1*c2])
    imHb.append(data[w1*w2]-continuum)
    
    # helium II
    dl = v/c*4686
    w1 = x > 4686 - dl
    w2 = x < 4686 + dl
    c1 = x > 4550
    c2 = x < 4750
    continuum = pl.median(data[c1*c2])
    imHe.append(data[w1*w2]-continuum)
    
    #print i
    
##############################################################################
def sub_mov_ave(im,L):
    # function takes trailed spectra and subtracts moving average of length L
    def movingaverage(x,L):
        ma = pl.zeros(len(x),dtype='Float64')
        # must take the lead-up zone into account (prob slow)
        for i in range(0,L):
            ma[i] = pl.average(x[0:i+1])

        for i in range(L,len(x)):
            #print i
            ma[i] = ma[i-1] + 1.0/L*(x[i]-x[i-L])

        return ma

    def medfilt(x,L):
        ma = sig.medfilt(x,L)
        return ma

    im_new = pl.array(im).copy()
    im_new[:] = 0.0
    im=pl.array(im)
    s = im.shape
    print s

    for i in range(s[1]):
        im_new[:,i] = movingaverage(im[:,i],L)

    return im-im_new
###########################################################################


def makebins(im,numbins):
    # returns the image binned into phase bins
    # phase2 contains sorted DNO phases
    
    # number in each bin
    im = pl.array(im)
    num = pl.zeros(numbins,dtype='Float64')
    
    #print im.shape[1]
    imnew = pl.zeros((numbins,im.shape[1]),dtype='Float64')

    bins = pl.arange(0.0,1.0,1.0/numbins)
    #print bins

    # sum spectra that falls into the same phase bin.
    for i in range(len(phase2)):
        #print phase2[i]
        gt = phase2[i] >= bins
        lt = phase2[i] < bins + 1.0/numbins
        #print lt*gt
        imnew[lt*gt] += im[i]
        num[lt*gt] += 1

    # divide by number in each bin to take average
    for i in range(len(num)):
        print num[i], imnew[i,:].sum()
        imnew[i,:] /= num[i]

    return imnew,num



# subtract running mean
#L = 2
#print 'Ha'
#imHa = sub_mov_ave(imHa,L)
#print 'Hb'
#imHb = sub_mov_ave(imHb,L)
#print 'He'
#imHe = sub_mov_ave(imHe,L)



extent = (-1*v,v,2*max(phase2),min(phase2))
# H alpha
pl.figure(figsize=(12,6))
pl.subplots_adjust(wspace=0.001)
#pl.gray()
ax1 = pl.subplot(131)


numbins = 5
numvelbins = 50


# add the spectra into phase bins
#im = pl.array([imHa[i] for i in argsort])

#im = N.array_split(im,numbins)
#im = [N.average(block,axis=0) for block in im]

im,bins = makebins(imHa,numbins)
im = N.concatenate([im,im])



#pl.imshow(im,aspect='auto',vmin=-0.0001,vmax=0.0001,cmap=pl.cm.gray_r,extent=extent,interpolation='nearest')
#pl.imshow(im,aspect='auto',vmin=-0.0002,vmax=0.0007,cmap=pl.cm.gray_r,extent=extent,interpolation='nearest')
pl.imshow(im,aspect='auto',cmap=pl.cm.gray_r,extent=extent,interpolation='nearest')
pl.xlabel('Velocity (km/s)')
pl.ylabel('Orbital phase')
#pl.colorbar()
pl.title(r'$H_{\alpha}$')
pl.xticks(pl.arange(-v,1.2*v,250)[1:-1])
#pl.savefig('specgramHa.png')


# H beta
ax2 = pl.subplot(132,sharey=ax1)

im,bins = makebins(imHb,numbins)
im = N.concatenate([im,im])




#pl.imshow(im,vmin=-0.0001,vmax=0.0001,aspect='auto',cmap=pl.cm.gray_r,interpolation='nearest',extent=extent)
#pl.imshow(im,aspect='auto',vmin=-0.0002,vmax=0.0003,cmap=pl.cm.gray_r,interpolation='nearest',extent=extent)
pl.imshow(im,aspect='auto',cmap=pl.cm.gray_r,interpolation='nearest',extent=extent)
#pl.colorbar()
pl.xlabel('Velocity (km/s)')
#pl.ylabel('Orbital phase')
pl.title(r'$H_{\beta}$')
pl.xticks(pl.arange(-v,1.2*v,250)[1:-1])
#pl.xticks(pl.arange(4850, 4880, 10))
#pl.savefig('specgramHb.png')
#pf.writeto('specgramHbfits',pl.array(imHb),clobber=True)


#pl.figure(figsize=(8,8))
ax3 = pl.subplot(133,sharey=ax1)
#pl.imshow(pl.array(imHe),vmin=-0.3e-14,vmax=1.0e-14,aspect='auto',cmap=pl.cm.gray_r,interpolation='nearest',extent=(4666,4709,1.09,0.81))


im,bins = makebins(imHe,numbins)
im = N.concatenate([im,im])


#pl.imshow(im,vmin=-0.0002,vmax=0.0005,aspect='auto',cmap=pl.cm.gray_r,interpolation='nearest',extent=extent)
pl.imshow(im,aspect='auto',cmap=pl.cm.gray_r,interpolation='nearest',extent=extent)
#pl.imshow(im,aspect='auto',vmincmap=pl.cm.gray_r,interpolation='nearest',extent=extent)
#pl.colorbar()
pl.xlabel('Velocity (km/s)')
#pl.ylabel('Orbital phase')
pl.title(r'$HeII$')
pl.xticks(pl.arange(-v,1.2*v,250)[1:-1])
#pl.xticks(pl.arange(4676, 4709, 12))
#pf.writeto('specgramHefits',pl.array(imHe),clobber=True)

#ax4 = pl.subplot(144,sharey=ax1)
#pl.xlabel('Magnitude')
#pl.title('Photometry')
#T0 -= 2453964.0

#photphase = (X[:,0] - T0) / P
#y = 10**(X[:,2]/(-2.5))
#y /= pl.average(y)
#pl.plot(y,photphase,'k.')
##pl.ylim(extent[3],extent[1])
#xt = pl.xticks()
#pl.xticks(xt[0][2:-1:3])


yticklabels = ax2.get_yticklabels() + ax3.get_yticklabels()# + ax4.get_yticklabels()
pl.setp(yticklabels, visible=False)

pl.savefig('specgram_fold_ave_sub%s.png' %(round(P2*86400,2)))




pl.show()





