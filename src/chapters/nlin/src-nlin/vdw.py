import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt

def vdwEOS(nu,t,a=-1,b=-1):
    """returns the pressure given molar volume nu,
       and temperature t using the re scaled van der Waal
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

def plot_EOS(nu,t,ll=0.6,pr=0,name='vdw'):

    for ti in t:
        p = vdwEOS(nu,ti)-pr
        plt.plot(nu,p,label=r"$\hat{T}$ = "+str(ti))
    # putting labels 
    plt.xlabel(r'$\hat{\nu}$') 
    if(pr>0):
        plt.ylabel(r'$\hat{P}-$'+str(pr))
 #       plt.ylim(-0.5,1)
 #       plt.xlim(0.5,2.5)
    else:
        plt.ylabel(r'$\hat{P}$')
        plt.ylim(0,3)
    if(ll>0):
        plt.plot(nu,np.repeat(ll,len(nu)), 'k', ls='--')
    plt.grid()
    plt.legend()
    fname='../fig-nlin/' + name + '.png'
    plt.savefig(fname, bbox_inches='tight',transparent=True)
    plt.show() 


     
  
if __name__ == "__main__": 
    t = np.array([0.9, 1.0,1.1, 1.2])
    nu = np.arange(.5,6,0.01)
#    plot_EOS(nu,t)
    
#    plot_EOS(nu,[1.2],1.5,name='vdwr1')
    plot_EOS(nu,[0.9],0,pr=0.5,name='vdwr_close')
