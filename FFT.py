tau = 6.283185307179586476925286766559
from math import sin,cos

def FFT(mylist, inverse=False):
    N = len(mylist)
    if N==1: return mylist[:]
    Xeven,Xodd = (FFT(mylist[i::2]) for i in range(2))
    rtrn = [None for i in range(N)]

    theta=(+1 if inverse else -1)*tau/N
    unit=cos(theta)+1j*sin(theta)
    coef = 1.0
    for k in range(N):
        rtrn[k] = Xeven[k%(N//2)] + coef*Xodd[k%(N//2)]
        coef *= unit
    return rtrn

def autocorrelations(mylist):
    return FFT([x*x for x in FFT(mylist)], inverse=True)

def periodicity(mylist): #not normalized
    return max(autocorrelations(mylist))
