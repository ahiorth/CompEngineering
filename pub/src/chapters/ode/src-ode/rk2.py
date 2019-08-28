import matplotlib.pyplot as plt
import numpy as np

def fm(c_old,c_in):
    return c_in-c_old

def rk2_step(c_old, c_in, h):
    k1=h*fm(c_old,c_in)
    k2=h*fm(c_old+0.5*k1,c_in)
    return c_old+k2

def ode_solv(c_into,c_init,t_final,h):
    f=[];t=[]
    c_in  = c_into #freshwater into tank
    c_old = c_init #seawater present 
    ti=0.
    while(ti <= t_final):
        t.append(ti); f.append(c_old)
        c_new = rk2_step(c_old,c_in,h)     
        c_old = c_new
        ti   += h
    return t,f
# rest of code is to make a figure
# choose some step sizes to investigate
h = [0.4,0.8,1.6,2.1]
# initial values
vol=1000;q=1;c_into = 0; c_init = 35
tau=vol/q;t_final=10 # end of simulation in min
t=[];f=[]
for dti in h:
    ti,fi = ode_solv(c_into,c_init,t_final,dti)
    t.append(np.array(ti));f.append(fi)
f_an = c_init*np.exp(-np.array(t[0]))
symb = ['-p','-v','-*','-s']
fig = plt.figure(dpi=150)
for i in range(0,len(h)):
    plt.plot(tau*t[i], f[i], symb[i], label='$\Delta t =$'
             +str(h[i]*tau)+" min")
plt.plot(tau*t[0], f_an, '-', color='k',label='analytical')
plt.legend(loc='upper right', ncol=1)
plt.ylim([0,50])
plt.grid()
plt.xlabel('Time [min]')
plt.ylabel('Concentration')
plt.savefig('../fig-ode/rk2.png', bbox_inches='tight'
            ,transparent=True)
plt.show()
