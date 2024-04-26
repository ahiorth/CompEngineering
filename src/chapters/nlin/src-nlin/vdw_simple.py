import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt

def vdwEOS(nu,t,a=-1,b=-1):
    """returns the pressure given molar volume nu,
       and temperature t using the rescaled van der Waal
       EOS """
    if(a<0):
        return 8*t/(3*nu-1)-3/(nu*nu)
    else:
        tc=8*a/(27*b)
        pc=8*a/(27*b*b)
        nuc=3*b
        nu2 = nu*nuc
        print(tc,pc,nu2)
#        return (8*t*tc/(3*nu2-1)-3/(nu2*nu2))*pc
        Rg=8.314
        print(Rg*t/(nu-b), a/nu/nu)
        return Rg*t/(nu-b)-a/nu/nu

def dvdwEOS(nu,t,p):
    return (1+8*t/(p+3/nu**2))/3
    

def dCO2EOS(v,P,T):
    """ returns the specific volume for CO2 - given P and T"""
    Rg=8.314 #J/mol K
    a=0.3640 #m^6Pa/mol
    b=4.267e-5 #m^3/mol
    Mw=44e-3 #kg/mol
    v = v*Mw #m^3/mol 
    return (P-a/(v*v))*(v-b)-Rg*T

def dCO2EOS2(v,P,T):
    """ returns the specific volume for CO2 - given P and T"""
    Rg=8.314 #J/mol K
    a=0.3640 #m^6Pa/mol
    b=4.267e-5 #m^3/mol
    Mw=44e-3 #kg/mol
    v = v*Mw #m^3/mol
    tc=8*a/(27*b)/Rg
    pc=8*a/(27*b*b)
    nuc=3*b
    t=T/tc
    p=P/pc
    nu = v/nuc
#    return 3*p*nu*nu*nu-(p+8*t)*nu*nu+9*nu-3
    return (p+3/(nu*nu))*(3*nu-1)-8*t

def der(v,P,T):
   return 16*T*v/(P*v**2+3)**2

def plot_EOS(nu,t):

    for ti in t:
        p = vdwEOS(nu,ti)
        z = der(nu,1.5,ti)
        plt.plot(nu,p,label=r"$\hat{T}$ = "+str(ti))
        plt.plot(nu,z,label=r"$f^\prime(x)\hat{T}$ = "+str(ti))
    # putting labels 
    plt.xlabel(r'$\hat{\nu}$') 
    plt.ylabel(r'$\hat{P}$')
    plt.ylim(0,3)
    plt.grid()
    plt.legend()
    plt.plot(nu,np.repeat(0.6,len(nu)), 'k', ls='--')
#    plt.savefig('../fig-nlin/vdw.png', bbox_inches='tight',transparent=True)
    plt.show() 

def f2(x,*args):
    return x-2+np.exp(-x)

def f(x,*args):
    return x**2-np.exp(-x)

def g(x,*args):
    return x-f(x)

def h(x):
    return np.sqrt(x**2+f(x))

def iterative(x,g,*args,prec=1e-8):
    MAX_ITER=1000
    eps = 1
    n=0
    while eps>prec and n < MAX_ITER:
        x_next = g(x,*args)
        eps = np.abs(x-x_next)
        x = x_next
        n += 1
    print('Number of iterations: ', n)
    return x
#end
#def bisection(f,a,b):
    
  
if __name__ == "__main__":

    iterative(1,dvdwEOS,1.2,1.5)

    s1= iterative(1.5,g)
    t = np.array([0.9, 1.0,1.1, 1.2])
    nu = np.arange(.5,3,0.01)
    plot_EOS(nu,t)

    x = np.arange(-2,2,0.01)
#    x=x/0.128
    P=2e6
    T=273.15+100
#    print(iterative(0.25,g))
    plt.plot(x,f(x),'--',label=r'$f(x)=x^2-e^{-x}$')
    plt.plot(x,g(x),'-', label =r'$g(x)=x-f(x)$')
#    plt.plot(x,h(x))
    plt.plot(x,x, ':',label ='x')
    plt.axvline(s1)
    plt.plot(s1,s1,'ro')
    plt.plot(s1,0,'ro', label ='root')
#    plt.plot(x,dCO2EOS2(x,P,T), label ='x')
#    plt.xlim(-max(x),max(x))
    plt.ylim(-2,2)
    plt.xlim(0,0.8)
    plt.grid()
    plt.legend(loc='upper left',ncol=2)
#    plt.savefig('../fig-nlin/f_g.png', bbox_inches='tight',transparent=True)
    plt.show()
    plt.close()
    
    plt.plot(x,x*x,'--',label=r'$x^2$')
    plt.plot(x,np.exp(-x),'-', label =r'$e^{-x}$')
    plt.plot(x,f(x),'-', label =r'$f(x)$')
#    plt.plot(x,h(x))
    plt.plot(s1,s1*s1,'ro')
    plt.plot(s1,0,'ro', label ='root')
#    plt.plot(x,dCO2EOS2(x,P,T), label ='x')
#    plt.xlim(-max(x),max(x))
    plt.ylim(-0.5,2)
    plt.xlim(0,2)
    plt.grid()
    plt.legend(loc='upper left',ncol=2)
#    plt.savefig('../fig-nlin/fx.png', bbox_inches='tight',transparent=True)
    plt.show()
    
    

