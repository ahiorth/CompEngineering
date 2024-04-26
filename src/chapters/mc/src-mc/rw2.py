#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 14:42:00 2019

@author: ah
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
N_=10000

def stdw(N,M):
    """
    N number of steps
    M number of runs
    """
    walks=[]
    for n in N:
        mu_i=[]
        x2_i=[]
        for m in range(M):
#            x = np.array([np.random.randint(-1,1) for i in range (n) ])
            x = 2*np.random.randint(0,2,size=n)-1
            # the path of the walker:
            dx_t=np.cumsum(x)
            #average distance per step
            mu_i.append(dx_t[-1])
            x2_i.append(dx_t[-1]*dx_t[-1])
        mu=np.sum(mu_i)/M
        x2=np.sum(x2_i)/M
        walks.append(x2-mu*mu)
        print('mu=',mu,'x2=', x2)
    return walks

N=[10,20,40,80,160,320,640]
M=1000
w=stdw(N,M)
plt.grid()
plt.plot(N,w,'-*')


# %%
