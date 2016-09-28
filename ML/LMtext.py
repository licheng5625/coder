import spikeMfit
import numpy as np
import scipy.optimize as optimization


T=0
slope0=1.5

def RSErr(T, x, y):
   if (len(y)==0):
       return 0;
   val = 0.0;
   for i in range(0, T):
       val += (x[i] - y[i])**2;
   val=((val/T)**0.5);
   return val;


def residuals(p, x, y):
    re=func(p)
    #print RSErr(T,re,y)
    return re - y

def func(p):#N_max0, betaN0, nb, Sb, bgn0, prate0, pshift0
    global T
    global slope0
    my_beta0=p[1]/p[0]
    (s,t)= spikeMfit.spikeM(T,
    p[0], my_beta0, -slope0,
    p[2], p[3],p[4],
    p[5], p[6], p[7],p[8],p[9], p[10])
    return s

#dat=pylab.loadtxt("data.txt")
def fittoSpikeM(dat):
    dat=np.array(dat)
    lentgh=len(dat)
    for i in range(11-lentgh):
        dat=np.append(dat,1)
    #print((dat))
    global T
    T = len(dat)
    N=sum(dat)

    x0 =  [N*0.8,0.5,11,10,0,1,0.5,10,1,0.5,10]
    p = optimization.leastsq(residuals,x0, args=( dat,dat))[0]
    #return p[7],p[8],p[10]
    return p[5], p[6], p[7],p[8],p[9], p[10]

# import pylab
# dat=pylab.loadtxt("/Users/licheng5625/Downloads/spikeM/data.txt")
#
# print(fittoSpikeM(dat[:42]))
# for p in optimization.leastsq(residuals,x0, args=( dat,dat))[0]:
#     print(p)

# print(p)
# my_beta0=p[1]/p[0]
# spikeMi.showSpike(T,
#     706.943075667, my_beta0, 1.5,
#     11, -2.8167852781,0.216101917915,
#     pfreq0, -2.07062361033, 18.3816179869,24,0.526357564784, 36.1655137142)
#T,N_max0,my_beta0,slope0,nc0,Sc0,bgn0,pfreq0,prate0,pshift0,qrate0,qshift0
# y=np.array([2.1,4,8,19,25])
# x=np.array([1,2,3,4,5])
#
# def residuals2(p, x, y):
#     return func2(p,x) - y
#
# def func2(p,x):#N_max0, betaN0, nb, Sb, bgn0, prate0, pshift0
#     print(p)
#     return  x*x*p[0]+p[1]
# x0 =  np.array([0,0])
# for p in optimization.leastsq(residuals2,x0, args=( x,y))[0]:
#  print(p)