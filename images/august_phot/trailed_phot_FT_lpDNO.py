# script to calculate trailed FT of the lightcurve

import astronomy as ast
import pylab as pl
import scipy.stats as sci

#X2 = pl.load('run2_flat.dat')
#X = pl.load('ec2117ans_2_cc.dat')
X = pl.load('S7651_FF.dat')
x = X[:,0]
y = X[:,1]
z = X[:,2]
# original lightcurve

#z = X2[:,2] + X2[:,1]

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

#pl.figure(figsize=(8,4))
pl.subplots_adjust(hspace=0.001)
ax1=pl.subplot(211)

# calculate phase
x = (x - T0) / P
date = (pl.array(date) - T0) / P

pl.scatter(x,y+z,marker='o',s=0.1)
#yl = pl.ylim()
#pl.ylim(yl[1],yl[0])
pl.xlim(date[0],date[-1])
pl.ylabel('Intensity')
yt = pl.yticks()
pl.yticks(yt[0][1:-1])


pl.subplot(212)
#im = pl.imshow(pl.array(ft).transpose(),aspect='auto',interpolation='bilinear',extent=(date[0],date[-1],f1,f0,),cmap=pl.cm.jet)
levels=pl.arange(0.000,0.00000005,0.000000001)
im = pl.contourf(pl.array(ft).transpose(),levels=levels,extent=(date[0],date[-1],f0,f1),cmap=pl.cm.jet)
pl.colorbar(im,orientation='horizontal',shrink=1.0)
#pl.xlabel('HJD (+2453965)')
pl.xlabel('Orbital Phase')
pl.ylabel('Frequency (cycles/day)')
yt = pl.yticks()
pl.yticks(yt[0][1:-1])

pl.subplots_adjust(bottom=0.24,right=0.98,left=0.15)

xticklabels = ax1.get_xticklabels()
pl.setp(xticklabels, visible=False)

#pl.figure()
#pl.plot(date,peaks,'-')
##im = pl.contourf(pl.array(ft).transpose(),levels=levels,extent=(date[0],date[-1],f1,f0),cmap=pl.cm.jet,origin='lower')
pl.show()






