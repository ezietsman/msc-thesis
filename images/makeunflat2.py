from pylab import *
import astronomy as ast

# to format the labels better
from matplotlib.ticker import FormatStrFormatter
fmt = FormatStrFormatter('%1.2g')  # or whatever


X1 = load('ec2117ans_1_c.dat')
x1 = X1[:,0]
y1 = 10**(X1[:,2]/(-2.5))
y1 /= average(y1)

T0 = 2453964.3307097
P = 0.1545255

figure(figsize=(6,4))
subplots_adjust(hspace=0.6,left=0.16)


ax = subplot(211)


#plot(x1,y1,'.')
scatter((x1-T0)/P,y1,s=0.8,faceted=False)
xlabel('Orbital Phase')
ylabel('Intensity')
title('Original Lightcurve')
#ylim(min(y1)-0.0000005,max(y1)+0.0000005)
ax.yaxis.set_major_formatter(fmt) 

ax = subplot(212)

x2,y2 = ast.signal.dft(x1,y1,0,7000,1)

plot(x2,y2,'k-')
xlabel('Frequency (cycles/day)')
ylabel('Amplitude')
#vlines(3560,0.000000025,0.00000003,color='k',linestyle='solid')
#vlines(950,0.000000025,0.00000003,color='k',linestyle='solid')
#text(3350,0.000000035,'DNO',fontsize=10)
#text(700,0.000000035,'lpDNO',fontsize=10)
xlim(0,7000)
ylim(0,0.004)
title('Periodogram')

#ax.yaxis.set_major_formatter(fmt) 

savefig('unflattened.png')


show()

