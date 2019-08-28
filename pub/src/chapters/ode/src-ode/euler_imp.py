import matplotlib.pyplot as plt
import numpy as np

def analytical(x):
    return np.exp(-x)

def one_step_imp(c_old, c_in, tau_inv,dt):
    fact=dt*tau_inv
    return (c_old+fact*c_in)/(1+fact)

def euler(c_into,c_init,t_final,vol,q,dt):
    f=[];t=[]
    tau_inv = q/vol
    c_in    = c_into #freshwater into tank
    c_old   = c_init #seawater present 
    ti=0.
    while(ti <= t_final):
        t.append(ti); f.append(c_old)
        c_new = one_step_imp(c_old,c_in,tau_inv,dt)     
        c_old = c_new
        ti   += dt
    return t,f
# rest of code is to make a figure
# choose some step sizes to investigate
dt = [100,500,900,1300]
# initial values
vol=1000;q=1;c_into = 0; c_init = 35
t_final=10000 # end of simulation in min
t=[];f=[]
for dti in dt:
    ti,fi = euler(c_into,c_init,t_final,vol,q,dti)
    t.append(np.array(ti));f.append(fi)
# note that t has to converted to array in order to
# use simple operations like / *, used in analytical
f_an = c_init*analytical(np.array(t[0])/vol/q)
symb = ['-p','-v','-*','-s']
fig = plt.figure(dpi=150)
for i in range(0,len(dt)):
    plt.plot(t[i], f[i], symb[i], label='$\Delta t =$'
             +str(dt[i])+'min')
plt.plot(t[0], f_an, '-', color='k',label='analytical')
plt.legend(loc='upper right', ncol=1)
plt.grid()
plt.xlabel('Time [min]')
plt.ylabel('Concentration')
plt.savefig('../fig-ode/euler_imp.png', bbox_inches='tight'
            ,transparent=True)
plt.show()
