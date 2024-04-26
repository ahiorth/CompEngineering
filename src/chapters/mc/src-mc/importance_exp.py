#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 13:11:50 2019

@author: ah
"""

import matplotlib.pyplot as plt
import numpy as np

def g(z):
    return np.cos(z)*np.exp(-z)

def mc_bf(N,b):
    z = np.random.uniform(0,b,size=N)
    return np.sum(np.cos(z)*np.exp(-z))*b/N

def mc_imp(N):
#    y = np.random.uniform(0,1,size=N)
#    x = -np.log(1-y)
    np.random.seed(1)
    x=np.random.exponential(size=N)
    norm=np.sum(x)/N
    return np.sum(np.cos(x))*norm/(N)


b= 1000

z = np.arange(0,b,0.001)
ana = np.trapz(g(z),z)

N=[10,100,1000,10000,1000000]
for n in N:
    print(n,' ', ana-mc_bf(n,b),ana-mc_imp(n))

plt.plot(z,g(z))
plt.close()
y=np.random.exponential(size=100000)
z=np.random.uniform(0,1,size=100000)
y2 = -np.log(1-z)
plt.hist(x=y, bins='auto', color='#0504aa',alpha=0.7, rwidth=0.85)
plt.show()
plt.hist(x=y2, bins='auto', color='#0504aa',alpha=0.7, rwidth=0.85)
plt.show()         