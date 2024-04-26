#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 14:42:00 2019

@author: ah
"""
#%%
import numpy as np
import random
import matplotlib.pyplot as plt
N_=10000
#x = [random.randint(-1,1) for i in range (N_) ]
x = 2*np.random.randint(0,2,size=N_)-1
# how far does the walker travel?
dx = np.sum(x)

# the path of the walker:
dx_t=np.cumsum(x)
plt.xlabel('No steps')
plt.ylabel('Distance')
plt.grid()

plt.plot(np.linspace(1,N_,N_),dx_t)
#plt.close()
#%%
#2 dimensions:
y = 2*np.random.randint(0,2,size=N_)-1
#y= [random.randint(-1,1) for i in range (N_) ]
dy_t=np.cumsum(y)
plt.grid()
plt.plot(dx_t,dy_t)



# %%
