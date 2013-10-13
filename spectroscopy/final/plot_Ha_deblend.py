# plot deblended Ha velocities and stuff

import pylab as pl
import pyfits as pf
import os

files = os.listdir(os.curdir)
#ff = []
date = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        date.append(float(pf.getheader(f)['HJD']))
        #ff.append(f)

# calculate phase based on eclipse ephemeris
T0 = 2453964.3307097
P = 0.1545255


c = 2.99792458e5

phase = (pl.array(date) - T0)/P

blue = pl.load('Ha_blue.dat')[:,0]
red = pl.load('Ha_red.dat')[:,0]
#X = pl.load('Ha_deblend.dat')

#red_vel = X[:,2]
#blue_vel = X[:,1]
#phase = X[:,0]


blue_vel = (blue - 6563.0) / 6563.0 * c
red_vel = (red - 6563.0) / 6563.0 * c  
pl.figure(figsize=(6,4))
pl.plot(phase,blue_vel,'bo-')
pl.plot(phase,red_vel,'ro-')
pl.ylim(-750,750)
pl.ylabel('Line Velocity (km/s)')
pl.xlabel('Orbital Phase')
pl.show()


temp = []

temp.append(phase)
temp.append(blue_vel)
temp.append(red_vel)


pl.save('Ha_deblend.dat', pl.array(temp).transpose())



