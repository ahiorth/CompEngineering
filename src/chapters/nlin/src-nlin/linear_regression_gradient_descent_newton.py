#%%
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
x_obs_ = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) 
y_obs_ = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12]) 
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


def Jacobian(x,f,dx=1e-5):
    N=len(x)
    x0=np.copy(x)
    f0=f(x)
    J=np.zeros(shape=(N,N))
    for j in range(N):
        x[j] = x[j] +  dx
        for i in range(N):   
            J[i][j] = (f(x)[i]-f0[i])/dx
        x[j] = x[j] -  dx
    return J




def newton_rapson(x,f,J=None, jacobian=False, prec=1e-8,MAXIT=100):
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
        plot_regression_line(x_old) 
        if not jacobian:
            J_=Jacobian(x_old,f)
        else:
            J_=J(x_old)
        z=np.linalg.solve(J_,-f(x_old))
        x_new=x_old+z
        if(np.sum(abs(x_new-x_old))<prec):
            print('Found solution:', x_new, 
                  ', after:', n, 'iterations.' )
            return x_new
        x_old=np.copy(x_new)
    print('Max number of iterations: ', MAXIT, ' reached.') 
    print('Try to increase MAXIT or decrease prec')
    print('Returning best guess, value of function is: ', f(x_new))
    return x_new


def gradient_descent(f,x,df, g=.001, prec=1e-8,MAXIT=10):
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
    for n in range(MAXIT):
        plot_regression_line(x_old)  
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

def S(b,x=x_obs_,y=y_obs_):
    return np.sum((y-b[0]-b[1]*x)**2)

def dS(b,x=x_obs_,y=y_obs_):
    return np.array([-2*np.sum(y-b[0]-b[1]*x),
                     -2*np.sum((y-b[0]-b[1]*x)*x)])

def J(b,x=x_obs_,y=y_obs_):
    N=len(b)
    J=np.zeros(shape=(N,N))
    xs=np.sum(x)
    J[0][0]=2*len(x)
    J[0][1]=2*xs
    J[1][0]=2*xs
    J[1][1]=2*np.sum(x*x)
    return J
N_=0
print('Gradient ')
b=np.array([0,0])
b=gradient_descent(S,b,dS)

print('Newtons method')
N_=0
b=np.array([-10,1000])
b2=newton_rapson(b,dS,J,jacobian=True)


# %%
