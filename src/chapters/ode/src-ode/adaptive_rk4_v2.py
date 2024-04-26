import matplotlib.pyplot as plt
import numpy as np

def fm(c_old,c_in):
    return c_in-c_old

def rk4_step(c_old, c_in, h):
    k1=h*fm(c_old,c_in)
    k2=h*fm(c_old+0.5*k1,c_in)
    k3=h*fm(c_old+0.5*k2,c_in)
    k4=h*fm(c_old+    k3,c_in)
    return c_old+(k1+2*k2+2*k3+k4)/6

def adaptive_ode_solv(c_into,c_init,t_final,atol=1e-4,rtol=1e-4):
    f=[];t=[]
    c_in    = c_into #freshwater into tank
    c_old   = c_init #seawater present 
    ti=0.; h_new=1;
    toli=1.; # a high init tolerance to enter while loop
    no_steps=0
    while(ti <= t_final):
        t.append(ti); f.append(c_old)
        tol = atol + rtol*c_old 
        while(toli>tol):# first two small steps
            hi=h_new
            k1 = rk4_step(c_old,c_in,hi*.5)
            k2 = rk4_step(k1,c_in,hi*.5)
            # ... and one large step
            k3 = rk4_step(c_old,c_in,hi)
            toli = abs(k3-k2)/15
            h_new=min(hi*(tol/toli)**(0.2),1)
            no_steps+=3
        toli=1.
        c_old=(16*k2-k3)/15
        ti   += hi
    print("No steps=", no_steps, "Tol=", tol)
    return t,f
# rest of code is to make a figure
vol=1;q=1;c_into = 0; c_init =1
t_final=4 # end of simulation
t=[];f=[]
tol=[1e-8,1e-7,1e-6,1e-5]
for toli in tol:
    ti,fi = adaptive_ode_solv(c_into,c_init,t_final,toli,0)
    t.append(ti);f.append(fi)

f_an = np.exp(-np.array(t[0]))
symb = ['-p','-v','-*','-s']
fig = plt.figure(dpi=150)
for i in range(0,len(tol)):
    plt.plot(t[i], f[i], symb[i], label='tol='+str(tol[i]))
plt.plot(t[0], f_an, '-', color='k',label='analytical')
plt.legend(loc='lower left', ncol=1)
plt.grid()
#plt.yscale('log')
plt.xlabel(r'Time [min/$\tau$]')
plt.ylabel('Concentration')
plt.savefig('../fig-ode/adaptive_rk4.png', bbox_inches='tight'
            ,transparent=True)
plt.show()
