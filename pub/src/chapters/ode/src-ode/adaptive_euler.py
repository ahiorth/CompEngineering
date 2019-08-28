import matplotlib.pyplot as plt
import numpy as np

def one_step(c_old, c_in,h):
    return (1-h)*c_old+h*c_in

def adaptive_euler(c_into,c_init,t_final,tol=1e-4):
    f=[];t=[]
    c_in    = c_into #freshwater into tank
    c_old   = c_init #seawater present 
    ti=0.; h_new=1e-3;
    toli=1.; # a high init tolerance to enter while loop
    no_steps=0
    global_err=0.
    while(ti <= t_final):
        t.append(ti); f.append(c_old)
        while(toli>tol):# first two small steps
            hi=h_new
            k1 = one_step(c_old,c_in,hi*.5)
            k2 = one_step(k1,c_in,hi*.5)
            # ... and one large step
            k3 = one_step(c_old,c_in,hi)
            toli = abs(k3-k2)
            h_new=hi*np.sqrt(tol/toli)
            no_steps+=3
        toli=1.
        c_old=2*k2-k3 # higher order correction
 # normal Euler, uncomment and inspect the global error
 #       c_old = k2 
        ti   += hi
        global_err += abs(np.exp(-ti)-c_old)
    print("No steps=", no_steps, "Global Error=", global_err)
    return t,f
# rest of code is to make a figure
c_into = 0; c_init =1; t_final=10
t=[];f=[]
tol=[1e-6,1e-3,1e-2,1e-1]
for toli in tol:
    ti,fi = adaptive_euler(c_into,c_init,t_final,toli)
    t.append(ti);f.append(fi)

f_an = np.exp(-np.array(t[0]))
symb = ['-p','-v','-*','-s']
fig = plt.figure(dpi=150)
for i in range(0,len(tol)):
    plt.plot(t[i], f[i], symb[i], label='tol='+str(tol[i]))
plt.plot(t[0], f_an, '-', color='k',label='analytical')
plt.legend(loc='lower left', ncol=1)
plt.grid()
plt.yscale('log')
plt.xlabel(r'Time [t/$\tau$]')
plt.ylabel('Concentration')
plt.savefig('../fig-ode/adaptive_euler.png', bbox_inches='tight'
            ,transparent=True)
plt.show()
