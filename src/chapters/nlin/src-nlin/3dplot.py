#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 15:38:13 2019

@author: ah
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


x_obs_ = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) 
y_obs_ = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12])

def S(b0,b1,xo=x_obs_,yo=y_obs_):
    x = []
    y = []
    z = []
    for i in range(len(b0)):
        xi=[]
        yi=[]
        zi=[]
        for j in range(len(b1)):
            xi.append(b0[i])
            yi.append(b1[j])
            zi.append(np.sum((yo-b0[i]-b1[j]*xo)**2))
        x.append(xi)
        y.append(yi)
        z.append(zi)
    return np.array(x),np.array(y),np.array(z)

b0=np.arange(-2,2,0.1)
b1=np.arange(-2,2,0.1)

X,Y,Z=S(b0,b1)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grab some test data.
#X, Y, Z = axes3d.get_test_data(0.05)

# Plot a basic wireframe.
#ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
#ax.plot_wireframe(x, y, z, rstride=10, cstride=10)
#ax.plot_surface(x, y, z)
ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,linewidth=0, antialiased=False)
# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

plt.show()
