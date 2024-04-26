#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 12:04:18 2019

@author: ah
"""

import numpy as np


def g(x):
    return np.exp(1-x*x)
def h(x):
    return np.exp(-x/2)

def I(x):
    return np.exp(1-x*x)

def J(x):
    return np.sqrt(1-np.log(x))

def iterative(x,g,prec=1e-8):
    MAX_ITER=1000
    eps = 1
    n=0
    while eps>prec and n < MAX_ITER:
        x_next = g(x)
        eps = np.abs(x-x_next)
        x = x_next
        n += 1
    print('The solution is: ', x, 'Number of iterations: ', n)
    return x

iterative(0.99,g,1e-8)
iterative(2.5,J,1e-8)
#iterative(.999,I,1e-8)
#iterative(.9999999,I,1e-8)

