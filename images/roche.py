# try to make a Roche-lobe plot
# let z = 0
# using formula from Warner (1995) p31

from pylab import *

#calculate some parameters
G=1.0
Msun = 1.0
M1 = 0.5*Msun
M2 = 0.125*Msun
mu = M2/(M1+M2)
P = 4*3600.0   # 4 hours in seconds
omega = 2*pi/P
q = M2/M1
a = ((P**2.0)*G*(M1+M2)/(4*pi**2.0))**(0.333333333333333)

# make a calculation grid
x = arange(-0.75*a,1.5*a,a/100.0,'d')
y = arange(-0.75*a,0.75*a,a/100.0,'d')
X,Y = meshgrid(x,y)

#calculate the potentials
phi = -1.0*G*M1/sqrt(X**2 + Y**2 + 1.0e-20) - 1.0*G*M2/sqrt((X-a)**2+Y**2+1.0e-20) - 0.5*(omega**2)*((X-mu*a)**2 + Y**2)

phi = abs(phi)
levels=[0.0070,0.0075,0.008,0.01]
#gray()
#levels = arange(0.007,0.1,0.0001)
figure(figsize=(6,4))
#levels = arange(0.007,0.1,0.001)
CS = contour(phi,levels=levels,colors='k',extent=(-0.75,1.5,-0.75,0.75))
#CS = contourf(phi,levels=levels,extent=(-0.75,1.5,-0.75,0.75),cmap=cm.jet)

#colorbar()
text(0.50,0,'L1',fontsize=12)
text(0,0,'1',fontsize=12)
text(0.98,0,'2',fontsize=12)
draw()


show()

#Eureka!!!