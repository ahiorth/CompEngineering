#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 12:15:21 2019

@author: ah
"""
#%%
import matplotlib.pyplot as plt
import numpy as np


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

b=10000

ana2 = 1/(np.exp(1)**0.5)
if(b<10):
    z = np.arange(-b,b,0.01)
    ana = np.trapz(g(z),z)
else:
    ana=ana2

N=[10,100,1000,10000,1000000]
for n in N:
    print(n,' ', ana-mc_bf(n,b),ana-mc_imp(n))
z = np.arange(-5,5,0.01)

plt.show()
plt.plot(z,g(z),label=r'$\cos(x)\, e^{-x^2/2}$')
plt.plot(z,normal(z),label=r'$\frac{1}{\sqrt{2\pi}}\, e^{-x^2/2}$')
plt.legend()
plt.grid()
plt.savefig('../fig-mc/gauss_imp.png', bbox_inches='tight'
            ,transparent=True)
plt.show()

# %%
