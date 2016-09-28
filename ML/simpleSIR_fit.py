import scipy.optimize as optimization

import scipy.integrate as spi
import numpy as np
import pylab as pl

dat=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 16, 23, 85, 116, 134, 158, 181, 214, 227]


def diff_eqs(INP,t,para):
    '''The main set of equations'''
    Y=np.zeros((2))
    V = INP
    beta=para[0]
    gamma=para[1]
    Y[0] = - beta * V[0] * V[1] + gamma * V[1]
    Y[1] = beta * V[0] * V[1] - gamma * V[1]
    return Y   # For odeint

def getdata(p,timeEND):
    t_start = 1.0; t_end = timeEND; t_inc = 1.0
    t_range = np.arange(t_start, t_end+t_inc, t_inc)
    INPUT=p[:2]
    RES = spi.odeint(diff_eqs,INPUT,t_range,args=(p[2:],))
    #print(RES)
    return RES


def residuals(p, x, y,timeEND):
    #print RSErr(T,re,y)
    RES=getdata(p,49)
    return RES[:timeEND,1] - y


def fitSIS(dat):
    lentgh=len(dat)
    dat=np.array(dat)

    if lentgh==0:
        for i in range(4-lentgh):
            dat=np.append(dat,0)
    else:
        dat=dat/dat[-1]
        if lentgh<4:
            lastdata=dat[-1]
            for i in range(4-lentgh):
                dat=np.append(dat,lastdata)
    N=dat[-1]
    N0=dat[0]
    timeEND=len(dat)
    x0 =  [N,N0,0,0]
    p = optimization.leastsq(residuals,x0, args=( dat,dat,timeEND))[0]
    return p

dat=np.array(dat)

p=fitSIS(dat)
# #p=[1-0.001,0.001,1.4247,0.14286]
print(p[2:])
RES=getdata(p,48)
print(RES[:,1])
#Ploting
pl.subplot(211)
pl.plot(RES[:,0], '-g', label='Susceptibles')
pl.title('Program_2_5.py')
pl.xlabel('Time')
pl.ylabel('Susceptibles')
pl.subplot(212)
pl.plot(RES[:,1], '-r', label='Infectious')
pl.plot( dat/dat[-1], '-b', label='real Infectious')

pl.xlabel('Time')
pl.ylabel('Infectious')
pl.show()
