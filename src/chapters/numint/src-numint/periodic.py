#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 11:03:15 2019

@author: ah
"""

import numpy as np
import matplotlib.pyplot as plt

def f(x,w):
    return x*np.exp(-x)*np.cos(w*x)

x=np.arange(0,20,0.01)
w=40
plt.plot(x,f(x,w),label=r'$\omega$=' +str(w))
plt.grid
plt.show()
