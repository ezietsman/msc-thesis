# merge the spectra together i.e. make 3 ccd spectra -> 1 spectrum

import string
import os


for i in range(61,396):
    print i
    # open output file
    outputfile = open('spec%04d.dat'%i,'w') 
    
    # ccd 1    
    myfile = open('cob_P20060817%04d_12cc.txt'% i,'r') 
    temp = myfile.readlines()
    myfile.close()
    outputfile.write(string.join(temp))
    
    # ccd 2
    myfile = open('cob_P20060817%04d_34cc.txt'% i,'r')
    temp = myfile.readlines()
    myfile.close()
    outputfile.write(string.join(temp))
    
    # ccd 3
    myfile = open('cob_P20060817%04d_56cc.txt'% i,'r')
    temp = myfile.readlines()
    myfile.close()
    outputfile.write(string.join(temp))
    
    outputfile.close()