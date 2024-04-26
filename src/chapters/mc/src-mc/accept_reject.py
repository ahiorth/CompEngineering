#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 12:15:21 2019

@author: ah
"""
#%%

import matplotlib.pyplot as plt
import numpy as np

def uniform(a,b):
    return np.array([a,a,b,b]),np.array([0,1/(b-a),1/(b-a),0])

def normal(z):
    return np.exp(-z*z/2)/np.sqrt(2*np.pi)

def g(z):
    return np.array(np.cos(z)*normal(z))

def mc_bf(N,b):
    z=np.random.uniform(-b,b,size=N)
    return np.sum(g(z))*2*b/N

def mc_imp(N):
    z=np.random.normal(size=N)
    return np.sum(np.cos(z))/N


def random_normal():
    trials=0
    l=-5
    u=-l
    c=4.5
    try:
        while(trials < 1000):
            Y = np.random.uniform(l,u)
            GY = c/(u-l)
            ratio = normal(Y)/GY
            if (np.random.uniform()<ratio):
                #accept 
                return Y
    except:
        print('Coud not find a random variable')

def randN(N):
    return np.array([random_normal() for _ in range(N)])

N=10000
y=randN(N)

plt.hist(y, bins='auto', color='#0504aa',alpha=0.7, rwidth=0.85)
g = np.random.normal(size=N)
plt.hist(g, bins='auto', color='red',alpha=0.7, rwidth=0.85)

z = np.arange(-10,10,0.01)
#plt.plot(z,normal(z))
#plt.ylim(0,1)
plt.show()
#N=[10,100,1000,10000,1000000]
#for n in N:
#    print(n,' ', ana-mc_bf(n,b),ana-mc_imp(n))



plt.show()
l=-5
u=-l
c=4.5
x,y=uniform(l,u)
plt.plot(z,normal(z))
plt.plot(x,c*y)
plt.show()

# %%
