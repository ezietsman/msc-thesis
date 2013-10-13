# removes the first line (1 element) from Starlink Echmop Ascii output files.
# for all .txt files.

import os
import string

files = os.listdir(os.curdir)

for i in files:
    name, ext = os.path.splitext(i)
    if ext == '.txt':
        print i
        myfile = file(i,'r')
        lines = myfile.readlines()
        if len(lines[0]) < 10:
            del lines[0]
        # write output as cob_P20060817*
        newfile = file('c'+i,'w')
        newfile.write(string.join(lines))
