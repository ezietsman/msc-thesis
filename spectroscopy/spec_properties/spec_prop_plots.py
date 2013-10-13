# make in and out of eclipse average spectrum plots

import pylab as pl
import pyfits as pf
import os
#import scipy.stats as stats
#import scipy.signal as sig
#import astronomy as ast 
#import movingaverage as MA



files = os.listdir('../final/')
files.sort()
ff = []
for f in files:
    #print f
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append('../final/'+f)


# calculate phase based on eclipse ephemeris
T0 = 2453964.3307097
P = 0.1545255
#phase = []
#print 'Calculating phase...\n'
#for i in range(len(ff[:-2])):
    #temp = ((float(pf.getheader(ff[i])['HJD']) - T0)/P)
    #phase.append(temp)
#print '...Done!\n'

        
        
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


def avespec(speclist,p1,p2):
    # returns wavelength range and average of spectra in list between phase p1 and p2
    ave = []
    x = None
    for s in speclist:
        #print s
        data = pf.getdata(s)
        head = pf.getheader(s)
        phase = (float(head['HJD'])-T0)/P
        print phase
        start = head['CRVAL1']
        step = head['CDELT1']
        length = head['NAXIS1']
        x = start + pl.arange(0,length)*step
        if phase >= p1 and phase <= p2:
            ave.append(data)
    
    ave = pl.average(ave,axis=0)
    return x,ave


x,out_eclipse = avespec(ff,7.8,7.9)
x,mid_eclipse = avespec(ff,7.95,8.05)



head = pf.getheader('../final/EC0000.fits')
pf.writeto('mid_eclipse.fits',data=mid_eclipse,header=head,clobber=True)
pf.writeto('outof_eclipse.fits',data=out_eclipse,header=head,clobber=True)








#pl.show()





