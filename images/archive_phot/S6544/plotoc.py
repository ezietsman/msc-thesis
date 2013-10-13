# make O-C plots from the output files of oc

import pylab as pl
import os
import string




# archive ephemeris


def makeplot(X,hjd):

    T0 = 2452525.374416
    P = 0.154525
    
    #X = pl.load(filename)
    a = X[:,0][:-1]
    p = X[:,1][:-1]
    x = (X[:,2][:-1]+hjd-T0)/P
    siga = X[:,3][:-1]
    sigp = X[:,4][:-1]
    
    pl.figure(figsize=(6,4))
    pl.subplots_adjust(left=0.14,hspace=0.001)

    # plot the amplitude
    ax1 = pl.subplot(211)
    pl.errorbar(x,a,siga,fmt='ro')
    pl.xlabel('Orbital Phase')
    pl.ylabel('Amplitude')
    yt = pl.yticks()
    ax1.set_yticks(yt[0][1:-1])
    pl.grid()
   
    # plot the phase
    ax2 = pl.subplot(212)
    pl.errorbar(x,p,sigp,fmt='go')
    pl.xlabel('Orbital Phase')
    pl.ylabel('Phase (O-C)')
    yt = pl.yticks()
    ax2.set_yticks(yt[0][1:-1])
    pl.grid()
    
    # remove the amplitude graph's x-axis
    pl.setp(ax1.get_xticklabels() , visible=False)


    pl.show()
    
    

if __name__ == '__main__':
    os.system('ls -l')
    filename = raw_input('Open which file ? : ')
    hjd = int(raw_input('Add how much to fix Julian Date? : '))
    X = pl.load(filename)
    makeplot(X,hjd)
    