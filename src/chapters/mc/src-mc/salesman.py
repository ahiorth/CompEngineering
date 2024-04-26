#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 17:26:01 2019

@author: ah
"""
import numpy as np
import matplotlib.pyplot as plt
N_=30
R_=0.02

Tmax_=10
Tmin_=1e-3
tau_=1e4
# Define starting route
r_=np.empty([N_+1,2],dtype=float)
np.random.seed(2)
for i in range(N_):
    r_[i,0]=np.random.uniform()
    r_[i,1]=np.random.uniform()
r_[N_]=r_[0]

#form Wikipedia
r_true_=np.loadtxt('trav_sal.txt')
r_=np.loadtxt('trav_sal.txt')
N_=len(r_[:,0])
#rescale
r_true_=r_true_/1800
r_=r_/1800
np.random.shuffle(r_)
r_=np.append(r_,[r_[0]],axis=0)
r_true_=np.append(r_true_,[r_true_[0]],axis=0)

def mag(x):
    return np.sqrt(np.sum(x*x))

def distance(r=r_,N=N_):
    s=0.0
    for i in range(N):
        s += mag(r[i+1]-r[i])
    return s

def plot_route(t,r=r_,s=60,N=N_,route=True):
    plt.scatter(r[0,0],r[0,1],s=s*4,color='r')
    plt.scatter(r[1:,0],r[1:,1],s=s,color='k')
    if route:
        plt.plot(r[:,0],r[:,1],'-')
        for i in range(N):
            di=np.sqrt(np.sum((r[i+1]-r[i])*(r[i+1]-r[i])))
            xi=0.5*(r[i,0]+r[i+1,0])
            #        yi=0.5*(r[i,1]+r[i+1,1])
            yi=(r[i+1,1]-r[i,1])/(r[i+1,0]-r[i,0])*(xi-r[i,0])+r[i,1]
            xf=xi+0.05*di
            yf=(r[i+1,1]-r[i,1])/(r[i+1,0]-r[i,0])*(xf-r[i,0])+r[i,1]
            dx=xf-xi
            dy=yf-yi
            if(r[i,0]>r[i+1,0]):
                dx=-dx
                dy=-dy
                plt.arrow(xi,yi,dx,dy,length_includes_head=True,head_width=0.04, head_length=0.02, fc='k', ec='k')
#    print(xi,yi,xf,yf)
#    plt.arrow(xi,yi,xf,yf,shape='full',lw=0,length_includes_head=True, head_width=.01)
    plt.title('Travel Route at time ' + str(t))
    plt.show()
    plt.close()


def trav_salesman():
    # Main Loop
    t_=0
    T_=Tmax_
    plot_route(t_)
    D_=distance()
    no_it_=0
    while T_>Tmin_:
        no_it_ +=1
        t_+=1
        T_=Tmax_*np.exp(-t_/tau_)
        
        if no_it_ %1000==0:
            print('Distance=', D_, 'Cooling Temp:', T_,Tmin_)
            plot_route(t_)
    
        # Choose two cities to swap and make sure they are distinct
        i,j=np.random.randint(1,N_),np.random.randint(1,N_)
        while i==j:
            i,j=np.random.randint(1,N_),np.random.randint(1,N_)
        
        # swap and calculate change in distance
        oldD_=D_
        r_[i,0],r_[j,0]=r_[j,0],r_[i,0]
        r_[i,1],r_[j,1]=r_[j,1],r_[i,1]
        D_=distance()
        deltaD_=D_-oldD_
        #if Move is rejected swap back
        if(np.random.uniform()>=np.exp(-deltaD_/T_)):
            r_[i,0],r_[j,0]=r_[j,0],r_[i,0]
            r_[i,1],r_[j,1]=r_[j,1],r_[i,1]
            D_=oldD_
    
plot_route(0,route=False)    
trav_salesman()
trav_salesman()
plot_route(0,r=r_true_)
print('True Distance', distance(r_true_))
