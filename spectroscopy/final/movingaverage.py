# program to develop and test moving average function

import pylab as pl
import astronomy as ast

def movingaverage(x,L):
    ma = pl.zeros(len(x),dtype='Float64')
    # must take the lead-up zone into account (prob slow)
    for i in range(0,L):
        
        ma[i] = pl.average(x[0:i+1])

    for i in range(L,len(x)):
        #print i
        ma[i] = ma[i-1] + 1.0/L*(x[i]-x[i-L])
        
    return ma





if __name__=='__main__':
    x = pl.arange(0.0,0.25,5.7870370370370373e-05)
    y = pl.sin(2*pl.pi*(3000*x+pl.rand())) + pl.sin(2*pl.pi*(2000*x+pl.rand())) + pl.sin(2*pl.pi*(1000*x+pl.rand())) + pl.sin(2*pl.pi*(500*x+pl.rand())) + pl.sin(2*pl.pi*(250*x+pl.rand()))
    
    
    xnew = movingaverage(x,20)
    ynew = y - movingaverage(y,20)
    #ynew2 = pl.movavg(y,10)
    
    print len(x),len(xnew)
    
    pl.figure()
    pl.plot(x,y,'b-')
    pl.plot(xnew,ynew,'r-')
    #pl.plot(ynew2,'g-')
    #pl.ylim(-1.5,1.5)
    
    pl.figure()
    f,a = ast.signal.dft(x,y,0,4000,1)
    pl.plot(f,a,'b-')
    f,a = ast.signal.dft(xnew,ynew,0,4000,1)
    pl.plot(f,a,'r-')
    
    
    pl.show()
    