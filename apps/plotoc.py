# make O-C plots from the output files of oc

import pylab as pl
import os
import string




# archive ephemeris


def makeplot(X,hjd,filename,xlo,xhi):

    # archive ephem
    #T0 = 2452525.374416
    # august ephem
    T0 = 2453964.330709
    P = 0.154525

    #   set some lower and upper time axis limits. set xlo to None for auto limits
    xlo = xlo
    xhi = xhi

    X = pl.load(filename)
    a = X[:,0][:-1]
    p = X[:,1][:-1]
    x = (X[:,2][:-1]+hjd-T0)/P - int(((X[:,2][:-1]+hjd-T0)/P)[0])
    #x = X[:,2][:-1]    
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
    if xlo != None:
        pl.xlim(xlo,xhi)
    else:
        pl.xlim(min(x)-0.02, max(x)+0.02)
    pl.grid()
   
    # plot the phase
    ax2 = pl.subplot(212)
    pl.errorbar(x,p,sigp,fmt='go')
    pl.xlabel('Orbital Phase')
    pl.ylabel('Phase (O-C)')
    yt = pl.yticks()
    ax2.set_yticks(yt[0][1:-1])
    if xlo != None:
        pl.xlim(xlo,xhi)
    else:
        pl.xlim(min(x)-0.02, max(x)+0.02)
    pl.grid()
    #pl.ylim(-1.0,0.5)
    # remove the amplitude graph's x-axis
    pl.setp(ax1.get_xticklabels() , visible=False)
    
    #pl.savefig(filename[:-3]+'png')


    pl.show()
    
    

if __name__ == '__main__':
    os.system('ls -l')
    filename = raw_input('Open which file ? : ')
    hjd = int(raw_input('Add how much to fix Julian Date? : '))
    temp = string.split(raw_input('Lower and upper limit of x-axis (orbital period) :  '))
    try:
        xlo = float(temp[0])
        xhi = float(temp[1])
    except:
        xlo = None
        xhi = None
    X = pl.load(filename)
    makeplot(X,hjd,filename,xlo,xhi)
    