# program to calculate average O-C diagram from files in current folder

import pylab as pl
import os
import string
from matplotlib.ticker import FormatStrFormatter

fmt = FormatStrFormatter('%1.4g')  # or whatever


files = os.listdir(os.curdir)
anew = []
pnew = []
xnew = []
sanew = []
spnew = []
lcxnew = []
lcynew = []

for f in files:
    f = string.strip(f)
    
    if f[-4:] == '.dat':
        if f[-8:] != 'FFOP.dat':
            print f
            X = pl.load(f)
            
            x = X[:,2]
            # limit orbital phase between 0.8 and 1.2
            lt = x < 1.2
            gt = x > 0.8
            x = x[lt*gt]
    
            if len(x) != 0:
                a = X[:,0][lt*gt]
                p = X[:,1][lt*gt] - pl.average(X[:,1][lt*gt])
                sa = X[:,3][lt*gt]
                sp = X[:,4][lt*gt]
                
        
                # get outliers to fall in respectable range
                lt = p < -1.0
                p[lt] += 1.0
                gt = p > 0.5
                p[gt] -= 1.0
                
                
                
                
                anew.append(a)
                pnew.append(p)
                xnew.append(x)
                sanew.append(sa)
                spnew.append(sp)
        else:
            # make the average lightcurve
            print f
            X = pl.load(f)
            
            x = X[:,0]
 
            # limit orbital phase between 0.8 and 1.2
            lt = x < 1.2
            gt = x > 0.8
            x = x[lt*gt]
            
    
            if len(x) != 0:
                lcy = X[:,1][lt*gt] + X[:,2][lt*gt]
                lcy -= lcy[0]
                
                lcxnew.append(x)
                lcynew.append(lcy)
        
                
            
        
     
# now all points are together in a array
a = pl.concatenate(anew[:])
p = pl.concatenate(pnew[:])
x = pl.concatenate(xnew[:])
sa = pl.concatenate(sanew[:])
sp = pl.concatenate(spnew[:])
lcx = pl.concatenate(lcxnew[:])
lcy = pl.concatenate(lcynew[:])

anew = []
pnew = []
xnew = []
sanew = []
spnew = []
lcxnew = []
lcynew = []

print min(lcx), max(lcx)

# calc averages and errors for each bin
r = pl.arange(0.8,1.2,0.0125)
for i in r:
    gt = x > i
    lt = x < i + 0.0125
    gt2 = lcx > i
    lt2 = lcx < i + 0.0125
    try:
        anew.append(pl.average(a[gt*lt]))
        pnew.append(pl.average(p[gt*lt]))
        xnew.append(pl.average(x[gt*lt]))
        sanew.append(((pl.array((sa[gt*lt]))**2).mean())**0.5)
        spnew.append(((pl.array((sp[gt*lt]))**2).mean())**0.5)
        lcxnew.append(pl.average(lcx[gt2*lt2]))
        lcynew.append(pl.average(lcy[gt2*lt2]))
    except:
        continue
    
a = pl.array(anew)
p = pl.array(pnew)
x = pl.array(xnew)
sa = pl.array(sanew)
sp = pl.array(spnew)
lcx = pl.array(lcxnew)
lcy = pl.array(lcynew)

print len(lcx), len(lcy),len(a),len(p),len(x)

# make the first phase point == 1.0
p = p + 1.0-max(p)



pl.figure(figsize=(6,4))
pl.subplots_adjust(left=0.14,hspace=0.001)

# plot the lightcurve

ax3 = pl.subplot(311)        
pl.plot(lcx,lcy,'b.')
pl.xlabel('Orbital Phase')
pl.ylabel('Intensity')
#pl.ylim(0,5e-8)
yt = pl.yticks()
ax3.set_yticks(yt[0][1:-1])
pl.xlim(0.8,1.2)

ax3.yaxis.set_major_formatter(fmt) 



# plot the amplitude
ax1 = pl.subplot(312)        
pl.errorbar(x,a,sa,fmt='ro')
pl.xlabel('Orbital Phase')
pl.ylabel('Amplitude')
pl.ylim(0,5e-8)
yt = pl.yticks()
ax1.set_yticks(yt[0][1:-1])
ax1.yaxis.set_major_formatter(fmt) 
pl.xlim(0.8,1.2)
pl.grid()

# plot the phase
ax2 = pl.subplot(313)
pl.errorbar(x,p,sp,fmt='go')
pl.xlabel('Orbital Phase')
pl.ylabel('Phase (O-C)')


yt = pl.yticks()
ax2.set_yticks(yt[0][1:-1])
pl.ylim(0.0,1.1)
pl.xlim(0.8,1.2)
pl.grid()

pl.setp(ax1.get_xticklabels() , visible=False)
pl.setp(ax3.get_xticklabels() , visible=False)

pl.savefig('average_OC.png')
# remove the amplitude graph's x-axis

pl.show()