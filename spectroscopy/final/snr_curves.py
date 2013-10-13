# run splot using pyraf script to catch output
# script uses splot to create signal-to-noise curves for the run
import os
import pylab as pl
import pyfits as pf
import astronomy as ast
import pp


cd = os.getcwd()
os.chdir('/home/ewald/')
from pyraf import iraf
os.chdir(cd)


iraf.onedspec()

# create list of files containing the fits filenames
os.system('ls ../extracted/ec*.fits > speclist')

try:
    os.remove('splot.log')
except:
    pass

speclist = file('speclist','r')
output = file('snr_curves.dat','w')
output.write('# HJD Ha red yellow Hb He2 blue\n') 
HJD = []


#define regions to calculate snr

regions = {}
regions['Ha'] = [6558,6573]
regions['red'] = [6350,6450]
regions['yellow'] = [5474,5574]
regions['Hb'] = [4852,4876]
regions['He2'] = [4679,4695]
regions['blue'] = [4450,4550]


def read_out(s):
    # reads output from splot's snr command and returns snr as float
    snr = s[0].split()[-1]
    return snr

for spec in speclist:
    # read data and header
    print '\n %s \n' % spec
    data = pf.getdata(spec)
    head = pf.getheader(spec)
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    x = start + pl.arange(0,length)*step
    HJD.append(float(head['HJD']))

    SNR = []
    # calculate snr using splot for every region. 
    for reg in enumerate(['Ha','red','yellow','Hb','He2','blue']):
        # write to cursor file
        #os.remove('cursor')
        cfile = file('cursor','w')
        s = "%s 0.001 1 m\n%s 0.001 1 m\n" % (regions[reg[1]][0],regions[reg[1]][1])
        cfile.write(s)
        cfile.close() # do this otherwise get freaky bugs
        out = iraf.splot(images=spec.strip(),cursor='cursor',Stdout=1)
        SNR.append(read_out(out))
        print reg, SNR[0]
    
    # Now print output 
    s = [' '.join('%s'%i for i in SNR)]
    #print s
    output.write(str(head['HJD'])+' ' + s[0]+'\n')
      
    
output.close()
# run bplot
#iraf.bplot(images='@speclist',cursor='cursor')

#HJDfile = open('HJD.dat','w')
#for d in HJD:
    #HJDfile.write('%s\n'%d)
#HJDfile.close()
    
    
# get the output. Tune this grep command for the wavelength
#os.system('grep 65 splot.log > rv.dat')


