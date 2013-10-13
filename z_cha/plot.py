import pylab as pl


X = pl.load('S6061r.dat')
x1 = (X[:,0]-X[:,0][0])*86400.0
y1 = 10**(X[:,3]/(-2.5))

X2 = pl.load('ec2117ans_2_cc.dat')
x2 = (X2[:,0]-X2[:,0][0])*86400.0
y2 = 10**(X2[:,2]/(-2.5))


pl.plot(x1,y1/y1.mean(),'.',label='Z Cha')
pl.plot(x2,y2/y2.mean(),'.',label='EC2117')
pl.legend()
pl.show()

