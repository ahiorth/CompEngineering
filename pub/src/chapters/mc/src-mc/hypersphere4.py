from scipy.special import gamma
import random
import numpy as np

def f(x,R=1):
    r=R*R
    for xi in x:
      r-=xi*xi
    if(r<0):
        return 0.
    else:
        return 2*np.sqrt(r)

def f2(x,R=1):
    r=R*R
    for xi in x:
      r-=xi*xi
    if(r<0):
        return 0.
    else:
        return 1.

def d1_trapez(lower_limit, upper_limit,func,x,i,N,D=1):
    h     = (upper_limit-lower_limit)/N
    x[i]  = lower_limit
    area  = func(x)
    x[i]  = upper_limit
    area += func(x)
    area *= 0.5
    x[i]  = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        x[i]  += h # midpoint value
        area  += func(x)
    return area*h

def d2_trapez(lower_limit, upper_limit,func,x,i,N):
    h     = (upper_limit-lower_limit)/N
    x[i]  = lower_limit
    area  = d1_trapez(lower_limit, upper_limit,func,x,i+1,N)
    x[i]  = upper_limit
    area += d1_trapez(lower_limit, upper_limit,func,x,i+1,N)
    area *= 0.5
    x[i]  = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        x[i] += h # midpoint value
        area += d1_trapez(lower_limit, upper_limit,func,x,i+1,N)
    return area*h        

def d3_trapez(lower_limit, upper_limit,func,x,i,N):
    h     = (upper_limit-lower_limit)/N
    x[i]  = lower_limit
    area  = d2_trapez(lower_limit, upper_limit,func,x,i+1,N)
    x[i]  = upper_limit
    area += d2_trapez(lower_limit, upper_limit,func,x,i+1,N)
    area *= 0.5
    x[i]  = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        x[i] += h # midpoint value
        area += d2_trapez(lower_limit, upper_limit,func,x,i+1,N)
    return area*h

def dd_trapez(lower_limit,upper_limit,func,x,i,N,D):
    h = (upper_limit-lower_limit)/N
    if(i == D-1):
        funci=d1_trapez
    else:
        funci=dd_trapez
    x[i]  = lower_limit
    area  = funci(lower_limit, upper_limit,func,x,i+1,N,D)
    x[i]  = upper_limit
    area += funci(lower_limit, upper_limit,func,x,i+1,N,D)
    area *= 0.5
    x[i]  = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        x[i] += h # midpoint value
        area += funci(lower_limit, upper_limit,func,x,i+1,N,D)
    return area*h      


def mc_nball(N=1000,D=3,R=1):
    """
    Calculates the volume of a hypersphere using accept and reject
    N: Number of random points
    D: Number of dimensions
    R: Radius of hypersphere
    """
    vol=0.
    for _ in range(N):
        r=0.
        for _ in range(D):
            xi=random.uniform(-R,R)
            r+=xi*xi
        if np.sqrt(r) <= R: vol += 1
#    print("Number of points inside n-ball: ", vol)
    return vol/N*(2*R)**D

def mc_nball_sampling(N=1000,D=3,R=1):
    """
    Calculates the volume of a hypersphere using sampling
    N: Number of random points
    D: Number of dimensions
    R: Radius of hypersphere
    """
    vol=0.
    x=[0. for i in range(D-1)]
    for _ in range(N):
        for i in range(D-1):
            x[i]=random.uniform(-R,R)
        vol += f(x)
    return vol/N*(2*R)**(D-1)

def nball(R=1,D=3):
    """
    Returns volume of hypersphere
    """
    return (np.pi*R*R)**(D/2)/(gamma(D/2+1))

def fact(n):
    if n == 0:
        return 1
    else:
        ret = 1
        for i in range(2,n+1):
            ret *= i
    return ret

def fact_rec(n):
    if n == 0:
        return 1
    else:
        return n*fact_rec(n-1)

if __name__ == '__main__':
    import time
    start = time.time()
    n=100
    D=3
    N=1000000
    fp=open("hypersphere.txt","w")
    st = "D\tMCI\ttime\tMCI2\ttime\tTrapez\ttime\tAn\tN"
    fp.write(st+"\n");print(st)
    tr_e=[]
    mc_e=[]
    mc_e2=[]
    n=20
    for D in range(3,10):
        N=100000
        start = time.time()
        mc=mc_nball(N,D)
        end = time.time()
        t_mc=end-start
#        N2=int(N/n)
        start = time.time()
        mc2=mc_nball_sampling(N,D)
        end = time.time()
        t_mc2=end-start
        an=nball(1,D)
#        print(mc, an, "error=",(mc-an) )
        x = [0. for i in range(D)]
#    Area  = 2*d3_trapez(-1,1,f,x,0,N=n)
#   
#    print('Numerical value= ', Area)
#    print('Error= ', (an-Area))
        start = time.time()
        Area2 = dd_trapez(-1,1,f,x,0,n,D-2)
        end = time.time()
        t_trap=end-start
        mcei=abs(mc-an)
        mcei2=abs(mc2-an)
        trei=abs(Area2-an)
        Ni=1./np.sqrt(N)
        N2i=N**(-2/D)
        mc_e.append(mcei)
        mc_e2.append(mcei2)
        tr_e.append(trei)
        st = str(D)+"\t"+str(mcei)+"\t"+str(t_mc)+"\t"+str(mcei2)+"\t"+str(t_mc2)+"\t"+str(trei)+"\t"+str(t_trap)+"\t"+str(an)+"\t"+str(N)
#        print(abs(mc-an),"\t",abs(Area2-an),"\t", an,"\t",1./np.sqrt(N),"\t",N**(-2/D))
        fp.write(st+"\n");print(st)

    fp.close()
    DD= [ i for i in range(3,10)]
    import matplotlib.pyplot as plt
    plt.plot(DD,mc_e,label="MC")
    plt.plot(DD,mc_e2,label="MC-Imp")
    plt.plot(DD,tr_e,label="Trapezoidal")
    plt.grid()
    plt.legend(loc='best')
    plt.show()
    
