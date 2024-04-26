#%%
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

def rk4_step(func,y,t,dt):
    k1=dt*func(y,t)
    k2=dt*func(y+0.5*k1,t+0.5*dt)
    k3=dt*func(y+0.5*k2,t+0.5*dt)
    k4=dt*func(y+k3,t+dt)
    return (k1+2*k2+2*k3+k4)/6

def rk_adpative(func,y0,t0,tf,rel_tol=1e-5,abs_tol=1e-5,p=4):
    c=[]
    t=[]
    ti=t0
    c.append(y0)
    t.append(ti)
    dt=1e-2 # start with very small step 
    while(ti<=tf):
        EPS=np.linalg.norm(c[-1])*rel_tol+abs_tol
        eps=1
        while(eps>EPS): # find correct dt
            DT=dt
            c_new = c[-1] + rk4_step(func,c[-1],ti,DT) #one large step
            c1    = c[-1] + rk4_step(func,c[-1],ti,DT*0.5) # and two small steps
            c2    = c1 + rk4_step(func,c1,ti+0.5*DT,DT*0.5)
            eps   = np.linalg.norm(c2-c_new)/(2**p-1)
            dt = 0.9*DT*(EPS/eps)**(1/(p+1)) # could also multiply with 0.9 to be conservative
        c.append((2**p*c2-c_new)/(2**p-1))
        #c.append(c2)
        ti=ti+DT
        t.append(ti)
    return np.array(t),np.array(c)

def my_odeint(func,y0,t,rel_tol=1e-5,abs_tol=1e-5):
    """
    same call syntax as scipy.integrate.odeint
    t is a numpy vector containing the times at which the solution is to be calculated
    """
    y=[]
    ti=t[0]
    tf=t[-1]
    
    dt_list=t[1:]-t[:-1]
    dt_list=dt_list.tolist()
    t_list=np.copy(t[1:]).tolist()
    #avoid pop from empty list
    t_list.append(0.)
    dt_list.append(0.)

    next_time=t_list.pop(0)
    next_dt  = dt_list.pop(0)
    y.append(y0)
    y_old=y0
    p=4
    dt=1e-2 # intitial guess  
    while(ti<tf):
        EPS=np.linalg.norm(y_old)*rel_tol+abs_tol
        eps=1
        while(eps>EPS): # find correct dt
            DT=min(dt,next_dt)
            y_new = y_old + rk4_step(func,y_old,ti,DT) #one large step
            y1    = y_old + rk4_step(func,y_old,ti,DT*0.5) # and two small steps
            y2    = y1 + rk4_step(func,y1,ti+0.5*DT,DT*0.5)
            eps   = np.linalg.norm(y2-y_new)/(2**p-1)
            dt = 0.9*DT*(EPS/eps)**(1/(p+1)) # could also multiply with 0.9 to be conservative
        y_old=(2**p*y2-y_new)/(2**p-1)
        next_dt=next_dt-DT
        ti=ti+DT
        if np.abs(ti-next_time) < 1e-8:
             y.append(y_old)
             next_time=t_list.pop(0)
             next_dt  = dt_list.pop(0)
    return np.array(y)

def g(y,t):
    return np.array([y[1],-y[0]])
def f(y,t):
    return np.array([y[1],1/t-2*y[1]/t-1])

def analytical(x):
    return 5/2-5/(6*x)+x/2-x*x/6

y0=np.array([2,1])
#y0=np.array([0,1])

tf=10
t=np.linspace(1, tf, 3)

y=my_odeint(f, y0, t)
sol = odeint(f, y0, t)

x_rk,y_rk=rk_adpative(f,y0,1,tf)
plt.plot(t,y[:,0],'*',label='numerical')
plt.plot(x_rk,y_rk[:,0],'*',label='numerical-RK')
plt.plot(t,analytical(t),'-',label='analytical')
plt.plot(t,sol[:,0],'^',label='odeint')

#plt.plot(x,analytical(x),label='analytical')
plt.grid()
plt.legend()

# %%
