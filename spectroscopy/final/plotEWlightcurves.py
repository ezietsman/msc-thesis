import pylab as pl
import astronomy as ast

plotfile = open('splot.log').readlines()
HJDfile = open('HJD.dat').readlines()


ew = []
center = []

HJD = pl.array([float(d) for d in HJDfile][1:-2])


for line in plotfile:
    # if the line doesn't contain letters
    if line.find('EC') == -1 and line.find('flux') == -1and len(line.strip()) > 0:
        print line
        c,temp1,temp2,e = [float(num) for num in line.split()]
        ew.append(e)
        center.append(c)

ew = pl.array(ew[:-2])
center = pl.array(center[:-2])

print len(ew),len(center),len(HJD)

#X = pl.load('rv.dat')
#ew = X[:,0]
pl.figure()
pl.subplot(311)
pl.title('Line Center')
pl.plot(center,'o')

pl.subplot(312)
pl.plot(HJD,ew,'go')
pl.title('Equivalent Width')

pl.subplot(313)

f,a = ast.signal.dft(HJD,ew,0,4000,1)
pl.plot(f,a)
pl.title('Equivalent Width FT')

pl.show()


temp = []
temp.append(HJD)
temp.append(ew)
temp.append(center)
pl.save('EW.dat',pl.array(temp).transpose())
