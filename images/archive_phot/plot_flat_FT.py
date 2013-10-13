# plot all the flattened lightcurves and FT's of them in this directory

import pylab as pl
import os
import astronomy as ast
import string



# ephemeris
T0 = 2452525.3744165
P = 0.1545255


#files = os.listdir(os.curdir)
myfile = open('list','r')
files = myfile.readlines()

DNOlist = ['6544_', 'S6549','S6551','S6564','S6660','S6570']
lpDNOlist = ['6544_']


pl.figure(figsize=(6,4))
pl.subplots_adjust(hspace=0.5,left=0.15,right=0.95)
for f in files:
    f = string.strip(f)
    if f[-6:] == 'FF.dat':
        print f
        X = pl.load(f)
        x = X[:,0]
        y = X[:,1]
        
        ## clip big values of y
        
        #lt = y < 0.08
        #gt = y > -0.08
        
        #y = y[lt*gt]
        #x = x[lt*gt]
        
        freq,a = ast.signal.dft(x,y,0,4000,1)

        pl.subplot(211)
        phase = (x-T0)/P - int(((x-T0)/P)[0])
        pl.plot(phase,y,'k.')
        #yl = pl.ylim()
        #pl.ylim(yl[1],yl[0])
        pl.xlim(phase[0]-0.1,phase[0]+1.75)
        
        pl.ylabel('Intensity')
        pl.xlabel('Orbital Phase')
        
        pl.subplot(212)
        pl.plot(freq,a,'k')
        pl.xlabel('Frequency (c/d)')
        pl.ylabel('Amplitude')
        
        # mark DNOs and lpDNOs
        if f[-13:-8] in DNOlist:
            gt = freq > 3000
            freq2 = freq[gt]
            a2 = a[gt]
            nu = freq2[a2.argsort()[-1]]
            pl.vlines(nu,0.002,0.0025,color='k',linestyle='solid')
            pl.text(nu-125,0.00255,'DNO',fontsize=11)
        
        if f[-13:-8] in lpDNOlist:
            gt = freq > 800
            lt = freq < 1100
            freq2 = freq[gt*lt]
            a2 = a[gt*lt]
            nu = freq2[a2.argsort()[-1]]
            pl.vlines(nu,0.002,0.0025,color='k',linestyle='solid')
            pl.text(nu-125,0.00255,'lpDNO',fontsize=11)

        pl.savefig('%s.png'% f[:-4])
        pl.clf()