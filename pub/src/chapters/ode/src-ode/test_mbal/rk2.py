import matplotlib.pyplot as plt
import numpy as np

def fm(c_old,c_in):
    return c_in-c_old

def rk2_step(c_old, c_in, h):
    k1=h*fm(c_old,c_in)
    k2=h*fm(c_old+0.5*k1,c_in)
    return c_old+k2

def rk4_step(c_old, c_in, h):
    k1=h*fm(c_old,c_in)
    k2=h*fm(c_old+0.5*k1,c_in)
    k3=h*fm(c_old+0.5*k2,c_in)
    k4=h*fm(c_old+    k3,c_in)
    return c_old+(k1+2*k2+2*k3+k4)/6

def ode_solv(c_into,c_init,t_final,h):
    f=[];t=[];m=[]
    c_in  = c_into #freshwater into tank
    c_old = c_init #seawater present 
    ti=0.
    mout=mbal=0
    while(ti <= t_final):
        t.append(ti); f.append(c_old);m.append(mbal)
        c_new = rk2_step(c_old,c_in,h)
        mout += (c_old+c_new)*h/2
        c_old = c_new
        mbal = (c_new+mout-c_init)/(c_init)
        ti   += h
    print(mbal)
    return t,f,m
# rest of code is to make a figure
# choose some step sizes to investigate
h = [0.01,0.1,0.5,0.9]
# initial values
vol=1000;q=1;c_into = 0; c_init = 35
tau=vol/q;t_final=100 # end of simulation in min
t=[];f=[];m=[]
for dti in h:
    ti,fi,mi = ode_solv(c_into,c_init,t_final,dti)
    t.append(np.array(ti));f.append(fi);m.append(mi)
f_an = c_init*np.exp(-np.array(t[0]))
symb = ['-p','-v','-*','-s']
fig = plt.figure(dpi=150)
for i in range(0,len(h)):
    plt.plot(tau*t[i], m[i], symb[i], label='$\Delta t =$'
             +str(h[i]*tau)+" min")
#plt.plot(tau*t[0], f_an, '-', color='k',label='analytical')
plt.legend(loc='upper right', ncol=1)
#plt.ylim([-0.5,4])
#plt.xlim([0,1000])
plt.grid()
plt.xlabel('Time [min]')
#plt.yscale('log')
plt.ylabel('Concentration')
plt.savefig('rk2.png', bbox_inches='tight'
            ,transparent=True)
plt.show()
