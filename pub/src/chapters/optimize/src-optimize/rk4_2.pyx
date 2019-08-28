import matplotlib.pyplot as plt
import numpy as np
import time

def fm(c_old,c_in,tau):
    return (c_in-c_old)/tau

def rk4_step(c_old, c_in, tau, h):
    c_next=[]
    for i in range(len(c_old)):
        k1=h*fm(c_old[i],c_in[i],tau[i])
        k2=h*fm(c_old[i]+0.5*k1,c_in[i],tau[i])
        k3=h*fm(c_old[i]+0.5*k2,c_in[i],tau[i])
        k4=h*fm(c_old[i]+    k3,c_in[i],tau[i])
        c_next.append(c_old[i]+(k1+2*k2+2*k3+k4)/6)
    return c_next

def ode_solv(c_into,c_init,t_final,tau,h):
    f=[];t=[]
    c_in  = c_into #freshwater into first tank
    c_old = c_init #seawater present 
    ti=0.
    while(ti <= t_final):
        t.append(ti); f.append(c_old)
        c_new = rk4_step(c_old,c_in,tau,h)     
        c_old = c_new
        # put concentration of tank 0 into tank 1 etc.
        for i,ci in enumerate(c_old[:len(c_old)-1]):
            c_in[i+1]=ci
        ti   += h
    return np.array(t),np.array(f)

h = 1e-5
# initial values
vol=1;q=1;c_into = [0,0,0]; c_init = [1,0,0]
tau=[1,1,1];t_final=10 # end of simulation 
t0=time.time()
t,f=ode_solv(c_into,c_init,t_final,tau,h)
t1 = time.time()
print("Time for execution: ", t1-t0)
