import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt





def g(x):
    return x-f(x)

def h(x):
    return np.sqrt(x**2-f(x))

def f(x):
    return x**2-np.exp(-x)

def f2(x):
    return x**2-np.exp(1-x**2)

def f3(x):
    return x+2*x-np.exp(-x)

def f2inv(x):
    return np.sqrt(x**2-np.log(x*x))

def iterative(x,g,prec=1e-8, MAXIT=1000):
    '''Approximate solution of x=g(x) by fixed point iterations.
    x : starting point for iterations 
    eps : desired precision
    Returns x when x does not change more than prec
    and number of iterations MAXIT are not exceeded
    '''
    eps = 1
    n=0
    while eps>prec and n < MAXIT:
        x_next = g(x)
        eps = np.abs(x-x_next)
        x = x_next
        n += 1
        if(np.isinf(x)):
            print('Quitting .. maybe bad starting point?')
            return x
    if (n<MAXIT):
        print('Found solution: ', x, ' After ', n, 'iterations')
    else:
        print('Max number of iterations exceeded')
    return x
#end
#def bisection(f,a,b):
    
  
if __name__ == '__main__':

    s1= iterative(100,g)
    s2= iterative(100,h)

    
    
#    s3=iterative(.01,f2)
#    s4=iterative(.01,f2inv)

    x = np.arange(-100,100,0.01)
#    x=x/0.128
    P=2e6
    T=273.15+100
#    print(iterative(0.25,g))
    plt.plot(x,f(x),'-',label=r'$f(x)=x^2-e^{-x}$')
#    plt.plot(x,h(x),'-', label =r'$g(x)=e^{-x/2}$')
#    plt.plot(x,h(x),'-', label =r'$g(x)=x-f(x)$')
#    plt.plot(x,h(x))
#    plt.plot(x,x, ':',label ='x')
#    plt.axvline(s1)
    plt.plot(s2,s2,'ro')
    plt.plot(s1,0,'ro', label ='root')
#    plt.plot(x,dCO2EOS2(x,P,T), label ='x')
#    plt.xlim(-max(x),max(x))
#    plt.ylim(-100,100)
    plt.xlim(-150,150)
    plt.grid()
    plt.xlabel(r'$x$')
    plt.legend(ncol=2)
#       plt.savefig('../fig-nlin/newton_bad.png', bbox_inches='tight',transparent=True)
    plt.show()
    plt.close()
    
    plt.plot(x,x*x,'--',label=r'$x^2$')
    plt.plot(x,np.exp(-x),'-', label =r'$e^{-x}$')
    plt.plot(x,f(x),'-', label =r'$x^2-e^{-x}$')
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
    
    

