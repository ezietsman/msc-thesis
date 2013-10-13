from pylab import *
import astronomy as ast

X = load('ec2117ans_2_cc_FF.dat')
x = X[:,0]
y = X[:,1]
l = len(x)
xx = x[2*l/4.0:3*l/4.0]
yy = y[2*l/4.0:3*l/4.0]
f,a = ast.signal.dft(xx,yy,0,4000,1)
subplot(211)
plot(f,a)
xlim(0,500)
subplot(212)
plot(xx,yy)
subplot(211)
plot(f,a)
xlim(0,500)
subplot(211)
subplot(212)
plot(xx,yy)
X = load('ec2117ans_2_cc.dat')
x = X[:,0]
y = X[:,2]
l = len(x)
xx = x[2*l/4.0:3*l/4.0]
yy = y[2*l/4.0:3*l/4.0]
f,a = ast.signal.dft(xx,yy,0,4000,1)
subplot(211)
plot(f,a)
ylim(0,0.01)

show()
