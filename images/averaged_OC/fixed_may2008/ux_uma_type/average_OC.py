# Calculates the average of the O-C diagrams in the 'OC' file 
# Time units are orbital phase

import pylab as pl
import string

files = open('OC','r').readlines()
# Dict to hold ephemerides. '1' -> Archive,   '2' -> August, 'P' -> Period
ephemeris = {}
ephemeris['1'] = 2452525.374416
ephemeris['2'] = 2453964.330709

pl.figure()

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
    tpp -= pl.average(tpp[0])
    #tpp += 1.0
    
    pp.append(tpp)
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
lt = xx < 1.2
gt = xx > 0.8
xx = xx[lt*gt]
pp = pp[lt*gt]
aa = aa[lt*gt]
sa = sa[lt*gt]
sp = sp[lt*gt]


print xx,aa,pp,sa,sp 



# average lightcurve in N bins
N = 10

# try-except block takes away points at the end of the array if array cannot be split in N equal parts
#try:
    #xx = pl.average(pl.split(xx,N),1)
    #pp = pl.average(pl.split(pp,N),1)
    #aa = pl.average(pl.split(aa,N),1)
    #sp = pl.average(pl.split(sp**2,N),1)**0.5
    #sa = pl.average(pl.split(sa**2,N),1)**0.5
    
    
#except:
    #l = int(len(xx)/N)*N
    #xx = pl.average(pl.split(xx[0:l],N),1)
    #pp = pl.average(pl.split(pp[0:l],N),1)
    #aa = pl.average(pl.split(aa[0:l],N),1)
    #sp = pl.average(pl.split(sp[0:l]**2,N),1)**0.5
    #sa = pl.average(pl.split(sa[0:l]**2,N),1)**0.5
    
# save the lightcurve

#temp = []
#temp.append(xx)
#temp.append(yy)
#pl.save('ave_oc.dat',pl.array(temp).transpose())

pl.subplot(211)
pl.errorbar(xx,aa,sa,c='r',marker='o')
pl.subplot(212)
pl.errorbar(xx,pp,sp,c='g',marker='o')
pl.show()


