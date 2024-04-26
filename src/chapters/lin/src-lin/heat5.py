#%%
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.histograms import _hist_bin_auto

def tri_diag(a, b, c, k1=-1, k2=0, k3=1):
    """ a,b,c diagonal terms
        default k-values for 4x4 matrix:
        | b0 c0 0  0 |
        | a0 b1 c1 0 |
        | 0  a1 b2 c2|
        | 0  0  a2 b3|
    """
    return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)

class HeatSolver:
    def __init__(self,h,central=True):
        self.h=h
    # Set simulation parameters
        self.L = 1.0              # length of domain
        self.n = int(round(self.L/self.h))  # number of cells 
        self.y=np.arange(self.n+1)*h   # includes right bc 
        self.Tb=25
        self.sigma = 100*self.L**2/1.65
        self.a=np.ones(self.n-1)
        self.b=-np.ones(self.n)*2
        self.c=np.ones(self.n-1)
        self.d=np.repeat(-self.h*self.h*self.sigma,self.n)
        self.d[-1]=self.d[-1]-self.Tb # constant temperature
        #### boundary conditions - central difference ###
        if central:
            self.c[0]=2
        else:
            self.b[0]=-1
        self.A=tri_diag(self.a,self.b,self.c)
    def analytical(self,x):
        return self.sigma*(1-x*x)/2+self.Tb
    def solve(self):
        Tn=np.linalg.solve(self.A,self.d)
        #append boundary value
        self.Tn=np.append(Tn,self.Tb)
    def plot(self):
        ya=np.arange(0,1,0.01)
        Ta=self.analytical(ya)
        plt.plot(self.y,self.Tn,'*', label='numerical n=' + str(self.n))
        plt.plot(ya,Ta, label='analytical' )
        plt.legend()
        plt.grid()
    def error(self):
        return np.abs(self.analytical(0)-self.Tn[0])



H1=HeatSolver(0.025,False)
H1.solve()
H1.plot()
print(H1.error()) 
h=np.logspace(-4,-1,10) 
err=[]
for hi in h:
    H1=HeatSolver(hi,False)
    H1.solve()
    err.append(H1.error())
plt.close()
plt.plot(h,err, '*')
plt.xscale('log')
plt.yscale('log')
plt.grid()
# %%
