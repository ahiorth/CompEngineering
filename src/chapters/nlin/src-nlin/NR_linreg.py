#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 12:53:55 2019

@author: ah
"""
import numpy as np
import matplotlib.pyplot as plt
 # observations 

N_=0
def plot_regression_line(b,x=x_obs_, y=y_obs_): 
    global N_
    # plotting the actual points as scatter plot 
    plt.scatter(x, y, color = "m", 
               marker = "o", s = 30,label="data") 
  
    # predicted response vector 
    y_pred = b[0] + b[1]*x
  
    # plotting the regression line
    if(len(b)>1):
#        plt.plot(x, y_pred, color = "g", label = "R-squared = {0:.3f}".format(b[2]))
        plt.plot(x, y_pred, color = "g", label = "iteration:" + str(N_) +", (b[0],b[1])= ({0:.3f}".format(b[0]) + ", {0:.3f})".format(b[1]))
        plt.legend()
    else:
        plt.plot(x, y_pred, color = "g")
  
    # putting labels 
    plt.xlabel('x') 
    plt.ylabel('y') 
    plt.grid()
    plt.legend()
#    plt.savefig('../fig-nlin/stdec'+str(N_)+'.png', bbox_inches='tight',transparent=True)
    N_=N_+1  
    # function to show plot 
    plt.show() 

def NewtonRapson(f,x,Jinv, prec=1e-8,MAXIT=500):
    '''Approximate solution of f(x)=0 by Newtons method.
    f    : f(x)=0.
    x    : starting vector
    Jinv : inverse Jacobian
    eps  : desired precision    
    Returns x when it is closer than eps to the root, 
    unless MAX_ITERATIONS are not exceeded
    '''
    MAX_ITERATIONS=MAXIT
    x_old = x
    for n in range(MAX_ITERATIONS):
        x_new = x_old - np.dot(Jinv,f(x_old))
        if(abs(max(x_new-x_old))<prec):
            print('Found solution:', x_new, 
                  ', after:', n, 'iterations.' )
            return x_new
        x_old=x_new
    print('Max number of iterations: ', MAXIT, ' reached.') 
    print('Try to increase MAXIT or decrease prec')
    print('Returning best guess, value of function is: ', f(x_new))
    return x_new
#end

def Jinv(x,x=x_obs_,y=y_obs_):
    j=[]
    j.append(-2*np.sum(y-b[0]-b[1]*x))
    
def gradient_descent(f,x,df, g=.001, prec=1e-8,MAXIT=10000):
    '''Minimize f(x) by gradient descent.
    f   : min(f(x))
    x   : starting point 
    df  : derivative of f(x)
    g   : learning rate
    prec: desired precision
    
    Returns x when it is closer than eps to the root, 
    unless MAX_ITERATIONS are not exceeded
    '''
    MAX_ITERATIONS=MAXIT
    x_old = x
    for n in range(MAX_ITERATIONS):
        x_new = x_old - g*df(x_old)       
        if(abs(np.max(x_new-x_old))<prec):
            print('Found solution:', x_new, 
                  ', after:', n, 'iterations.' )
            return x_new
        x_old=x_new
    print('Max number of iterations: ', MAXIT, ' reached.') 
    print('Try to increase MAXIT or decrease prec')
    print('Returning best guess, value of function is: ', f(x_new))
    return x_new
#end
x_obs_ = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) 
y_obs_ = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12]) 
def S(b,x=x_obs_,y=y_obs_):
    return np.sum((y-b[0]-b[1]*x)**2)

def dS(b,x=x_obs_,y=y_obs_):
    return np.array([-2*np.sum(y-b[0]-b[1]*x),
                     -2*np.sum((y-b[0]-b[1]*x)*x)])

b=np.array([0,0])
b=gradient_descent(S,b,dS)
plot_regression_line(b)

