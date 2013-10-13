from pylab import *
import astronomy as ast



X1 = load('ec2117ans_1_c.dat')
x1 = X1[:,0]
y1 = X1[:,2]

T0 = 2453964.3307097
P = 0.1545255



figure(figsize=(6,4))

subplot(211)
subplots_adjust(hspace=0.6)

#plot(x1,y1,'.')
scatter((x1-T0)/P,y1,s=0.8,faceted=False)
xlabel('Orbital Phase')
ylabel('Relative Magnitude')
title('Original Lightcurve')
ylim(max(y1)+0.25,min(y1)-0.25)


subplot(212)
x2,y2 = ast.signal.dft(x1,y1,0,7000,1)
plot(x2,y2,'k-')
xlabel('Frequency (cycles/day)')
ylabel('Amplitude (mag)')
title('Periodogram')
xlim(0,7000)
ylim(0,0.005)

savefig('unflattened.png')

show()

