# program to make plots of the lightcurves for inclusion in dissertation
import pylab as pl
import astronomy as ast

runlen = []
# ephemeris
T0 = 2453964.3307097
P = 0.1545255


X = pl.load('S7651/S7651_FF_norm.dat')
x1 = X[:,0]
y1 = X[:,1] 
z1 = X[:,2]
f1,a1 = ast.signal.dft(x1,y1,0,4000,1)
x1 = (X[:,0]-T0)/P
runlen.append(max(x1)-min(x1))

X = pl.load('S7655/S7655_FF_norm.dat')
x2 = X[:,0]
y2 = X[:,1] 
z2 = X[:,2]
f2,a2 = ast.signal.dft(x2,y2,0,4000,1)
x2 = (X[:,0]-T0)/P
runlen.append(max(x2)-min(x2))

    
X = pl.load('S7659/S7659_FF_norm.dat')
x3 = X[:,0]
y3 = X[:,1] 
z3 = X[:,2]
f3,a3 = ast.signal.dft(x3,y3,0,4000,1)
x3 = (X[:,0]-T0)/P
runlen.append(max(x3)-min(x3))

X = pl.load('S7661/S7661_FF_norm.dat')
x4 = X[:,0] -3 + 2453967 
y4 = X[:,1] 
z4 = X[:,2]
f4,a4 = ast.signal.dft(x4,y4,0,4000,1)
x4 = (X[:,0] -3 + 2453967 - T0)/P
runlen.append(max(x4)-min(x4))
    
        
print runlen
runlen = max(runlen)+0.4





##############################################################################################
pl.figure(figsize=(6,4))

pl.subplots_adjust(hspace=0.47,left=0.16)

pl.subplot(211)
pl.scatter(x1,y1,marker='o',s=0.1,color='k')
pl.ylim(-0.06,0.06)
pl.xlim(pl.average(x1)-runlen/2,pl.average(x1)+runlen/2)
pl.ylabel('Intensity')
pl.xlabel('Orbital Phase')

pl.subplot(212)
#f,a = ast.signal.dft(x1,y1,0,4000,1)
pl.plot(f1,a1,'k')
pl.ylabel('Amplitude')
pl.xlabel('Frequency (c/d)')
pl.ylim(0.0,0.007)
pl.vlines(3560,0.002,0.0025,color='k',linestyle='solid')
pl.vlines(950,0.002,0.0025,color='k',linestyle='solid')
pl.text(3425,0.00255,'DNO',fontsize=11)
pl.text(750,0.00255,'lpDNO',fontsize=11)
pl.ylim(0.0,0.007)

pl.savefig('S7651/S7651.png')

##############################################################################################
##############################################################################################
pl.figure(figsize=(6,4))
pl.subplots_adjust(hspace=0.47,left=0.16)

pl.subplot(211)
pl.scatter(x2,y2,marker='o',s=0.1,color='k')
pl.ylim(-0.06,0.06)
#pl.xlim(min((x2-T0)/P),max((x2-T0)/P))
pl.xlim(pl.average(x2)-runlen/2,pl.average(x2)+runlen/2)
pl.ylabel('Intensity')
pl.xlabel('Orbital Phase')

pl.subplot(212)
#f,a = ast.signal.dft(x2,y2,0,4000,1)
pl.plot(f2,a2,'k')
pl.ylabel('Amplitude')
pl.xlabel('Frequency (c/d)')
#pl.ylim(yl[0],yl[1])

pl.vlines(3636,0.002,0.0025,color='k',linestyle='solid')
pl.vlines(829,0.002,0.0025,color='k',linestyle='solid')
pl.text(3500,0.00255,'DNO',fontsize=11)
pl.text(700,0.00255,'lpDNO',fontsize=11)
pl.ylim(0.0,0.007)
pl.savefig('S7655/S7655.png')

##############################################################################################
##############################################################################################


pl.figure(figsize=(6,4))
pl.subplots_adjust(hspace=0.47,left=0.16)

pl.subplot(211)
pl.scatter(x3,y3,marker='o',s=0.1,color='k')
pl.ylim(-0.06,0.06)
#pl.xlim(min((x3-T0)/P),max((x3-T0)/P))
pl.xlim(pl.average(x3)-runlen/2,pl.average(x3)+runlen/2)
pl.ylabel('Intensity')
pl.xlabel('Orbital Phase')

pl.subplot(212)
#f,a = ast.signal.dft(x3,y3,0,4000,1)
pl.plot(f3,a3,'k')
pl.ylabel('Amplitude')
pl.xlabel('Frequency (c/d)')
#pl.ylim(yl[0],yl[1])
pl.ylim(0.0,0.007)
pl.savefig('S7659/S7659.png')


##############################################################################################
##############################################################################################

pl.figure(figsize=(6,4))
pl.subplots_adjust(hspace=0.47,left=0.16)

pl.subplot(211)
pl.scatter(x4,y4,marker='o',s=0.1,color='k')
pl.ylim(-0.06,0.06)
#pl.xlim(min((x4-T0)/P),max((x4-T0)/P))
pl.xlim(pl.average(x4)-runlen/2,pl.average(x4)+runlen/2)
pl.ylabel('Intensity')
pl.xlabel('Orbital Phase')

pl.subplot(212)
#f,a = ast.signal.dft(x4,y4,0,4000,1)
pl.plot(f4,a4,'k')
pl.ylabel('Amplitude')
pl.xlabel('Frequency (c/d)')
#pl.ylim(yl[0],yl[1])
pl.ylim(0.0,0.007)
pl.savefig('S7661/S7661.png')

##############################################################################################


pl.show()



