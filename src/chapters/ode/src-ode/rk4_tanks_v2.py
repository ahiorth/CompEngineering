import matplotlib.pyplot as plt
import numpy as np

def fm(c,t,c_in,tau):
    rhs=[]
    rhs.append(c_in-c[0])
    rhs.append(c[0]-c[1])
    rhs.append(c[1]-c[2])
    return np.array(rhs)/tau

def rk4_step(t,c,h,*args):
    """
    Integrates from time t to t+h using RK4
    t = current time
    h = step size
    c = solution vector
    """
    k1=h*fm(c,t,*args)
    k2=h*fm(c+0.5*k1,t+0.5*h,*args)
    k3=h*fm(c+0.5*k2,t+0.5*h,*args)
    k4=h*fm(c+k3,t+h,*args)
    return c+(k1+2*k2+2*k3+k4)/6

def ode_solv(ti,c,t_final,h,*args):
    """
    solves a set of ODE with known initial conditions
    from time ti to t_final
    ti = start time
    c = initial conditions at time ti
    t_final = end time
    h = step size
    """
    f=[];t=[]
    c_old = c      #seawater present 
    while(ti <= t_final):
        t.append(ti); f.append(c_old)
        c_new = rk4_step(ti,c_old,h,*args)     
        c_old = c_new
        ti   += h
    return np.array(t),np.array(f)
h = 1e-2
# initial values
vol=1;q=1;c_into = 0; c_init = [1,0,0]
tau=[1,1,1];t_final=10 # end of simulation 
t,f = ode_solv(0,c_init,t_final,h,c_into,tau)
# rest of code is to make a figure

f_an = []
f_an.append(c_init[0]*np.exp(-t))
f_an.append(c_init[0]*t*np.exp(-t))
f_an.append(c_init[0]*0.5*t*t*np.exp(-t))

symb = ['-p','-v','-*','-s']
fig = plt.figure(dpi=150)
for i in range(0,len(c_init)):
    legi = '$\hat{C}_'+str(i)+'(\\tau)$'
    plt.plot(t, f[:,i], '-', label=legi,lw=4)
    plt.plot(t, f_an[i], '--', color='k')
plt.plot(0,0 , '--', color='k',label='analytical')
plt.legend(loc='upper right', ncol=1)
#plt.ylim([0,50])
plt.grid()
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.savefig('../fig-ode/rk4_2.png', bbox_inches='tight'
            ,transparent=True)
plt.show()
