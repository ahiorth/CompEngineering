#%%
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.numeric import ComplexWarning

V=2
q=1
tau=V/q
tf=4
c0=10000
def analytical(t,c0=c0,tau=tau):
    return c0*np.exp(-t/tau)
def f(c,t):
    return -1./tau*c

def euler_step(c,t,dt):
    return dt*f(c,t)
def rk2_step(c,t,dt):
    k1=dt*f(c,t)
    a=c+0.5*k1
    k2=dt*f(c+0.5*k1,t+dt*0.5)
    return k2
def euler(c0,dt,tf=tf):
    c=[]
    t=[]
    ti=0.
    c.append(c0)
    t.append(ti)
    while(ti<=tf):
        c.append(c[-1]+euler_step(c[-1],ti,dt))
        ti=ti+dt
        t.append(ti)
    return np.array(t),np.array(c)

def rk2(c0,dt,tf=tf):
    c=[]
    t=[]
    ti=0.
    c.append(c0)
    t.append(ti)
    while(ti<=tf):
        c.append(c[-1]+rk2_step(c[-1],ti,dt))
        ti=ti+dt
        t.append(ti)
    return np.array(t),np.array(c)

def rk4_step(c,t,dt):
    k1=dt*f(c,t)
    k2=dt*f(c+0.5*k1,t+0.5*dt)
    k3=dt*f(c+0.5*k2,t+0.5*dt)
    k4=dt*f(c+k3,t+dt)
    return (k1+2*k2+2*k3+k4)/6

def rk4(c0,dt,tf=tf):
    c=[]
    t=[]
    ti=0.
    c.append(c0)
    t.append(ti)
    while(ti<=tf):
        c.append(c[-1]+rk4_step(c[-1],ti,dt))
        ti=ti+dt
        t.append(ti)
    return np.array(t),np.array(c)

def euler_adpative(c0,EPS=1e-3,tf=tf):
    c=[]
    t=[]
    ti=0.
    c.append(c0)
    t.append(ti)
    dt=1e-6 # start with very small step 
    while(ti<=tf):
        eps=1
        while(eps>EPS): # find correct dt
            DT=dt
            c_new = c[-1] + euler_step(c[-1],ti,dt) #one large step
            c1    = c[-1] + euler_step(c[-1],ti,dt*0.5) # and two small steps
            c2    = c1 + euler_step(c1,ti,dt*0.5)
            eps   = np.abs(c2-c_new)
            dt = dt*np.sqrt(EPS/eps) # could also multiply with 0.9 to be conservative
        c.append(2*c2-c_new)
        ti=ti+DT
        t.append(ti)
    return np.array(t),np.array(c)

def rk_adpative(c0,rel_tol=1e-5,abs_tol=1e-5,tf=tf,p=4):
    c=[]
    t=[]
    ti=0.
    c.append(c0)
    t.append(ti)
    dt=1e-2 # start with very small step 
    while(ti<=tf):
        EPS=np.abs(c[-1])*rel_tol+abs_tol
        eps=1
        while(eps>EPS): # find correct dt
            DT=dt
            c_new = c[-1] + rk4_step(c[-1],ti,dt) #one large step
            c1    = c[-1] + rk4_step(c[-1],ti,dt*0.5) # and two small steps
            c2    = c1 + rk4_step(c1,ti,dt*0.5)
            eps   = np.abs(c2-c_new)/(2**p-1)
            dt = 0.9*dt*(EPS/eps)**(1/p) # could also multiply with 0.9 to be conservative
        c.append((2**p*c2-c_new)/(2**p-1))
        #c.append(c2)
        ti=ti+DT
        t.append(ti)
    return np.array(t),np.array(c)

dt=.001       
tn,cn=euler(c0,dt=dt,tf=tf)
tn_rk,cn_rk=rk2(c0,dt=0.01,tf=tf)
tn_rk4,cn_rk4=rk4(c0,dt=0.1,tf=tf)
tn_a,cn_a=euler_adpative(c0,EPS=1e-5,tf=tf)
tn_ark,cn_ark=rk_adpative(c0,tf=tf)
ca=analytical(tn)
plt.plot(tn,cn,'*',label='Euler-explicit')
plt.plot(tn_a,cn_a,'^',label='Euler-adaptive')
plt.plot(tn_ark,cn_ark,'^',label='RK-adaptive')
plt.plot(tn_rk,cn_rk,'-',label='RK-2')
plt.plot(tn_rk4,cn_rk4,':',label='RK-4')
plt.plot(tn,ca,'-')
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.grid()

print('Error Euler Explicit ', np.abs(cn[-1]-analytical(tn[-1])), ' no steps ', len(cn) )
print('Error Explicit - RK2 ', np.abs(cn_rk[-1]-analytical(tn_rk[-1])), ' no steps ', len(cn_rk) )
print('Error Explicit - RK4 ', np.abs(cn_rk4[-1]-analytical(tn_rk4[-1])), ' no steps ', len(cn_rk4) )
print('Error Euler Adaptive method ', np.abs(cn_a[-1]-analytical(tn_a[-1])), ' no steps ', len(cn_a) )
print('Error RK Adaptive method ', np.abs(cn_ark[-1]-analytical(tn_ark[-1])), ' no steps ', len(cn_ark) )

# %%
