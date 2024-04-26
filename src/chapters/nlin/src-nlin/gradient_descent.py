#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 12:53:55 2019

@author: ah
"""
import numpy as np

def gradient_descent(f,x, g=.1, prec=1e-8,MAXIT=50):
    '''Minimize f(x)=0 by gradient descent.
    The derivative of the function is calculated numerically
    f   : f(x)=0.
    x   : starting point  
    eps : desired precision
    
    Returns x when it is closer than eps to the root, 
    unless MAXIT are not exceeded
    '''
    x_old = x
    h     = 1e-4
    for n in range(MAXIT):
        print(x_old, f(x_old))
        x_new = x_old - g*0.5*(f(x_old+h)-f(x_old-h))/h
        
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
    return (x**2 - np.exp(-x))**2

def g(x):
    return x-np.exp(1-x*x)

gradient_descent(f,1)
