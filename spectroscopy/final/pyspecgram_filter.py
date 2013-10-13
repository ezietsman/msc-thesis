# Read output files and make spectrogram


import pylab as pl
import pyfits as pf
import os
import scipy.stats as stats
import matplotlib.axes3d as axes3d
import scipy.signal as signal
#eP20060817%04d%s.0001.fits' % (i,ccd)


X = pl.load('ec2117ans_2_cc.dat')

files = os.listdir(os.curdir)
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
ave = pf.getdata('aveEC2117.fits')


# start with lpDNO @ 829 c/d. check if this is the actual frequency
# calculate phase for every spectrum and assign number to it
#period = 1.0/3627.965
#t0 = float(pf.getheader(ff[0])['HJD'])

print 'Calculating phase...\n'
for i in range(len(ff[:-2])):
    temp = ((float(pf.getheader(ff[i])['HJD']) - T0)/P)
    phase.append(temp)
print '...Done!\n'


# now get the phases, sort them and find the order of numbers.
phase = pl.array(phase)
phase2 = (pl.array(phase) - phase[0]) / P2
phase2,argsort = stats.fastsort(pl.array(phase2))


# speed of light in km/s
c = 2.99792458e5
v = 1500.0
for i in ff:
    
    
    # subtract average from spectrum
    data = pf.getdata(i)# - ave
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
    
    imHa.append(data[w1*w2]-pl.average(data[w1*w2]))
    #imHa.append((data[w1*w2]))
    #imHa.append((data[w1*w2]-pl.average(data[w1*w2])-(ave[w1*w2]-pl.average(ave[w1*w2]))))
    
    dl = v/c*4860.0
    w1 = x > 4860 - dl
    w2 = x < 4860 + dl
    #data = pf.getdata(i)
    imHb.append(data[w1*w2]-pl.average(data[w1*w2]))
    #imHb.append((data[w1*w2]-pl.average(data[w1*w2])-(ave[w1*w2]-pl.average(ave[w1*w2]))))
    #imHb.append(data[w1*w2])
    
    dl = v/c*4686
    w1 = x > 4686 - dl
    w2 = x < 4686 + dl
    #data = pf.getdata(i)
    imHe.append(data[w1*w2]-pl.average(data[w1*w2]))
    #imHe.append((data[w1*w2]-pl.average(data[w1*w2])-(ave[w1*w2]-pl.average(ave[w1*w2]))))
    #imHe.append(data[w1*w2])
    
    print i




# now create filter coefficients
# filter parameters
fp = 144.0
fs = 100.0
wp = fp*pl.pi*dtspec*2.0/pl.pi
ws = fs*pl.pi*dtspec*2.0/pl.pi
gpass = 0.1
gstop = 15
ftype = 'cheby1'

#print wp
#print ws

# calculate filter coefficients and filter the lightcurve
b,a = signal.iirdesign(wp,ws,gpass,gstop,ftype=ftype)


#filter each of the images
print 'Filtering Ha'
imHa = pl.array(imHa)
h,w = imHa.shape
for i in range(w):
    ynew = imHa[:,i]
    yf = signal.lfilter(b,a,ynew)
    #pl.figure()
    #pl.subplot(211)
    #pl.plot(ynew)
    #pl.subplot(212)
    #pl.plot(yf)
    #pl.show()
    yf -= yf[0]
    imHa[:,i] = yf
    
print 'Filtering Hb'
imHb = pl.array(imHb)
h,w = imHb.shape
for i in range(w):
    ynew = imHb[:,i]
    yf = signal.lfilter(b,a,ynew)
    #yf -= yf[0]
    imHb[:,i] = yf

print 'Filtering HeII'
imHe = pl.array(imHe)
h,w = imHe.shape
for i in range(w):
    ynew = imHe[:,i]
    yf = signal.lfilter(b,a,ynew)
    #yf -= yf[0]
    imHe[:,i] = yf




extent = (-1*v,v,max(phase),min(phase))
# H alpha
pl.figure(figsize=(7,7))
pl.subplots_adjust(wspace=0.001)
#pl.gray()
ax1 = pl.subplot(141)


#pl.imshow(pl.array(imHa),aspect='auto',vmin=-0.1e-14,vmax=0.5e-14,cmap=pl.cm.gray_r,extent=(6540,6586,1.09,0.81),interpolation='bilinear')



pl.imshow(pl.array(imHa),aspect='auto',cmap=pl.cm.gray_r,extent=extent,interpolation='bilinear')


# plot the deblended velocities

#dat = pl.load('Ha_deblend.dat')

#pl.plot(dat[:,1], dat[:,0], 'yo-')
#pl.plot(dat[:,2], dat[:,0], 'yo-')

#print dat[:,0]


#im = pl.contourf(pl.flipud(pl.array(imHa)),100,extent=(6540,6586,1.09,0.81),cmap=pl.cm.jet)
pl.xlabel('Velocity (km/s)')
pl.ylabel('Orbital phase')
#pl.colorbar()
pl.title(r'$H_{\alpha}$')
pl.xticks(pl.arange(-v,1.2*v,1000)[1:-1])
#pl.savefig('specgramHa.png')
#pf.writeto('specgramHa.fits',pl.array(imHa),clobber=True)


