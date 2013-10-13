# script to make plots for all the archive lighcurves used.


import pylab as pl
import string
import astronomy as ast

myfile = open('FFlc','r').readlines()



def makeplot(filename):
    T0 = 2452525.374416
    P = 0.154525
    
    X = pl.load(filename)
    x = X[:,0]
    y = X[:,1]
    print x[0] # check for HJD faults
    
    #orbital phase
    p = (x-T0)/P
    
    pl.figure(figsize=(6,4))
    pl.subplots_adjust(hspace=0.47,left=0.16)
    
    pl.subplot(211)
    pl.scatter(p,y,marker='o',s=0.1,color='k')
    pl.ylim(-0.06,0.06)
    pl.xlim(pl.average(p)-1.25,pl.average(p)+1.25)
    pl.ylabel('Intensity')
    pl.xlabel('Orbital Phase')
    
    pl.subplot(212)
    f,a = ast.signal.dft(x,y,0,4000,1)
    pl.plot(f,a,'k')
    pl.ylabel('Amplitude')
    pl.xlabel('Frequency (c/d)')
    #pl.ylim(yl[0],yl[1])
    
    #pl.vlines(3636,0.002,0.0025,color='k',linestyle='solid')
    #pl.vlines(829,0.002,0.0025,color='k',linestyle='solid')
    #pl.text(3500,0.00255,'DNO',fontsize=11)
    #pl.text(700,0.00255,'lpDNO',fontsize=11)
    pl.ylim(0.0,0.004)
    pl.savefig('%spng'%filename[:-3])






for f in myfile:
    print f
    f = string.strip(f)
    makeplot(f)
    
    
pl.show()