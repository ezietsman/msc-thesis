# script to print some things for a latex table

import string
import pylab as pl

myfile = open('lc','r').readlines()

for f in myfile:
    X = pl.load(string.strip(f))
    dt = (X[:,0][1] -X[:,0][0])*86400.0
    hjd = X[:,0][0]
    l = (max(X[:,0]) - min(X[:,0]))*86400.0/3600.0
    
    print string.strip(f)[:5] ,' & ', ' check ',' & ',hjd,' & ',round(l,2),' & ',round(dt,1) ,'& check & check \\\\ '