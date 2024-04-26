#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
c_in=0
c0=1
q=321*24*60*60*365 #m^3/year
V=56*1000**3    #m^3
tau=V/q        #day
def rk2_step(func,y,t,dt,*args):
    """
    Integrates from time t to t+h using RK2
    func = right hand side of ODE
    y = solution vector
    t = current time
    h = step size
    """
    k1=dt*func(y,t,*args)
    k2=dt*func(y+0.5*k1,t+dt*0.5,*args)
    return k2

def rk4_step(func,y,t,dt,*args):
    """
    Integrates from time t to t+h using RK4
    func = right hand side of ODE
    y = solution vector
    t = current time
    dt = step size
    """
    k1=dt*func(y,t,*args)
    k2=dt*func(y+0.5*k1,t+0.5*dt,*args)
    k3=dt*func(y+0.5*k2,t+0.5*dt,*args)
    k4=dt*func(y+k3,t+dt,*args)
    return (k1+2*k2+2*k3+k4)/6

def ode_solv(func,y0,dt,t0,tf,*args):
    """
    solves a set of ODE with known initial conditions
    from time ti to t_final
    ti = start time
    y0 = initial conditions at time t0
    tf = end time
    dt = step size
    """
    y=[];t=[]
    ti=t0
    y_old=y0
    while(ti <= tf):
        t.append(ti); y.append(y_old)
        y_new = y_old+rk4_step(func,y_old,ti,dt,*args) # or rk2_step    
        y_old = y_new
        ti   += dt
    return np.array(t),np.array(y)

def func(y,t):
    return 1/tau*(c_in-y)
dt=.1
t,y=ode_solv(func,c0,dt,0,20)
print('Numerical Error ', np.abs(y[-1]-np.exp(-t[-1]/tau)))

plt.plot(t,y,'*',label='numerical')
plt.plot(t,np.exp(-t/tau),label='analytical')
plt.xlabel('Time [years]')
plt.legend()
plt.grid()


def rk_adpative(func,y0,t0,tf,*args,rel_tol=1e-5,abs_tol=1e-5,p=4):
    """
    solves an ODE with known initial conditions
    from time ti to t_final
    ti = start time
    y0 = initial conditions at time t0
    tf = end time
    rel_tol relative toleranse
    abs_tol absolute toleranse
    p order of numerical method, could set p=2 and 
    change rk4_step to rk2_step
    """
    y=[]
    t=[]
    ti=t0
    y.append(y0)
    t.append(ti)
    dt=1e-2 # start with a small step 
    while(ti<=tf):
        y_old=y[-1]
        EPS=np.abs(y_old)*rel_tol+abs_tol
        eps=10*EPS
        while(eps>EPS): # find correct dt
            DT=dt
            # one large step from t to t+dt
            y_new = y_old + rk4_step(func,y_old,ti,DT) 
            # and two small steps - from t -> t+dt/2
            y1    = y_old + rk4_step(func,y_old,ti,DT*0.5) 
            # and from t+dt/2 to t + dt
            y2    = y1 + rk4_step(func,y1,ti+0.5*DT,DT*0.5)
            eps   = np.abs(y2-y_new)/(2**p-1) # estimate numerical error
            dt = 0.9*DT*(EPS/eps)**(1/(p+1))  # calculate new time step
        y.append((2**p*y2-y_new)/(2**p-1))
        ti=ti+DT # important to add DT not dt
        t.append(ti)
    return np.array(t),np.array(y) # cast to numpy arrays

xa,ya=rk_adpative(func,c0,0,20)
print('Numerical Error adaptive ', np.abs(ya[-1]-np.exp(-xa[-1]/tau)))

plt.plot(xa,ya,'^',label='adaptive')
plt.legend()
plt.show()
plt.close()



def fm(c,t): # rhs of tanks in series
    c_in=0
    tau=1
    rhs=[]
    rhs.append(c_in-c[0])
    rhs.append(c[0]-c[1])
    rhs.append(c[1]-c[2])
    return np.array(rhs)/tau

# initial values
tau=1
vol=1;q=1;c_into = 0; c_init = [1,0,0]
t_final=10 # end of simulation
dt=1e-2 
#note same solver as before
t_vec,f_vec=ode_solv(fm,c_init,dt,0,t_final)

f_an = []
f_an.append(c_init[0]*np.exp(-t_vec/tau))
f_an.append(c_init[0]*t_vec/tau*np.exp(-t_vec/tau))
f_an.append(c_init[0]*0.5*t_vec*t_vec/tau/tau*np.exp(-t_vec/tau))

symb = ['-p','-v','-*','-s']
for i in range(len(c_init)):
    legi = '$\hat{C}_'+str(i)+'(\\tau)$'
    plt.plot(t_vec, f_vec[:,i], '-', label=legi,lw=4)
    plt.plot(t_vec, f_an[i], '--', color='k')
plt.plot(0,0 , '--', color='k',label='analytical')
plt.legend(loc='upper right', ncol=1)
#plt.ylim([0,50])
plt.grid()
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.show()


def g(y,t):
    return np.array([y[1],-y[0]])

def f2(y,t):
    return np.array([y[1],1/t-2*y[1]/t-1])

def analytical(x):
    return 5/2-5/(6*x)+x/2-x*x/6

y0=np.array([2,1])
x,y=ode_solv(f2,y0,1e-1,1,10)

plt.plot(x,y[:,0],'*',label='numerical')
plt.plot(x,analytical(x),'-',label='analytical')

t=np.linspace(1, 10, 10)
sol = odeint(f2, y0, t)
plt.plot(t,sol[:,0],'^',label='odeint')

#plt.plot(x,analytical(x),label='analytical')
plt.grid()
plt.legend()




# %%
