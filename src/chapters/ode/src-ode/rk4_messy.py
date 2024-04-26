import matplotlib.pyplot as plt
import numpy as np

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
h = 1e-2
# initial values
vol=1;q=1;c_into = [0,0,0]; c_init = [1,0,0]
tau=[1,1,1];t_final=10 # end of simulation 
t,f = ode_solv(c_into,c_init,t_final,tau,h)
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
