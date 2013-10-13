from pylab import *
from astronomy import *

t = arange(0.0,0.5,0.01)
f = 0.33*sin(2*pi*15.0*t)

t,f = read_file_interactive('run2_flat.dat')

#figure(figsize=(6,4))
subplot(211)
plot(t,f,'g.')
xlabel(r'Time')
ylabel(r'Value')
ylim(-0.2,0.2)

subplot(212)
freq,amp = periodogram(t,f,0,5000,0.1)
plot(freq,amp)
xlabel(r'Frequency')
ylabel(r'Amplitude')
savefig(r'image.png')
