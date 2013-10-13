#! /usr/bin/python
# added useless line here


from pylab import *
from astronomy import *
from liboc import *
from os import system

system('ls -l')
t,f = read_file_interactive(raw_input("Enter filename : "))
N = int(raw_input("How many cycles? : "))
freq = float(raw_input("What frequency ? : "))
t = t - int(t[0])

choice = raw_input("Take slope into account? y/[n] : ")
if choice == 'y' or choice == 'Y':
    ocd = oc(f,t,freq,N,slope=1)
else:
    ocd = oc(f,t,freq,N,slope=0)


# plot onscreen
subplot(311)

plot(t,f,'.')
ylabel("Magnitude")
xlim(min(ocd[2]) - 0.01 , max(ocd[2]) + 0.01)
ylim(max(f) + 0.25 , min(f)-0.25)

		
subplot(312)
errorbar(ocd[2],ocd[0],ocd[3],fmt='r.')
ylabel("Amplitude")
xlim(min(ocd[2]) - 0.01 , max(ocd[2]) + 0.01)

subplot(313)
errorbar(ocd[2],ocd[1],ocd[4],fmt='g.')
xlim(min(ocd[2]),max(ocd[2]))
ylabel("O-C (phase)")
xlabel("Time")
xlim(min(ocd[2]) - 0.01, max(ocd[2]) + 0.01)
ylim(-0.75,0.75)
show()

		
# Make the hardcopy
#subplot(311)
#plot(t,f,'.')
#ylabel("Magnitude")
#lim(min(ocd[2]) - 0.01 , max(ocd[2]) + 0.01)
#ylim(max(f) + 0.25 , min(f)-0.25)

		
#subplot(312)
subplot(211)
errorbar(ocd[2],ocd[0],ocd[3],fmt='r.')
ylabel("Amplitude")
xlim(min(ocd[2]) - 0.01 , max(ocd[2]) + 0.01)
vlines(0.32,-1,1,'k-')
vlines(0.352,-1,1,'k-')
vlines(0.474,-1,1,'k-')
vlines(0.503,-1,1,'k-')

#subplot(313)
subplot(212)
errorbar(ocd[2],ocd[1],ocd[4],fmt='g.')
xlim(min(ocd[2]),max(ocd[2]))
ylabel("O-C (phase)")
xlabel("Time")
xlim(min(ocd[2]) - 0.01, max(ocd[2]) + 0.01)
ylim(-0.75,0.75)
vlines(0.32,-1,1,'k-')
vlines(0.352,-1,1,'k-')
vlines(0.474,-1,1,'k-')
vlines(0.503,-1,1,'k-')
		
name = raw_input("Enter output image name [image.png] : ")
if len(name) == 0:
	savefig("image.png")
else:
	savefig(name)
	
	
