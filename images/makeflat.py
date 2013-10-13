from pylab import *
import astronomy as ast

# to format the labels better
from matplotlib.ticker import FormatStrFormatter
fmt = FormatStrFormatter('%1.4f')  # or whatever


X1 = load('/home/ewald/werk/msc_thesis/images/august_phot/S7651/S7651_FF_norm.dat')
x1 = X1[:,0]
y1 = X1[:,1]

T0 = 2453964.3307097
P = 0.1545255

figure(figsize=(8,6))

subplots_adjust(hspace=0.6,left=0.16)


subplot(211)


#plot(x1,y1,'.')
scatter((x1-T0)/P,y1,s=0.8,faceted=False,color='b')
xlabel('Orbital Phase')
ylabel('Intensity')
title('Flattened Lightcurve')
#ylim(max(y1)+0.05,min(y1)-0.05)


ax = subplot(212)

x2,y2 = ast.signal.dft(x1,y1,0,7000,1)

plot(x2,y2,'k-')
xlabel('Frequency (cycles/day)')
ylabel('Amplitude')
vlines(3560,0.002,0.0025,color='k',linestyle='solid')
vlines(950,0.002,0.0025,color='k',linestyle='solid')
text(3350,0.00255,'DNO',fontsize=11)
text(700,0.00255,'lpDNO',fontsize=11)
xlim(0,7000)
title('Periodogram')

ax.yaxis.set_major_formatter(fmt) 

savefig('flattened.png')


show()

