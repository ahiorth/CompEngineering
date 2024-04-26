#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 12:15:21 2019

@author: ah
"""

import matplotlib.pyplot as plt
import numpy as np

def uniform(a,b):
    return np.array([a,a,b,b]),np.array([0,1/(b-a),1/(b-a),0])

name='acc_rej.txt'
x_,p_=np.loadtxt(name,unpack=True)

norm_ = np.trapz(p_,x_)
p_=p_/norm_
def hiorth_dist(x,xp=x_,fp=p_):
    return np.interp(x, xp, fp)
    

def random_normal():
    trials=0
    l=min(x_)
    u=max(x_)
    c=max(p_)*1.01
    try:
        while(trials < 1000):
            Y = np.random.uniform(l,u)
            GY = c/(u-l)
            ratio = hiorth_dist(Y)/GY
            if (np.random.uniform()<ratio):
                #accept 
                return Y
    except:
        print('Coud not find a random variable')

def randN(N):
    return np.array([random_normal() for _ in range(N)])

N=10000
y=randN(N)
fig, ax1 = plt.subplots()
plt.hist(y, bins='auto', color='#0504aa',alpha=0.7, rwidth=0.85,density=True)
ax2=ax1.twinx() 
ax2.plot(x_,p_,label='hiorth distribution',lw=2,color='r')
plt.legend()
plt.show()
#N=[10,100,1000,10000,1000000]
#for n in N:
#    print(n,' ', ana-mc_bf(n,b),ana-mc_imp(n))
