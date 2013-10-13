# script to calculate trailed FT of the lightcurve

import astronomy as ast
import pylab as pl
import scipy.stats as sci

X = pl.load('S7651_FF_norm.dat')
x = X[:,0]
y = X[:,1]
z = X[:,2]

N = len(x)
fitlength = 100
#x -= int(x[0])

# ephemeris
T0 = 2453964.3307097
P = 0.1545255

#x = (x - T0) / P

ft = []
date = []
peaks = []

f0 = 500
f1 = 1500

for i in range(0,N,int(fitlength/2.0)):
		
	if i + fitlength/2.0 <= len(x):
                print 'somewhere'
                
                date.append(pl.average(x[i:i + fitlength]))
                f,a = ast.signal.dft(x[i:i+fitlength],y[i:i+fitlength],f0,f1,1)
                ft.append(a)
                #sort,argsort = sci.fastsort(a)
                #peaks.append(f[argsort[-1]])
                
		# / len(x[i:i+fitlength]))
                print i, i+fitlength
	else:
                print 'finally'
		#x = fitwave(y[i:len(t)+1],t[i:len(t)+1],freq)
                f,a = ast.signal.dft(x[i:len(x)+1],y[i:len(x)+1],f0,f1,1)
                ft.append(a)
                #sort,argsort = sci.fastsort(a)
                #peaks.append(f[argsort[-1]])
		date.append(pl.average(x[i:-1]))# / len(x[i:-1]))
        print i
                        
print '\n\n\n\n',N
print pl.shape(ft)

pl.figure(figsize=(6,4))

## calculate phase
x = (x - T0) / P
date = (pl.array(date) - T0) / P

#lt = date < 1.2
#gt = date > 0.8

#date = date[gt*lt]


levels=pl.arange(0.0,0.008 ,0.0001)
im = pl.contourf(pl.array(ft).transpose(),levels=levels,extent=(date[0],date[-1],f0,f1),cmap=pl.cm.jet)
pl.colorbar(im,orientation='horizontal',shrink=1.0,ticks=list(pl.arange(min(levels),max(levels),0.002)))
#pl.xlabel('HJD (+2453965)')
pl.xlabel('Orbital Phase')
pl.ylabel('Frequency (cycles/day)')
yt = pl.yticks()
pl.yticks(yt[0][1:-1])
#pl.xlim(0.8,1.2)

pl.subplots_adjust(bottom=0.34)

pl.savefig('S7651_trailed_FT_lpDNO.png')

pl.show()






