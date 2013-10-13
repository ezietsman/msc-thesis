# program splits lightcurve into n bins and gives fourier transforms and
# stats for each bin
# also show plots of FTs and lightcurves of each bin

import pylab as pl
import astronomy as ast
import scipy.stats as stats
import os
import string


os.system('ls -l')
filename = raw_input('Open which file ? : ')
os.system('less %s' % filename)
cols = string.split(raw_input('Use which columns ? : '))

# load a lightcurve
X = pl.load(filename)
x = X[:,int(cols[0])-1]
y = X[:,int(cols[1])-1]
z = X[:,int(cols[2])-1]


n = int(raw_input('Split into how many bins?  : '))

# split into n bins
x_bins = pl.array_split(x,n)
y_bins = pl.array_split(y,n)
z_bins = pl.array_split(z,n)


f = string.split(raw_input('Start End freq  : '))
f0 = float(f[0])
f1 = float(f[1])

print f0,f1
# now do fourier transform on every bins and give stats
ft_bins = [ast.signal.dft(x_bins[i],y_bins[i],f0,f1,1) for i in range(n)]

#print pl.shape(ft_bins)
print '\nBin\t','Amp\t\t\t','F c/d\t\t','F(s)\n\n'
for i in range(n):
    sort, argsort = stats.fastsort(ft_bins[i][1])
    amp = ft_bins[i][1][argsort[-1]]
    freq = ft_bins[i][0][argsort[-1]]
    print i,'\t',amp,'\t',freq,'\t',86400.0/freq
print '\n\n\n'


# make plots
pl.figure(figsize=(9,12))
for i in range(n):
    plots = '%s1%s' % (n,i+1)
    pl.subplot(plots)
    pl.plot(ft_bins[i][0],ft_bins[i][1],'k')

# Flattened lightcurve
pl.figure(figsize=(9,12))
for i in range(n):
    plots = '%s1%s' % (n,i+1)
    pl.subplot(plots)
    pl.plot(x_bins[i],y_bins[i],'k.')
pl.title('filtered')
# original ligthcurves

pl.figure(figsize=(9,12))
for i in range(n):
    plots = '%s1%s' % (n,i+1)
    pl.subplot(plots)
    pl.plot(x_bins[i],y_bins[i]+z_bins[i],'k.')
pl.title('Unfiltered')

pl.show()







