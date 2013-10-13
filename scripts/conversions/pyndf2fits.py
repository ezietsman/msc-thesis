# convert all .sdf files to fits format using starlink ndf2fits program

import os

files = os.listdir(os.curdir)

for sdf in files:
    name,ext = os.path.splitext(sdf)
    
    if ext=='.sdf':
        print 'Converting %s to FITS' % name
        command = '/star/bin/convert/ndf2fits %s.sdf %s.fits' % (name,name)
        os.system(command)