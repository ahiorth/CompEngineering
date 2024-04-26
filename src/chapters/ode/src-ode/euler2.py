import matplotlib.pyplot as plt
import numpy as np

def analytical(t,tau,ci):
    d=t/tau
    return ci*np.exp(-d)

def one_step(c_old, c_in, tau_inv,dt):
    fact=dt*tau_inv
    return (1-fact)*c_old+fact*c_in

def euler(c_into,c_init,t_final,vol,q,dt):
    f=[] 
    t=[]
    c_in = c_into  #freshwater into tank
    c_old = c_init #seawater present
    tau_inv = q/vol 
    ti=0.
    t.append(ti);f.append(c_old)
    cum_err=0;
    while(ti <= t_final):
        ti += dt
        t.append(ti)
        c_new = one_step(c_old,c_in,tau_inv,dt)
        c_an=analytical(ti,1/tau_inv,c_init)
        cum_err += abs(c_an-c_new)
        print(ti,c_an,c_new,cum_err)
        f.append(c_new)
        c_old=c_new
    print("Cumm Error = ", cum_err)
    print("Est Cumm Error = ", dt*c_init*.5)
    return t,f
dt = [0.01,0.1]
t=[];f=[]
t_final=1;c_into = 0; c_init = 35
vol=1;q=1
for dti in dt:
    ti,fi = euler(c_into,c_init,t_final,vol,q,dti)
    t.append(ti)
    f.append(fi)
# note that t has to converted to array in order to
# use simple operations like / * etc.
f_an = analytical(np.array(t[0]),1000,35)
symb = ['-p','-v','-h','-s']
fig = plt.figure(dpi=150)
for i in range(0,len(dt)):
    plt.plot(t[i], f[i], symb[i], label='$\Delta t =$'+str(dt[i])+'min')
plt.plot(t[0], f_an, '-', color='k',label='analytical')
plt.legend(loc='upper right', ncol=1)
plt.grid()
plt.ylabel('Concentration')
plt.xlabel('Time [min]')
# Save the plot in a file
plt.savefig('../fig-ode/euler.png', bbox_inches='tight',transparent=True)
plt.show()
