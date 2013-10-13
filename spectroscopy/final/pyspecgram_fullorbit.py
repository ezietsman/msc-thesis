# Read output files and make spectrogram


import pylab as pl
import pyfits as pf
import os


#eP20060817%04d%s.0001.fits' % (i,ccd)


files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)


imHa = []
imHb = []
imHe = []



# speed of light in km/s
c = 2.99792458e5
v = 1500.0
for i in ff[:-2]:
    head = pf.getheader(i)
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    x = start + pl.arange(0,length)*step
    
    # hydrogen alpha
    dl = v/c*6563.0
    w1 = x > 6563 - dl
    w2 = x < 6563 + dl
    data = pf.getdata(i)
    imHa.append((data[w1*w2]-pl.average(data[w1*w2])))
    #imHa.append((data[w1*w2]))
    
    dl = v/c*4860.0
    w1 = x > 4860 - dl
    w2 = x < 4860 + dl
    data = pf.getdata(i)
    imHb.append(data[w1*w2]-pl.average(data[w1*w2]))
    #imHb.append(data[w1*w2])
    
    dl = v/c*4686
    w1 = x > 4686 - dl
    w2 = x < 4686 + dl
    data = pf.getdata(i)
    imHe.append(data[w1*w2]-pl.average(data[w1*w2]))
    #imHe.append(data[w1*w2])
    
    print i
    

extent = (-1500,1500,1.09,0.81)
# H alpha
pl.figure(figsize=(8,8))
pl.subplots_adjust(wspace=0.001)
#pl.gray()
ax1 = pl.subplot(131)


#pl.imshow(pl.array(imHa),aspect='auto',vmin=-0.1e-14,vmax=0.5e-14,cmap=pl.cm.gray_r,extent=(6540,6586,1.09,0.81),interpolation='bilinear')

pl.imshow(pl.array(imHa),aspect='auto',cmap=pl.cm.gray_r,extent=extent,interpolation='bilinear')

ax1.set_xlim(-1500,1500)
ax1.set_ylim(1.1,0)


#im = pl.contourf(pl.flipud(pl.array(imHa)),100,extent=(6540,6586,1.09,0.81),cmap=pl.cm.jet)
pl.xlabel('Velocity (km/s)')
pl.ylabel('Orbital phase')
#pl.colorbar()
pl.title(r'$H_{\alpha}$')
pl.xticks([-1000,0,1000])
#pl.savefig('specgramHa.png')
#pf.writeto('specgramHa.fits',pl.array(imHa),clobber=True)


# H beta
#pl.figure(figsize=(8,8))
ax2 = pl.subplot(132,sharey=ax1)
#pl.imshow(pl.array(imHb),vmin=-0.3e-14,vmax=0.5e-14,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=(4840,4880,1.09,0.81))
pl.imshow(pl.array(imHb),vmin=-0.5e-8,vmax=0.5e-8,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=extent)
ax2.set_xlim(-1500,1500)
ax2.set_ylim(1.1,0)
#pl.colorbar()
pl.xlabel('Velocity (km/s)')
#pl.ylabel('Orbital phase')
pl.title(r'$H_{\beta}$')
pl.xticks([-1000,0,1000])
#pl.xticks(pl.arange(4850, 4880, 10))
#pl.savefig('specgramHb.png')
#pf.writeto('specgramHbfits',pl.array(imHb),clobber=True)


#pl.figure(figsize=(8,8))
ax3 = pl.subplot(133,sharey=ax1)
#pl.imshow(pl.array(imHe),vmin=-0.3e-14,vmax=1.0e-14,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=(4666,4709,1.09,0.81))
pl.imshow(pl.array(imHe),vmin=-0.5e-8,vmax=1.2e-8,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=extent)
ax3.set_xlim(-1500,1500)
ax3.set_ylim(1.1,0)
#pl.colorbar()
pl.xlabel('Velocity (km/s)')
#pl.ylabel('Orbital phase')
pl.title(r'$HeII$')
pl.xticks([-1000,0,1000])
#pl.xticks(pl.arange(4676, 4709, 12))
#pf.writeto('specgramHefits',pl.array(imHe),clobber=True)


yticklabels = ax2.get_yticklabels()+ax3.get_yticklabels()
pl.setp(yticklabels, visible=False)

pl.savefig('specgram_fullorbit.png')
#pl.figure(figsize=(8,8))
#pl.imshow(pl.array(im34),vmin=0,vmax=100)
#pl.title('CCD34')

#pl.figure(figsize=(8,8))
#pl.imshow(pl.array(im34),vmin=0,vmax=100)
#pl.title('CCD56')

pl.show()





