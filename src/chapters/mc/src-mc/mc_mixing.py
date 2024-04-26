#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 09:57:11 2019

@author: ah
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
def mixing_mc(N,dt,t_final,q=1,V=1):
    p=V/q*dt
    Np=[]
    t=[]
    ti=0
    while (ti<t_final):
        n=N
        Np.append(n)
        t.append(ti)
        for i in range(n):
            if(np.random.uniform() < p):
                N -=1
        ti+=dt
    return np.array(t),np.array(Np)

N=1000
t,n=mixing_mc(N,0.01,10)

plt.plot(t,n/N,'-*',label='MC')
plt.plot(t,np.exp(-t),'--',lw=4,label='analytical')
plt.legend()
        
# %%
