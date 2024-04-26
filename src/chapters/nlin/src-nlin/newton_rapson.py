#%%
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 09:26:55 2020

@author: 2902412
"""

import numpy as np

def Jacobian(x,f,*args,dx=1e-5,**kwargs):
    N=len(x)
    x0=np.copy(x)
    f0=f(x,*args,**kwargs)
    J=np.zeros(shape=(N,N))
    for j in range(N):
        x[j] = x[j] +  dx
        for i in range(N):   
            J[i][j] = (f(x,*args,**kwargs)[i]-f0[i])/dx
        x[j] = x[j] -  dx
    return J




def newton_rapson(x,f,*args,J=None, jacobian=False, prec=1e-8,MAXIT=10,**kwargs):
    '''Approximate solution of f(x)=0 by Newtons method.
    The derivative of the function is calculated numerically
    f   : f(x)=0.
    J   : Jacobian
    x   : starting point  
    eps : desired precision
    
    Returns x when it is closer than eps to the root, 
    unless MAX_ITERATIONS are not exceeded
    '''
    MAX_ITERATIONS=MAXIT
    x_old = np.copy(x)
    for n in range(MAX_ITERATIONS):
        if not jacobian:
            J=Jacobian(x_old,f,*args,**kwargs)
        print(J)
        z=np.linalg.solve(J,-f(x_old,*args,**kwargs))
        x_new=x_old+z
        if(np.sum(abs(x_new-x_old))<prec):
            print('Found solution:', x_new, 
                  ', after:', n, 'iterations.' )
            return x_new
        x_old=np.copy(x_new)
    print('Max number of iterations: ', MAXIT, ' reached.') 
    print('Try to increase MAXIT or decrease prec')
    print('Returning best guess, value of function is: ', f(x_new,*args,**kwargs))
    return x_new

def gradient_descent(x,f,df, g=.001, prec=1e-8,MAXIT=10000):
    '''Minimize f(x) by gradient descent.
    f   : min(f(x))
    x   : starting point 
    df  : derivative of f(x)
    g   : learning rate
    prec: desired precision
    
    Returns x when it is closer than eps to the root, 
    unless MAXIT are not exceeded
    '''
    x_old = x
    eps=1
    n=0
    while eps >prec and n<MAXIT:
        n=n+1
        x_new = x_old - g*df(x_old)
        eps=np.abs(np.max(x_new-x_old))   
        x_old=np.copy(x_new)
    if eps < prec:
        print('Found solution:', x_new, ', after:', n, 'iterations.' )
    else:
        print('Max number of iterations: ', MAXIT, ' reached.') 
        print('Try to increase MAXIT or decrease prec')
        print('Returning best guess, value of function is: ', f(x_new))
    return x_new

if __name__=='__main__':
    def g(z):
        x=z[0]
        y=z[1]
        return (x*x+y*y-4)**2+(4*x*x-y*y-4)**2
    def dg(z):
        x=z[0]
        y=z[1]
        return np.array([(x*x+y*y-4)*4*x+16*x*(4*x*x-y*y-4),
        (x*x+y*y-4)*4*y-4*y*(4*x*x-y*y-4)])
    def f(z):
        x=z[0]
        y=z[1]
        return np.array([x*x+y*y-4,4*x*x-y*y-4])
    
    def df(z):
        x=z[0]
        y=z[1]
        return np.array([2*x,-2*y])

    def J_ana(z):
        x=z[0]
        y=z[1]
        J=np.zeros(shape=(2,2))
        J[0][0]=2*x
        J[0][1]=4*x
        J[1][0]=2*y
        J[1][1]=-2*y
        return J 
    x0=np.array([.2,.2])
    x=newton_rapson(x0,f,MAXIT=10)
    x=newton_rapson(x0,f,J=J_ana, MAXIT=10)
    print(f(x))
    x=gradient_descent(x0,g,dg,g=.001,MAXIT=1000)
    print(f(x))


# %%
