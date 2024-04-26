#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 09:12:37 2019

@author: ah
"""
import numpy as np

X = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) 
Y = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12]) 

# Building the model
m = 0
c = 0

L = 0.5  # The learning Rate
epochs = 1000  # The number of iterations to perform gradient descent

n = float(len(X)) # Number of elements in X

# Performing Gradient Descent 
for i in range(epochs): 
    Y_pred = m*X + c  # The current predicted value of Y
    D_m = (-2/n) * sum(X * (Y - Y_pred))  # Derivative wrt m
    D_c = (-2/n) * sum(Y - Y_pred)  # Derivative wrt c
    m = m - L * D_m  # Update m
    c = c - L * D_c  # Update c
    
print (m, c)
# %%
