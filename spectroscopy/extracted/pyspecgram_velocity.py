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
for i in ff:
    head = pf.getheader(i)
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    x = start + pl.arange(0,length)*step
    
    # hydrogen alpha 
    w1 = x > 6540
    w2 = x < 6586
    data = pf.getdata(i)
    imHa.append((data[w1*w2]-pl.average(data[w1*w2])))
    
    w1 = x > 4840
    w2 = x < 4880
    data = pf.getdata(i)
    imHb.append(data[w1*w2]-pl.average(data[w1*w2]))
    
    w1 = x > 4666
    w2 = x < 4709
    data = pf.getdata(i)
    imHe.append(data[w1*w2]-pl.average(data[w1*w2]))
    
    print i
    

# H alpha
pl.figure(figsize=(8,8))
X=pl.load('Ha.dat')
t = int(X[:,0][0])
E = t + 0.413168468257
# calculate t in terms of orbital phase
# period in days
period = 13351.0/86400.0
phase = (X[:,0]-E)/period - int(((X[:,0]-E)/period)[0])

#pl.subplots_adjust(wspace=0.001)
#pl.gray()
ax1 = pl.subplot(131)
pl.imshow(pl.array(imHa),aspect='auto',vmin=-0.1e-14,vmax=0.5e-14,cmap=pl.cm.gray_r,extent=(6540,6586,1.09,0.81),interpolation='bilinear')
pl.xlabel('Wavelength')
pl.ylabel('Orbital phase')
#pl.colorbar()
pl.title(r'$H_{\alpha}$')
pl.xticks(pl.arange(6540, 6586, 15))
pl.plot(X[:,1],phase,'r-')
#pl.savefig('specgramHa.png')
#pf.writeto('specgramHa.fits',pl.array(imHa),clobber=True)


## H beta
##pl.figure(figsize=(8,8))
#ax2 = pl.subplot(132,sharey=ax1)
#pl.imshow(pl.array(imHb),vmin=-0.3e-14,vmax=0.5e-14,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=(4840,4880,1.09,0.81))
##pl.colorbar()
#pl.xlabel('Wavelength')
##pl.ylabel('Orbital phase')
#pl.title(r'$H_{\beta}$')
#pl.xticks(pl.arange(4850, 4880, 10))
##pl.savefig('specgramHb.png')
##pf.writeto('specgramHbfits',pl.array(imHb),clobber=True)


##pl.figure(figsize=(8,8))
#ax3 = pl.subplot(133,sharey=ax1)
#pl.imshow(pl.array(imHe),vmin=-0.3e-14,vmax=1.0e-14,aspect='auto',cmap=pl.cm.gray_r,interpolation='bilinear',extent=(4666,4709,1.09,0.81))
##pl.colorbar()
#pl.xlabel('Wavelength')
##pl.ylabel('Orbital phase')
#pl.title(r'$HeII$')
#pl.xticks(pl.arange(4676, 4709, 12))
##pf.writeto('specgramHefits',pl.array(imHe),clobber=True)


#yticklabels = ax2.get_yticklabels()+ax3.get_yticklabels()
#pl.setp(yticklabels, visible=False)

#pl.savefig('specgram.png')
#pl.figure(figsize=(8,8))
#pl.imshow(pl.array(im34),vmin=0,vmax=100)
#pl.title('CCD34')

#pl.figure(figsize=(8,8))
#pl.imshow(pl.array(im34),vmin=0,vmax=100)
#pl.title('CCD56')

pl.show()





