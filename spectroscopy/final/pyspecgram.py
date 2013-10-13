# Read output files and make spectrogram


import pylab as pl
import pyfits as pf
import os
import scipy.stats as stats
import scipy.signal as sig
import astronomy as ast 
#import movingaverage as MA


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

# time between spectra
dtspec = float(pf.getheader(ff[1])['HJD']) - float(pf.getheader(ff[0])['HJD'])
P2 = dtspec*24.0
print 'P2 = ',P2

imHa = []
imHb = []
imHe = []
phase = []


print 'Calculating phase...\n'
for i in range(len(ff[:-2])):
    temp = ((float(pf.getheader(ff[i])['HJD']) - T0)/P)
    phase.append(temp)
print '...Done!\n'


# now get the phases, sort them and find the order of numbers.
phase = pl.array(phase)
phase2 = (pl.array(phase) - phase[0]) / P2
phase2,argsort = stats.fastsort(pl.array(phase2))

ave = pf.getdata('average.fits')
        
        
# speed of light in km/s
c = 2.99792458e5
v = 1500.0
for i in ff[:-2]:
    # subtract average from spectrum
    data = pf.getdata(i) #- ave
    head = pf.getheader(i)
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

    imHa.append((data[w1*w2]))

    dl = v/c*4860.0
    w1 = x > 4860 - dl
    w2 = x < 4860 + dl
    imHb.append(data[w1*w2])

    dl = v/c*4686
    w1 = x > 4686 - dl
    w2 = x < 4686 + dl
    imHe.append(data[w1*w2])
    print i


# run moving average
def sub_mov_ave(im,L):
    # function takes trailed spectra and subtracts moving average of length L
    def movingaverage(x,L):
        ma = pl.zeros(len(x),dtype='Float64')
        # must take the lead-up zone into account (prob slow)
        for i in range(0,L):
            ma[i] = pl.average(x[0:i+1])
    
        for i in range(L,len(x)):
            ma[i] = ma[i-1] + 1.0/L*(x[i]-x[i-L])
            
        return ma
    
    def medfilt(x,L):
        ma = sig.medfilt(x,L)
        return ma
    
    im_new = pl.array(im).copy()
    im_new[:] = 0.0
    im=pl.array(im)
    s = im.shape

    for i in range(s[1]):
        im_new[:,i] = medfilt(im[:,i],L)
    return im-im_new

L = 51

imHa = pl.array(imHa)
imHb = pl.array(imHb)
imHe = pl.array(imHe)

#imHa = sub_mov_ave(imHa,L)
#imHb = sub_mov_ave(imHb,L)
#imHe = sub_mov_ave(imHe,L)



def sigclip(im,nsig):
    # returns min and max values of image inside nsig sigmas
    temp = im.ravel()
    sd = pl.std(temp)
    m = pl.average(temp)
    gt = temp > m-nsig*sd
    lt = temp < m+nsig*sd
    temp = temp[gt*lt]
    mini = min(temp)
    maxi = max(temp)
    
    return mini,maxi

extent = (-1*v,v,max(phase),min(phase))
# H alpha
pl.figure(figsize=(7,4))
pl.subplots_adjust(wspace=0.001)
#pl.gray()
ax1 = pl.subplot(141)
mini,maxi = sigclip(pl.array(imHa),3)
pl.imshow(pl.array(imHa),vmin=mini,vmax=maxi,aspect='auto',cmap=pl.cm.gray_r,extent=extent,interpolation='bilinear')

# plot the deblended velocities
dat = pl.load('Ha_deblend.dat')
#pl.plot(dat[:,1], dat[:,0], 'yo-')
#pl.plot(dat[:,2], dat[:,0], 'yo-')

pl.xlabel('Velocity (km/s)')
pl.ylabel('Orbital phase')
pl.title(r'$H_{\alpha}$')
pl.xticks(pl.arange(-v,1.2*v,1000)[1:-1])


# H beta
ax2 = pl.subplot(142,sharey=ax1)

mini,maxi = sigclip(pl.array(imHb),3)
pl.imshow(pl.array(imHb),vmin=mini,vmax=maxi,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=extent)

# plot the deblended velocities
dat = pl.load('Hb_deblend.dat')
#pl.plot(dat[:,1], dat[:,0], 'yo-')
#pl.plot(dat[:,2], dat[:,0], 'yo-')

#pl.colorbar()
pl.xlabel('Velocity (km/s)')
pl.title(r'$H_{\beta}$')
pl.xticks(pl.arange(-v,1.2*v,1000)[1:-1])

#pl.figure(figsize=(8,8))
ax3 = pl.subplot(143,sharey=ax1)

mini,maxi = sigclip(pl.array(imHe),3)
pl.imshow(pl.array(imHe),vmin=mini,vmax=maxi,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=extent)
#pl.colorbar()
pl.xlabel('Velocity (km/s)')
#pl.ylabel('Orbital phase')
pl.title(r'$He_{II}$')
pl.xticks(pl.arange(-v,1.2*v,1000)[1:-1])

ax4 = pl.subplot(144,sharey=ax1)
pl.xlabel('Magnitude')
pl.title('Photometry')
T0 -= 2453964.0

photphase = (X[:,0] - T0) / P
pl.plot(X[:,2],photphase,'k.')
pl.ylim(extent[2],extent[3])
xt = pl.xticks()
pl.xticks(xt[0][2:-1:3])

yticklabels = ax2.get_yticklabels() + ax3.get_yticklabels() + ax4.get_yticklabels()
pl.setp(yticklabels, visible=False)

pl.savefig('specgram.png')

#Lines = {}
#Lines['Ha'] = imHa
#Lines['Hb'] = imHb
#Lines['He'] = imHe

## make lightcurves for Ha, Hb and He lines
#print 'Creating lightcurves'
#for line in Lines:
    #print line
    #pl.figure()
    #pl.subplot(211)
    #pl.title(line)
    #lc = Lines[line].sum(axis=1)
    #pl.plot(phase2,lc)
    #pl.xlabel('Orbital phase')
    #pl.ylabel('Intensity')
    
    #pl.subplot(212)
    #f,a = ast.signal.dft((phase*P + T0),lc,0,4000,1)
    #pl.plot(f,a)
    





pl.show()





