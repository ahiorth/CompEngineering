#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 10:16:07 2019

@author: ah
"""
#%%
import numpy as np
import matplotlib.pyplot as plt

# Integration of a exponetial distribution - "brute force"
def f(z,b):
    return np.array(z*np.exp(-z)/(1-np.exp(-b)))

def ana(b):
    return 1-b*np.exp(-b)/(1-np.exp(-b))

def mc_bf(N,b):
    z = np.random.uniform(0,b,size=N)
    return np.sum(f(z,b))*b/N

def mc_imp(N):
    z = np.random.exponential(size=N)
    return np.sum(z)/N

N=[100,1000,10000,100000,1000000,10000000]
b=10
for n in N:
    result = mc_bf(n,b)
    imp    = mc_imp(n)
    print(n,' ',ana(b)-result,ana(b)-imp, 1/np.sqrt(n))

    
z=np.arange(0,1,.01)
#plt.plot(z,f(z,b))
# %%
