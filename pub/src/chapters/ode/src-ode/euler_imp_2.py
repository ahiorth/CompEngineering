import matplotlib.pyplot as plt
import numpy as np

def fm(c_old,c_in,tau,h):
    return (c_old+c_in*h/tau)/(1+h/tau)

def euler_step(c_old, c_in, tau, h):
    c_next=[]
    for i in range(len(c_old)):
        if(i>0): c_in[i]=c_next[i-1] # c_new in next tank
        c_next.append(fm(c_old[i],c_in[i],tau[i],h))
    return c_next

def ode_solv(c_into,c_init,t_final,tau,h):
    f=[];t=[]
    c_in  = c_into #freshwater into first tank
    c_old = c_init #seawater present 
    ti=0.
    while(ti <= t_final):
        t.append(ti); f.append(c_old)
        c_new = euler_step(c_old,c_in,tau,h)     
        c_old = c_new
        # put concentration of tank 0 into tank 1 etc.
        for i,ci in enumerate(c_old[:len(c_old)-1]):
            c_in[i+1]=ci
        ti   += h
    return np.array(t),np.array(f)
h = 0.01
# initial values
vol=1;q=1;c_into = [0,0]; c_init = [1,0]
tau=[1,1e-3];t_final=10 # end of simulation 
t,f = ode_solv(c_into,c_init,t_final,tau,h)
# rest of code is to make a figure

f_an = [];t_an=np.arange(0,t_final,0.01)
f_an.append(c_init[0]*np.exp(-t_an))
f_an.append(c_init[0]*(1-tau[1]/tau[0])*(np.exp(-t_an/tau[0])-np.exp(-t_an/tau[1])))
symb = ['-p','-v','-*','-s']
fig = plt.figure(dpi=150)
for i in range(0,len(c_init)):
    legi = '$\hat{C}_'+str(i)+'(\\tau)$'
    plt.plot(t, f[:,i], '-', label=legi,lw=4)
    plt.plot(t_an, f_an[i], '--', color='k')
plt.plot(0,0 , '--', color='k',label='analytical')
plt.legend(loc='upper right', ncol=1)
#plt.ylim([0,50])
plt.grid()
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.savefig('../fig-ode/euler_imp_2.png', bbox_inches='tight'
            ,transparent=True)
plt.show()
