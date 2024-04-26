#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 12:32:23 2019

@author: ah
"""
import numpy as np
import matplotlib.pyplot as plt
import rk42 as od

# Our problem
    
def RHS(c,t,c_in,tau):
    rhs=[]
    rhs.append(c_in-c[0])
    rhs.append(c[0]-c[1])
    rhs.append(c[1]-c[2])
    return np.array(rhs)/tau

# initial values
yn=[1,0,0] # seawater in the first tank
t_start=0
t_final=10
h=0.01
c_init=yn
t=np.arange(t_start,t_final+2*h,h)

f=od.ode_solv(yn,t_start,t_final,RHS,h,0,1)
        
f_an = []
f_an.append(c_init[0]*np.exp(-t))
f_an.append(c_init[0]*t*np.exp(-t))
f_an.append(c_init[0]*0.5*t*t*np.exp(-t))

symb = ['-p','-v','-*','-s']
fig = plt.figure(dpi=150)
for i in range(0,len(c_init)):
    legi = '$\hat{C}_'+str(i)+'(\\tau)$'
    plt.plot(t, f[:,i], '-', label=legi,lw=4)
    plt.plot(t, f_an[i], '--', color='k')
plt.plot(0,0 , '--', color='k',label='analytical')
plt.legend(loc='upper right', ncol=1)
#plt.ylim([0,50])
plt.grid()
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    