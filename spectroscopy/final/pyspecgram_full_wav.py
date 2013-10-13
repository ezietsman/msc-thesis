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
w1 = None
w2 = None
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
    w1 = min(x)
    w2 = max(x)
    imHa.append((data))
    print i




imHa = pl.array(imHa)

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

extent = (w1,w2,max(phase),min(phase))
# H alpha
pl.figure(figsize=(12,4))
ax1 = pl.subplot(111)
pl.subplots_adjust(bottom=0.14,left=0.07,right=0.93)
mini,maxi = sigclip(pl.array(imHa),3)
pl.imshow(pl.array(imHa),vmin=mini,vmax=maxi,aspect='auto',cmap=pl.cm.gray_r,extent=extent,interpolation='bilinear')

pl.xlabel('Wavelength (Angstrom)')
pl.ylabel('Orbital phase')
#pl.title(r'$H_{\alpha}$')
pl.xticks(pl.arange(4000,7100,500))
pl.figtext(0.105,0.90,r'$H_{\delta}$')
pl.figtext(0.17,0.90,r'$H_{\gamma}$')
pl.figtext(0.27,0.90,r'$He_{II}$')
pl.figtext(0.32,0.90,r'$H_{\beta}$')
pl.figtext(0.47,0.90,r'$He_{I}$')
pl.figtext(0.795,0.90,r'$H_{\alpha}$')


pl.savefig('specgram_full.png')

pl.show()





