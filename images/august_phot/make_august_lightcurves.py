# program to make plots of the lightcurves for inclusion in dissertation
import pylab as pl
#import astronomy as ast

X = pl.load('S7651/S7651_FF_norm.dat')
x1 = X[:,0]
y1 = X[:,1] 
z1 = X[:,2]

X = pl.load('S7655/S7655_FF_norm.dat')
x2 = X[:,0]
y2 = X[:,1] 
z2 = X[:,2]
    
X = pl.load('S7659/S7659_FF_norm.dat')
x3 = X[:,0]
y3 = X[:,1] 
z3 = X[:,2]

X = pl.load('S7661/S7661_FF_norm.dat')
x4 = X[:,0] -3 + 2453967 
y4 = X[:,1] 
z4 = X[:,2]

##############################################################################################
pl.figure(figsize=(6,3))

t1 = int(x1[0])
t2 = int(x2[0])
t3 = int(x3[0])
t4 = int(x4[0])

pl.plot(x1-t1,y1+z1+3.5,'k,')
pl.plot(x2-t2,y2+z2+2.2,'k,')
pl.plot(x3-t3,y3+z3+1.1,'k,')
pl.plot(x4-t4,y4+z4,'k,')

pl.xlabel('Fractional Day')
pl.ylabel('Normalised\nIntensity')
pl.xlim(0.275,0.65)

pl.text(0.52,3.0,'S7651')
pl.text(0.6,1.8,'S7655')
pl.text(0.52,0.6,'S7659')
pl.text(0.46,-0.5,'S7661')
pl.subplots_adjust(bottom=0.15)

pl.savefig('../lightcurves.png')
pl.show()