# H beta
#pl.figure(figsize=(8,8))
ax2 = pl.subplot(142,sharey=ax1)
#pl.imshow(pl.array(imHb),vmin=-0.3e-14,vmax=0.5e-14,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=(4840,4880,1.09,0.81))
pl.imshow(pl.array(imHb),vmin=-0.5e-8,vmax=0.5e-8,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=extent)

# plot the deblended velocities

#dat = pl.load('Hb_deblend.dat')

#pl.plot(dat[:,1], dat[:,0], 'yo-')
#pl.plot(dat[:,2], dat[:,0], 'yo-')

#pl.colorbar()
pl.xlabel('Velocity (km/s)')
#pl.ylabel('Orbital phase')
pl.title(r'$H_{\beta}$')
pl.xticks(pl.arange(-v,1.2*v,1000)[1:-1])
#pl.xticks(pl.arange(4850, 4880, 10))
#pl.savefig('specgramHb.png')
#pf.writeto('specgramHbfits',pl.array(imHb),clobber=True)


#pl.figure(figsize=(8,8))
ax3 = pl.subplot(143,sharey=ax1)
#pl.imshow(pl.array(imHe),vmin=-0.3e-14,vmax=1.0e-14,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=(4666,4709,1.09,0.81))
pl.imshow(pl.array(imHe),vmin=-0.5e-8,vmax=1.0e-8,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=extent)
#pl.colorbar()
pl.xlabel('Velocity (km/s)')
#pl.ylabel('Orbital phase')
pl.title(r'$HeII$')
pl.xticks(pl.arange(-v,1.2*v,1000)[1:-1])
#pl.xticks(pl.arange(4676, 4709, 12))
#pf.writeto('specgramHefits',pl.array(imHe),clobber=True)

ax4 = pl.subplot(144,sharey=ax1)
pl.xlabel('Magnitude')
pl.title('Photometry')
T0 -= 2453964.0

photphase = (X[:,0] - T0) / P
pl.plot(X[:,2],photphase,'k.')
pl.ylim(extent[2],extent[3])
xt = pl.xticks()
pl.xticks(xt[0][2:-1:3])


#pl.xticks(pl.arange(4676, 4709, 12))
#pf.writeto('specgramHefits',pl.array(imHe),clobber=True)








yticklabels = ax2.get_yticklabels() + ax3.get_yticklabels() + ax4.get_yticklabels()
pl.setp(yticklabels, visible=False)

pl.savefig('specgram.png')
#pl.figure(figsize=(8,8))
#pl.imshow(pl.array(im34),vmin=0,vmax=100)
#pl.title('CCD34')

#pl.figure(figsize=(8,8))
#pl.imshow(pl.array(im34),vmin=0,vmax=100)
#pl.title('CCD56')





## plot the spectrograms folded on a certain period




#pl.figure(figsize=(8,8))

#extent = [-1500,1500,1,0]

#pl.subplots_adjust(wspace=0.001)
##pl.gray()
#ax1 = pl.subplot(131)

#im = pl.array([imHa[i] for i in argsort])

#pl.imshow(im,aspect='auto',cmap=pl.cm.gray_r,extent=extent,interpolation='bilinear')

#pl.xlabel('Velocity (km/s)')
#pl.ylabel('Orbital phase')
#pl.title(r'$H_{\alpha}$')
#pl.xticks([-1000,0,1000])

## H beta
#ax2 = pl.subplot(132,sharey=ax1)
#im = pl.array([imHb[i] for i in argsort])
#pl.imshow(im,vmin=-0.5e-8,vmax=0.5e-8,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=extent)

#pl.xlabel('Velocity (km/s)')

#pl.title(r'$H_{\beta}$')
#pl.xticks([-1000,0,1000])


#ax3 = pl.subplot(133,sharey=ax1)
#im = pl.array([imHe[i] for i in argsort])
#pl.imshow(im,vmin=-0.5e-8,vmax=0.5e-8,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=extent)
#pl.xlabel('Velocity (km/s)')
#pl.title(r'$HeII$')
#pl.xticks([-1000,0,1000])


#yticklabels = ax2.get_yticklabels()+ax3.get_yticklabels()
#pl.setp(yticklabels, visible=False)


##pl.figure()
##imHe = pl.array(imHe)
##imHa = pl.array(imHa)
##print imHa.shape
##print len(x[w1*w2])
##print len(phase)
##fig = pl.gcf()
##ax3d = axes3d.Axes3D(fig)
##plt = fig.axes.append(ax3d)

##xx,yy = pl.meshgrid(pl.arange(93),pl.arange(len(phase)))

##levels = pl.arange(-0.5e-8,1.0e-8,0.1e-8)

##ax3d.contour3D(xx,yy,imHa,levels=levels)


#pf.writeto('heII.fits',data=pl.array(imHe),clobber=True)

pl.show()





