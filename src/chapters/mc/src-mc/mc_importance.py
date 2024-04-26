#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 10:16:07 2019

@author: ah
"""
import numpy as np
import matplotlib.pyplot as plt

# Integration of a exponetial distribution - "brute force"
def f(z):
    return np.array(z*np.exp(-z/(1-z))/(1-z)**3)

def mc_bf(N):
    z = np.random.uniform(size=N)
    return np.sum(f(z))/N

def mc_imp(N):
    z = np.random.exponential(size=N)
    return np.sum(z)/N

N=[100,1000,10000,100000,1000000]
for n in N:
    result = mc_bf(n)
    imp    = mc_imp(n)
    print(n,' ',1-result,1-imp)

    
z=np.arange(0,1,.01)
plt.plot(z,f(z))
