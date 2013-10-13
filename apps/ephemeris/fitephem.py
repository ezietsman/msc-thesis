import numpy as n
import numpy.linalg as la


def fitephem(x,y):
    # fits straight line to eclipse times and return m,c (period,starting time) and their standard errors
    
    x = n.array(x,'d')
    y = n.array(y,'d')
    
    # build A matrix
    
    A = []
    l = []
    
    for i in range(len(x)):
        A.append([x[i],1.0])
        l.append(y[i])
        
    # calculate solutions
    At = n.transpose(A)
    AtA = n.dot(At,A)
    E = la.inv(AtA)
    Atl = n.dot(At,l)
    solutions = n.dot(E,Atl)
    
    # calculate uncertainties
    v = n.dot(A,solutions) - l
    sigma02 = (n.dot(n.transpose(v),v))/(len(x) - 2)
    sigmaxx = E*sigma02
        
    return solutions[0],solutions[1],sigmaxx[0][0]**0.5,sigmaxx[1][1]**0.5
    
    
    
    
        