import scipy.integrate as spi
import numpy as np
import pylab as pl

beta=1.4247
gamma=0.14286
p=0.1
l=0.1
b=0.1
e=0.1
I0=0.01
ND=48
TS=1.0
INPUT = (1.0-I0, I0,0,0)

def diff_eqs(INP,t):
	'''The main set of equations'''
	Y=np.zeros((4))
	S=INP[0]
	E=INP[1]
	I=INP[2]
	Z=INP[2]
	N=S+I+E+Z
	Y[0] = - beta * S * I/N -b * S * Z/N
	Y[1] = (1-p)*beta * S * I/N +(1-l)*b * S * Z/N-p*E*I/N-e*E
	Y[2] = - p*beta * S * I/N +p * E * I/N+e*E
	Y[3] = l*b** S * Z/N
	return Y   # For odeint



# t_start = 0.0; t_end = ND; t_inc = TS
# t_range = np.arange(t_start, t_end+t_inc, t_inc)
# RES = spi.odeint(diff_eqs,INPUT,t_range)
#
# print (RES)

#Ploting
# pl.subplot(211)
# pl.plot(RES[:,0], '-g', label='Susceptibles')
# pl.title('Program_2_5.py')
# pl.xlabel('Time')
# pl.ylabel('Susceptibles')
# pl.subplot(212)
# pl.plot(RES[:,2], '-r', label='Infectious')
# pl.xlabel('Time')
# pl.ylabel('Infectious')
# pl.show()
print()