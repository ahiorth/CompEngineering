#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 13:28:56 2019

@author: ah
"""
import random as r
import numpy as np

def pi_mc(N):
    """
    calculates pi using Monte Carlo Integration
    N: number of sampling points
    """
    n_pond=0
    for i in range(N):
        x = r.uniform(-1.,1.)
        y = r.uniform(-1,1.)
        if (x**2 + y**2 <= 1):
            n_pond +=1
    return n_pond/N*4

def pi_mcII(N):
    """
    calculates pi using Monte Carlo Integration
    N: number of sampling points
    """
    x = 2*np.random.rand(N)-1
    y = 2*np.random.rand(N)-1
    n_pond = x*x + y*y <=1
    return np.sum(n_pond)/N*4

N=[100,1000,10000,100000]
NN=100
for n in N:
    print(pi_mc(n), 'error ', pi_mc(n)-np.pi)
    print(pi_mcII(n), 'error II', pi_mcII(n)-np.pi)
est=np.zeros(len(N))

for i,n in enumerate(N):
    ei=0.
    for j in range(NN):
        ei+=pi_mc(n)
    est[i]=ei/NN
    
for n in range(len(N)):
    print('Estimate of pi= ', est[n], 'error: = ',np.pi-est[n])
            
    