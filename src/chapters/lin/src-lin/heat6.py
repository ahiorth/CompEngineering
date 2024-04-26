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
    def __init__(self,h):
        self.h=h
        self.dt=60*60*24 # 1 day
        self.t_final=60*60*24*50 # 10 days
    # Set simulation parameters
        self.L = 1.0              # length of domain
        self.k=1.65
        self.cp=1000
        self.rho=2400
        self.n = int(round(self.L/self.h))  # number of cells 
        self.y=np.arange(self.n)*h   
        self.Tb=25
        self.sigma = 100*self.L**2/1.65
        self.alpha=self.rho*self.cp*self.L*self.L/self.k
        self.a=np.ones(self.n-1)
        self.b=-(2+self.alpha*h*h/self.dt)*np.ones(self.n)
        self.c=np.ones(self.n-1)
        
        self.T_old=np.repeat(self.Tb,self.n)
        #### boundary conditions - central difference ##
        self.c[0]=2
        
        self.A=tri_diag(self.a,self.b,self.c)
    def analytical(self,x):
        return self.sigma*(1-x*x)/2+self.Tb
    def solve_time(self):
        self.t=0
        while self.t<self.t_final:
            self.solve()
            self.T_old=np.copy(self.Tn)
            self.plot()
            self.t +=self.dt   

    def solve(self):
        self.d=np.repeat(-self.h*self.h*self.sigma,self.n)
        self.d = self.d-self.alpha*self.h*self.h/self.dt*self.T_old
        self.d[-1]=self.d[-1]-self.Tb # constant temperature
        self.Tn=np.linalg.solve(self.A,self.d)
 
    def plot(self):
        ya=np.arange(0,1,0.01)
        Ta=self.analytical(ya)
        plt.title('Heat distribution at time ' + str(self.t/(24*60*60))+ ' days')
        plt.plot(self.y,self.Tn,'*', label='numerical n=' + str(self.n))
        plt.plot(ya,Ta, label='analytical' )
        plt.legend()
        plt.grid()
        plt.show()
    def error(self):
        i=self.n//2
        yi=self.y[i]
        return np.abs(self.analytical(yi)-self.Tn[i])



H1=HeatSolver(0.25)
H1.solve_time()

# %%
