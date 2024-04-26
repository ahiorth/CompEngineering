#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 12:53:55 2019

@author: ah
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
def bisection(f,a,b,PREC=1e-8,MAXIT=100):
    '''Approximate solution of f(x)=0 on interval [a,b] by bisection.

    f   : f(x)=0.
    a,b : brackets the root f(a)*f(b) has to be negative 
    PREC: desired precision
    
    Returns the midpoint when it is closer than eps to the root, 
    unless MAXIT are not exceeded
    '''
    if f(a)*f(b) > 0:
        print('You need to bracket the root, f(a)*f(b) >= 0')
        return None
    prec=10*PREC
    c = 0.5*(a + b)
    for n in range(MAXIT):
        c_old = c 
        fc = f(c)
        if fc == 0:
            print('Found exact solution ', c, 
                    ' after ', n, 'iterations' )
            return c
        if f(a)*fc < 0:
            b = c
        else:
            a = c
        c = 0.5*(a+b)
        prec=np.abs(c_old-c)
    if n<MAXIT-1:
        print('Found solution ', c,' after ', n, 'iterations' )
        return c
    else:
        print('Max number of iterations: ', MAXIT, ' reached.') 
        print('Try to increase MAXIT')
        print('Returning best guess, value of function is: ', fc)
    return c
#end
def f(x):
    return x**2-np.exp(-x)

def g(x):
    return x-np.exp(1-x*x)

bisection(f,-1000,1000)

x=np.linspace(-100,100,1000)
plt.plot(x,f(x))

# %%
