import matplotlib.pyplot as plt
import numpy as np

def analytical(x,tau,ci):
    d=x/tau
    return ci*np.exp(-d)

def one_step(c_old, c_in, tau_inv,dt):
    fact=dt*tau_inv
    return (1-fact)*c_old+fact*c_in

def euler(c_into,c_init,t_final,vol,q,dt):
    f=[];t=[]
    tau_inv = q/vol
    c_in    = c_into #freshwater into tank
    c_old   = c_init #seawater present 
    ti=0.
    while(ti <= t_final):
        t.append(ti); f.append(c_old)
        c_new = one_step(c_old,c_in,tau_inv,dt)     
        c_old = c_new
        ti   += dt
    return t,f
# rest of code is to make a figure
# choose some step sizes to investigate
dt = [100,400]
# initial values
vol=1000;q=1;c_into = 0; c_init = 35
t_final=2000 # end of simulation in min
t=[];f=[]
for dti in dt:
    ti,fi = euler(c_into,c_init,t_final,vol,q,dti)
    t.append(ti)
    f.append(fi)
# note that t has to converted to array in order to
# use simple operations like / *, used in analytical
f_an = analytical(np.array(t[0]),vol/q,c_init)
symb = ['-p','-v','-*','-s']
fig = plt.figure(dpi=150)
for i in range(0,len(dt)-1):
    plt.plot(t[i+1], f[i+1], symb[i+1], label='$\Delta t =$'
             +str(dt[i+1])+'min')
plt.plot(t[0], f_an, '-', color='k',label='analytical')
#plt.legend(loc='upper right', ncol=1)
plt.grid()
plt.xticks([])
plt.yticks([])
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.savefig('../fig-ode/euler_tofig.png', bbox_inches='tight'
            ,transparent=True)
plt.show()
