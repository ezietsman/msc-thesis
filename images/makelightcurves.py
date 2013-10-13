from pylab import *


# read data
X1 = load('ec2117ans_1_cc.dat')
X2 = load('ec2117ans_2_cc.dat')
X3 = load('ec2117ans_3_cc.dat')
X4 = load('ec2117ans_4_cc.dat')

x1 = X1[:,0]
y1 = X1[:,2]

x2 = X2[:,0]
y2 = X2[:,2]

x3 = X3[:,0]
y3 = X3[:,1]

x4 = X4[:,0]
y4 = X4[:,1]



figure(figsize = (6,4))



#plot(x1,y1,'.')
#plot(x2-1,y2+2.2,'g.')
#plot(x3-2,y3+3,'r.')
#plot(x4-3,y4+4.5,'k.')
scatter(x1,y1,s=2,color='b',faceted=False,label='S7651')
scatter(x2-1,y2+2.2,s=2,color='g',faceted=False,label='S7655')
scatter(x3-2,y3+3,s=2,color='r',faceted=False,label='S7659')
scatter(x4-3,y4+4.5,s=2,color='y',faceted=False,label='S7661')
xlabel('Fractional day',fontsize = 12)
ylabel('Relative \nMagnitude',fontsize = 12)
ylim(20,11.5)
legend()

savefig('lightcurves.png')
show()











