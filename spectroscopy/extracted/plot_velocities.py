import pylab as pl


# first plot the gaussian results

P = pl.load('ec2117ans_2_cc.dat')
X = pl.load('Ha.dat')
t = int(X[:,0][0])
E = 2453964.3307097

# calculate t in terms of orbital phase

# period in days
period = 0.1545255

phase = (X[:,0]-E)/period - int(((X[:,0]-E)/period)[0])
print phase

# velocities

pl.figure(figsize=(6,4))
#pl.subplot(212)

pl.plot(phase,X[:,2],'o-',label=r'$H_{\alpha}$')
X = pl.load('Hb.dat')
pl.plot(phase,X[:,2],'x-',label=r'$H_{\beta}$')
X = pl.load('HeII.dat')
pl.plot(phase,X[:,2],'^-',label=r'$HeII$')
pl.xlabel('Orbital Phase')
pl.ylabel('Velocity [km/s]')
pl.legend()
pl.grid()
pl.title('EC2117-54 Emission Line Velocities')
xlim = pl.xlim()
pl.ylim(-300,300)
pl.savefig('vel_gauss.png')

X = pl.load('Ha_ew.dat')

# period in days
pl.figure(figsize=(6,4))
#pl.subplot(212)
pl.plot(phase,X[:,1],'o-',label=r'$H_{\alpha}$')
X = pl.load('Hb_ew.dat')
pl.plot(phase,X[:,1],'x-',label=r'$H_{\beta}$')
X = pl.load('HeII_ew.dat')
pl.plot(phase,X[:,1],'^-',label=r'$HeII$')
pl.xlabel('Orbital Phase')
pl.ylabel('Velocity [km/s]')
pl.legend()
pl.grid()
pl.title('EC2117-54 Emission Line Velocities')
xlim = pl.xlim()
pl.savefig('vel_ew.png')
X = pl.load('Ha.dat')

# period in days
pl.figure(figsize=(6,4))
#pl.subplot(212)
pl.plot(phase,X[:,3],'o-',label=r'$H_{\alpha}$')
X = pl.load('Hb.dat')
pl.plot(phase,X[:,3],'x-',label=r'$H_{\beta}$')
X = pl.load('HeII.dat')
pl.plot(phase,X[:,3],'^-',label=r'$HeII$')
pl.xlabel('Orbital Phase')
pl.ylabel('FWHM (Angstrom)')
pl.legend()
pl.grid()
pl.title('EC2117-54 Line Widths')
pl.ylim(10,34)
pl.savefig('lw_gauss.png')


X = pl.load('Ha_ew.dat')

# period in days
pl.figure(figsize=(6,4))
#pl.subplot(212)
pl.plot(phase,X[:,2],'o-',label=r'$H_{\alpha}$')
X = pl.load('Hb_ew.dat')
pl.plot(phase,X[:,2],'x-',label=r'$H_{\beta}$')
X = pl.load('HeII_ew.dat')
pl.plot(phase,X[:,2],'^-',label=r'$HeII$')
pl.xlabel('Orbital Phase')
pl.ylabel('Equivalent width (Angstrom)')
pl.legend()
pl.grid()
pl.title('EC2117-54 Emission Line Equivalent Widths')
pl.ylim(-35,15)
pl.savefig('lw_ew.png')

#pl.subplot(211)
#phase = (P[:,0]-1+t-E)/period - int(((P[:,0]-1+t-E)/period)[0])
#neg = phase < 0.5
#phase[neg] += 1.0
#pl.plot(phase,P[:,2],'.')
#ylim = pl.ylim()
#pl.ylim(ylim[1],ylim[0])
#pl.ylabel('Relative Magnitude')
#pl.xlim(xlim[0],xlim[1])
#pl.title('Photometry Lightcurve')
#pl.grid()

print '\n\n\n\n'
print min(phase), max(phase)
    

pl.show()
