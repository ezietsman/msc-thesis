# program to read single star part of UCT CCD file and rewrite the file without the Julian date integers

from astronomy import read_file
import os

os.system("clear && ls -l")
choice = raw_input("Enter filename : ")

x,y = read_file(choice)

myint = int(x[0])

choice = raw_input("Enter output filename : ")
myfile = file(choice,'w')

for i in range(len(x)):
    s = str(x[i]-myint) + " " + str(y[i]) + "\n"
    myfile.write(s)
    
print myint