#%%
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

def g(z):
    return 1/np.sqrt(2*np.pi)*np.exp(-z*z/2)

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

    
#z=np.arange(0,1,.01)
#plt.plot(z,f(z))

z=np.arange(-10,10,.01)
plt.plot(z,g(z),label='Normal distribution')
plt.grid()
plt.legend()
plt.savefig('../fig-mc/norm.png', bbox_inches='tight',transparent=True)
plt.close()

z=np.arange(0,10,.01)
plt.plot(z,np.exp(-z),label='Exponential distribution')
plt.grid()
plt.legend()
plt.savefig('../fig-mc/exp.png', bbox_inches='tight',transparent=True)


# %%
