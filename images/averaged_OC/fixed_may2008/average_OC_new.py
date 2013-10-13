# Calculates the average of the O-C diagrams in the 'OC' file 
# Time units are orbital phase

import pylab as pl
import string

files = open('OC','r').readlines()
# Dict to hold ephemerides. '1' -> Archive,   '2' -> August, 'P' -> Period
ephemeris = {}
ephemeris['1'] = 2452525.374416
ephemeris['2'] = 2453964.330709

#pl.figure()

xx = []
aa = []
pp = []
sp = []
sa = []

for f in files:
    print 'Reading %s ' % f
    name, eph = string.split(f)
    T0 = ephemeris[eph]
    P = 0.154525
    
    X = pl.load(name)
    x = (X[:,2] - T0)/P
    xx.append(x - int(x[0]))
    aa.append(X[:,0])
    
    # let phase at 0.8 -> 1.0
    tpp = X[:,1]
    #tpp -= tpp[0]
    #tpp += 1.0
    
    pp.append(tpp-pl.average(tpp))
    sa.append(X[:,3])
    sp.append(X[:,4])
    

# now sort observations in terms of orbital phase
xx = pl.array([i for i in pl.flatten(xx)])
pp = pl.array([i for i in pl.flatten(pp)])
aa = pl.array([i for i in pl.flatten(aa)])
sa = pl.array([i for i in pl.flatten(sa)])
sp = pl.array([i for i in pl.flatten(sp)])

arg = xx.argsort()
xx = xx[arg]
pp = pp[arg]
aa = aa[arg]
sa = sa[arg]
sp = sp[arg]


# limit orb phase to [0.8,1.2]
lt = xx < 1.3
gt = xx > 0.8
xx = xx[lt*gt]
pp = pp[lt*gt]
aa = aa[lt*gt]
sa = sa[lt*gt]
sp = sp[lt*gt]


#print xx,aa,pp,sa,sp 



# average lightcurve in N bins
N = 20

# try-except block takes away points at the end of the array if array cannot be split in N equal parts
try:
    xx = pl.average(pl.split(xx,N),1)
    pp = pl.average(pl.split(pp,N),1)
    aa = pl.average(pl.split(aa,N),1)
    sp = pl.average(pl.split(sp**2,N),1)**0.5
    sa = pl.average(pl.split(sa**2,N),1)**0.5
    
    
except:
    
    l = int(len(xx)/N)*N
    dl = len(xx)-l
    print 'Dropped %s of %s points' % (dl,len(xx))
    xx = pl.average(pl.split(xx[dl/2:-dl/2],N),1)
    pp = pl.average(pl.split(pp[dl/2:-dl/2],N),1)
    aa = pl.average(pl.split(aa[dl/2:-dl/2],N),1)
    sp = pl.average(pl.split(sp[dl/2:-dl/2]**2,N),1)**0.5
    sa = pl.average(pl.split(sa[dl/2:-dl/2]**2,N),1)**0.5
    
    
# save the lightcurve

temp = []
temp.append(aa)
temp.append(pp)
temp.append(xx)
temp.append(sa)
temp.append(sp)
pl.save('ave_oc.dat',pl.array(temp).transpose())


pl.figure(figsize=(6,4))
pl.subplots_adjust(left=0.16,hspace=0.001)

ax1=pl.subplot(211)
pl.grid()
pl.ylabel('Amplitude')
pl.errorbar(xx,aa,sa,fmt='ro')
yt = pl.yticks()
ax1.set_yticks(yt[0][1:-1])


ax2=pl.subplot(212)
pl.errorbar(xx,pp,sp,fmt='go')
pl.xlabel('Orbital Phase')
pl.ylabel('Phase (O-C)')
pl.grid()
yt = pl.yticks()
#ax2.set_yticks(yt[0][1:-1])
pl.ylim(-1.2,0.6)

pl.setp(ax1.get_xticklabels() , visible=False)


pl.savefig('average_OC.png')
pl.show()


