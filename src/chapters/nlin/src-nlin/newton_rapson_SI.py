#%%
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 09:26:55 2020

@author: 2902412
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def Jacobian(x,f,*args,dx=1e-5):
    N=len(x)
    x0=np.copy(x)
    f0=f(x,*args)
    J=np.zeros(shape=(N,N))
    for j in range(N):
        x[j] = x[j] +  dx
        for i in range(N):   
            J[i][j] = (f(x,*args)[i]-f0[i])/dx
        x[j] = x[j] -  dx
    return J




def newton_rapson(x,f,*args,J=None, jacobian=False, prec=1e-8,MAXIT=10):
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
            J=Jacobian(x_old,f,*args)
        z=np.linalg.solve(J,-f(x_old,*args))
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

def gradient_descent(x,f,df,*args, g=.001, prec=1e-8,MAXIT=10000):
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
    print('x_old=',x_old)
    for n in range(MAXIT):
        x_new = x_old - g*df(x_old,*args)     
        if(abs(np.max(x_new-x_old))<prec):
            print('Found solution:', x_new, 
                  ', after:', n, 'iterations.' )
            return x_new
        x_old=np.copy(x_new)
    print('Max number of iterations: ', MAXIT, ' reached.') 
    print('Try to increase MAXIT or decrease prec')
    print('Returning best guess, value of function is: ', f(x_new,*args))
    return x_new

def SI_model(t, p, S0, I0):
    """
    :param t: An array of times.
    :param S0: The initial number of susceptible people.
    :param I0: The initial number of infected people.
    :param beta: The disease transmission rate parameter.
    :param lam: Decline parameter for exponential decline
                of beta (default: 0.0).
    :return: A tuple of arrays holding S(t) and I(t).
    """
    beta=p[0]
    lam=p[1]
    if(len(p))>2:
        S0=p[2]-1
        I0=1
    bt = (beta/lam)*(1.0 - np.exp(-lam*t)) if lam > 0 else beta*t
    I = 1./(1.0 + S0*np.exp(-bt)/I0)
    return I

def least_square(p,t_obs,i_obs,s0,i0):
    l=i_obs-SI_model(t_obs,p,s0,i0)
    return np.sum(l*l)

def dleast_square(p,t_obs,i_obs,s0,i0):
    dp=1.e-5
    df=np.zeros(len(p))
    dd=least_square(p,t_obs,i_obs,s0,i0)
    for i in range(len(p)):
        p[i]=p[i]+dp
        dpi=least_square(p,t_obs,i_obs,s0,i0)
        df[i]=(dpi-dd)/dp
        p[i]=p[i]-dp
    return df


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
    df = pd.read_csv('../data/corona_data.dat', sep='\t')

    def get_corona_data(location, data_file='../data/corona_data.dat'):
        """
        Extracts COVID-19 data for a specific location.

        :param location: The name of the location (case-sensitive).
        :param data_file: Path to file holding the COVID-19 data.
                        It is expected that columns of data are
                        separated by tabs, and that there is a
                        column called "LOCATION" with names of
                        each country, region, etc.
        :return: A pandas DataFrame with COVID-19 data for the
                input location.
        """
        df = pd.read_csv(data_file, sep='\t')
        try:
            df = df[df['LOCATION'] == location]
        except:
            print(f'Could not find data for location {location}...')
            return None
        return df
    x0=np.array([.2,.2])
    x=newton_rapson(x0,f,MAXIT=10)
    x=newton_rapson(x0,f,J=J_ana, MAXIT=10)
    print(f(x))
    x=gradient_descent(x0,g,dg,g=.001,MAXIT=1000)
    print(f(x))
    loc='Hubei'
    df = get_corona_data(loc)
    N = df['CONFIRMED'].iloc[-1]
    t_obs = df['ELAPSED_TIME_SINCE_OUTBREAK'].to_numpy()
    i_obs = df['CONFIRMED'].to_numpy()
    i_obs = i_obs/np.max(i_obs)
    p=np.array([2.,0.2])
    N=50e6
    plt.plot(t_obs,i_obs,'*')
    plt.plot(SI_model(t_obs,p,N-1,1),c='k',label='first guess')

    print('dll',dleast_square(p,t_obs,i_obs,s0=N-1,i0=1))
    p=gradient_descent(p,least_square,dleast_square,t_obs[t_obs<50],i_obs[t_obs<50],N-1,1,g=0.0001,prec=1e-8,MAXIT=10000)
    p2=newton_rapson(p,dleast_square, t_obs[t_obs<50],i_obs[t_obs<50],N-1,1, MAXIT=10,prec=1e-10)
    plt.plot(t_obs,i_obs,'o')
    plt.plot(SI_model(t_obs,p,N-1,1),'--',label='last guess')
    plt.plot(SI_model(t_obs,p2,N-1,1),'-',label='last guess - Newton')
    plt.legend()



# %%
