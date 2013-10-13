from pylab import *


# read data
X2 = load('ec2117ans_2_cc.dat')

x2 = X2[:,0]
y2 = X2[:,2]


T0 = 2453964.3307097
P = 0.1545255


x2 = ((x2 - 1 + 2453965.0) - T0)/P





figure(figsize = (6,4))

# start
t0 = (2453965.53868428 - T0)/P
tf = (2453965.58158814 - T0)/P


scatter(x2 ,y2,s=2,color='k',faceted=False,label='S7655')
xlabel('Orbital phase',fontsize = 12)
ylabel('Relative Magnitude',fontsize = 12)
yl = ylim()
ylim(yl[1],yl[0])

#legend()
fill([t0,t0,tf,tf],[13.5,12.2,12.2,13.5],'g',alpha=0.3,ec='g')
xlim(min(x2)-0.1,max(x2)+0.1)
savefig('S7655_SALT_coverage.png')
show()











