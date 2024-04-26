#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 12:53:55 2019

@author: ah
"""
import numpy as np

def newton(f,x, prec=1e-8,MAXIT=500):
    '''Approximate solution of f(x)=0 by Newtons method.
    The derivative of the function is calculated numerically
    f   : f(x)=0.
    x   : starting point  
    eps : desired precision
    
    Returns x when it is closer than eps to the root, 
    unless MAX_ITERATIONS are not exceeded
    '''
    MAX_ITERATIONS=MAXIT
    x_old = x
    h     = 1e-4
    for n in range(MAX_ITERATIONS):
        x_new = x_old - 2*h*f(x_old)/(f(x_old+h)-f(x_old-h))
        if(abs(x_new-x_old)<prec):
            print('Found solution:', x_new, 
                  ', after:', n, 'iterations.' )
            return x_new
        x_old=x_new
    print('Max number of iterations: ', MAXIT, ' reached.') 
    print('Try to increase MAXIT or decrease prec')
    print('Returning best guess, value of function is: ', f(x_new))
    return x_new
#end
    
def df(x):
    2*x+np.exp(-x)
def f(x):
    return x**2-np.exp(-x)

def g(x):
    return x-np.exp(1-x*x)

newton(f,-100)
#newton(f,1)
#newton(g,0)