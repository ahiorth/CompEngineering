#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 08:57:51 2019

@author: ah
"""
import numpy as np

def rk4_step(rhs,t,c,h,*args):
    """
    Integrates from time t to t+h using RK4
    rhs = right hand side
    t = current time
    h = step size
    c = solution vector
    """
    k1=h*rhs(c,t,*args)
    k2=h*rhs(c+0.5*k1,t+0.5*h,*args)
    k3=h*rhs(c+0.5*k2,t+0.5*h,*args)
    k4=h*rhs(c+k3,t+h,*args)
    return c+(k1+2*k2+2*k3+k4)/6

def ode_solv(rhs,ti,c,t_final,h,*args):
    """
    solves a set of ODE with known initial conditions
    from time ti to t_final
    rhs= right hand side vector
    ti = start time
    c = initial conditions at time ti
    t_final = end time
    h = step size
    """
    f=[];t=[]
    c_old = c      #seawater present 
    while(ti <= t_final):
        t.append(ti); f.append(c_old)
        c_new = rk4_step(rhs,ti,c_old,h,*args)     
        c_old = c_new
        ti   += h
    return np.array(t),np.array(f)