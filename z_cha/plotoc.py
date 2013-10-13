# make O-C plots from the output files of oc

import pylab as pl
import os
import string




# archive ephemeris


def makeplot(X,hjd,filename):

    # archive ephem
    T0 = 0 # 2452525.374416
    # august ephem
    #T0 = 2453964.330709
    P =1.0 #  0.154525
    
    
    X = pl.load(filename)
    a = X[:,0][:-1]
    p = X[:,1][:-1]
    x = X[:,2][:-1]+hjd 
    #x = X[:,2][:-1]    
    siga = X[:,3][:-1]
    sigp = X[:,4][:-1]
    
    X2 = pl.load('S6061r.dat')
    y = X2[:,3]
    x2 = X2[:,0]
    pl.figure(figsize=(6,4))
    pl.subplots_adjust(left=0.14,hspace=0.001)

    # plot the original lightcurve
    ax1 = pl.subplot(311)
    pl.plot(x2-int(x2[0]),y,'.')
    pl.xlabel('HJD +%s' %int(x2[0]))
    pl.ylabel('Magnitude')
    #yt = pl.yticks()
    #ax1.set_yticks(yt[0][1],yt[0][0])
    yl = pl.ylim()
    pl.ylim(yl[1],yl[0])
    pl.xlim(min(x-int(x[0]))-0.02, max(x-int(x[0]))+0.02)
    pl.grid()


    # plot the amplitude
    ax1 = pl.subplot(312)
    pl.errorbar(x-int(x[0]),a,siga,fmt='ro')
    pl.xlabel('HJD +%s' %int(x[0]))
    pl.ylabel('Amplitude')
    yt = pl.yticks()
    ax1.set_yticks(yt[0][1:-1])
    pl.xlim(min(x-int(x[0]))-0.02, max(x-int(x[0]))+0.02)
    pl.grid()
   
    # plot the phase
    ax2 = pl.subplot(313)
    pl.errorbar(x-int(x[0]),p,sigp,fmt='go')
    #pl.xlabel('Orbital Phase')
    pl.xlabel('HJD +%s' %int(x[0]))
    pl.ylabel('Phase (O-C)')
    yt = pl.yticks()
    ax2.set_yticks(yt[0][1:-1])
    pl.xlim(min(x-int(x[0]))-0.02, max(x-int(x[0]))+0.02)
    pl.grid()
    
    # remove the amplitude graph's x-axis
    pl.setp(ax1.get_xticklabels() , visible=False)
    
    pl.savefig(filename[:-3]+'png')


    pl.show()
    
    

if __name__ == '__main__':
    os.system('ls -l')
    filename = raw_input('Open which file ? : ')
    hjd = int(raw_input('Add how much to fix Julian Date? : '))
    X = pl.load(filename)
    makeplot(X,hjd,filename)
    