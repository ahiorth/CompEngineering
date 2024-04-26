#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 09:03:17 2019

@author: ah
"""

import numpy as np
import matplotlib.pyplot as plt

#In the implementation below the calculation goes faster 
#when we avoid unnecessary multiplications by h in the loop
def int_trapez(func,lower_limit, upper_limit,N):
    """ calculates the area of func over the domain lower_limit
        to upper limit using N integration points """
    h       = (upper_limit-lower_limit)/N
    area    = func(lower_limit)+func(upper_limit)
    area   *= 0.5
    val     = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        val  += h # midpoint value 
        area += func(val)
    return area*h


def int_romberg(func,lower_limit, upper_limit,tol,show=False):
    """ calculates the area of func over the domain lower_limit
        to upper limit for the given tol, if show=True the triangular
        array of intermediate results are printed """
    Nmax = 100
    R = np.empty([Nmax,Nmax]) # storage buffer
    h = (upper_limit-lower_limit) # step size
    R[0,0]    =.5*(func(lower_limit)+func(upper_limit))*h
    N = 1
    for i in range(1,Nmax):
        h /= 2
        N *= 2
        odd_terms=0
        for k in range (1,N,2): # 1, 3, 5, ... , N-1
            val        = lower_limit + k*h
            odd_terms += func(val)
		# add the odd terms to the previous estimate	
        R[i,0]   = 0.5*R[i-1,0] + h*odd_terms 
        for m in range(0,i): # m = 0, 1, ..., i-1
			# add all higher order terms in h
            R[i,m+1]   = R[i,m] + (R[i,m]-R[i-1,m])/(4**(m+1)-1)                  
		# check tolerance, best guess			
        calc_tol = abs(R[i,i]-R[i-1,i-1])       
        if(calc_tol<tol):
            break  # estimated precision reached 
    if(i == Nmax-1):
        print('Romberg routine did not converge after ',
              Nmax, 'iterations!')
    else:      
        print('Number of intervals = ', N)

    if(show==True):
        elem = [2**idx for idx in range(i+1)]
        print("Steps StepSize Results")
        for idx in range(i+1):
            print(elem[idx],' ',"{:.6f}".format((upper_limit-lower_limit)/2**idx),end = ' ')
            for l in range(idx+1):
                print("{:.6f}".format(R[idx,l]),end = ' ')
            print('')  
    return R[i,i] #return the best estimate

# gaussxw below adopted from
# M. Newman "Compuatiional Physics" - Appendix E
def gaussxw(N):
    # initial approximation to roots of the Legendre polynomials
    a = np.linspace(3,4*N-1,N)/(4*N+2)
    x = np.cos(np.pi*a+1/(8*N*N*np.tan(a)))
    #Find Root using Newtons method
    epsilon = 1e-15
    delta = 1.0
    while delta > epsilon:
        p0 = np.ones(N, float)
        p1 = np.copy(x)
        for k in range(1,N):
            p0,p1=p1,((2*k+1)*x*p1-k*p0)/(k+1)
        dp = (N+1)*(p0-x*p1)/(1-x*x)
        dx=p1/dp
        x-=dx
        delta = np.max(abs(dx))
    # caluclate the weights
    w = 2*(N+1)*(N+1)/(N*N*(1-x*x)*dp*dp)
    
    return x,w

# gaussxwab below adopted from
# M. Newman "Compuatiional Physics" - Appendix E
def gaussxwab(N,a,b):
    x,w=gaussxw(N)
    return 0.5*(b-a)*x+0.5*(b+a),0.5*(b-a)*w

def gauss(f,a,b,N):
    xp,wp = gaussxwab(N,a,b)
    return np.sum(wp*f(xp))

def f(x):
    return x**4-2*x+1

def g(x):
    u=(1-x)
    u*=u
    return np.exp(-x*x/u)/u

w=5
def h(x):
    u=x/(1-x)
    return u*np.exp(-u)*np.cos(w*u)/(1-x)/(1-x)

a=0.
b=1.
N=300
x=np.arange(a,b,0.0001)
plt.plot(x,h(x),label=r'$\omega=$'+str(w))
plt.grid()
plt.xlim(a,b)
plt.legend()
plt.show()

analytical = (1-w*w)/(w**2+1)**2
Area = gauss(h,a,b,N)
eps=max(1e-8,np.abs(Area-analytical))
Area2 = int_romberg(h,a,b*.99999999,eps,show=True)
Area3 = int_trapez(h,a,b*.99999999,N)
print('Numerical value = ', Area)
print('Error  Gauss    = ', (Area-analytical)) 
print('Error  Romberg  = ', (Area2-analytical)) 
print('Error  Trapez   = ', (Area3-analytical)) 

