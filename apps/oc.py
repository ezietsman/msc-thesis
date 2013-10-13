#! /usr/bin/python


from pylab import *
import pylab as pl
from astronomy import *
from liboc import *
from os import system
import string
#t = arange(0.0,0.12,0.0001)

#f = 0.5*sin(2*pi*1500*t)

#for i in range(len(t)):
	#f[i] = f[i] + (0.4*rand() - 0.2) 
system('ls -l')
#t,f = utils.read_file(raw_input("Enter filename : "))
#t,z = utils.read_file(raw_input("Enter filename : "))
filename = raw_input("Enter filename : ")
X = pl.load(filename)
t = X[:,0]
f = X[:,1]
z = X[:,2]

N = int(raw_input("How many cycles? : "))
freq = float(raw_input("What period [s] ? : "))
freq = 86400.0/freq

t = t - int(t[0])

# look at specific times only

#low = t < 0.36
#high = t > 0.

#t = t[low*high]
#f = f[low*high]
#z = z[low*high]


ocd = oc(f,t,freq,N)

#x = fitwave(f,t,1500.0)

#plot(t,f,'x')
#plot(t,x[0]*sin(2*pi*1500.0*t + x[1]),'r-')
#show()

		
		  
                  
figure(figsize=(9,6))
subplots_adjust(left=0.14,hspace=0.001)
# plot onscreen
ax1 = subplot(311)
plot(t,f+z,'.')
xlabel("Time")
ylabel("Magnitude")
xlim(min(ocd[2]) - 0.01 , max(ocd[2]) + 0.01)
yl = ylim()
yt = yticks()
ax1.set_yticks(yt[0][1:-1])
#ylim(yl[1],yl[0])
#xlim(0.54,0.58) # Eclipse 2 run S7655


ax2 = subplot(312)
grid()
#title("O-C Diagram")
errorbar(ocd[2][:-2],ocd[0][:-2],ocd[3][:-2],fmt='ro')
ylabel("Amplitude")
#xlabel("Time")
xlim(min(ocd[2]) - 0.01 , max(ocd[2]) + 0.01)
#xlim(0.54,0.58) # Eclipse 2 run S7655
yl = ylim()
ylim(0,yl[1])
yt = yticks()
ax2.set_yticks(yt[0][1:-1])



subplot(313)
grid()
errorbar(ocd[2][:-2],ocd[1][:-2],ocd[4][:-2],fmt='go')
#errorbar(ocd[2],ocd[1],ocd[4],fmt='g-')
xlim(min(ocd[2]),max(ocd[2]))
ylabel("Phase")
xlabel("Time")
xlim(min(ocd[2]) - 0.01, max(ocd[2]) + 0.01)
#xlim(0.54,0.58) # Eclipse 2 run S7655
#ylim(0,1)

#ylim(-1.0,1.0)
yt = yticks()
yticks(yt[0][1:-1])

xticks = ax1.get_xticklabels() + ax2.get_xticklabels()
setp(xticks, visible=False)

show()

		
## Make the hardcopy
#subplot(311)
#plot(t,f,'.')
#xlabel("Time")
#ylabel("Magnitude")
#xlim(min(ocd[2]) - 0.01 , max(ocd[2]) + 0.01)
#ylim(min(f) + 0.25 , max(f)-0.25)

		
#subplot(312)
#grid()
##title("O-C Diagram")
#errorbar(ocd[2],ocd[0],ocd[3],fmt='ro')
#ylabel("Amplitude")
#xlabel("Time")
#xlim(min(ocd[2]) - 0.01 , max(ocd[2]) + 0.01)

#subplot(313)
#grid()
#errorbar(ocd[2],ocd[1],ocd[4],fmt='go')
#xlim(min(ocd[2]),max(ocd[2]))
#ylabel("Phase")
#xlabel("Time")
#xlim(min(ocd[2]) - 0.01, max(ocd[2]) + 0.01)
##ylim(0,1)
		
#name = raw_input("Enter output image name [image.png] : ")
#if len(name) == 0:
	#savefig("image.png")
#else:
	#savefig(name)
	

print 'saving data to oc_out.dat'

save('oc_out.dat',array(ocd).transpose())


