import matplotlib.pyplot as plt
import numpy as np

#Maclaurin Serie of sin(x) at the power n
def mac_sin(x,n):
    f = 0.
    for i in range(0,n+1):
        p  = 2*i+1
        f += (-1)**i*pow(x,p)/np.math.factorial(p)
    return f

x = np.arange(-2*np.pi,2*np.pi,0.001)
f = np.sin(x)
# map calls the function mac_sin with the
# next arguments given
P=[]
P.append(list(map(mac_sin,x,[0]*len(x))))
P.append(list(map(mac_sin,x,[1]*len(x))))
P.append(list(map(mac_sin,x,[2]*len(x))))
P.append(list(map(mac_sin,x,[3]*len(x))))
P.append(list(map(mac_sin,x,[4]*len(x))))

fig = plt.figure(dpi=150)

st = ['-.','--',':','-.','--']
ll = ['$P_1$','$P_3$','$P_5$','$P_7$','$P_9$']

for i in range(0,5):
    plt.plot(x, P[i], st[i], label=ll[i])
plt.ylim(-1.1,1.5)
plt.plot(x, f, '-', label='$\sin (x)$')
plt.grid()
# Fancy legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          ncol=6, fancybox=True, shadow=True)
# Save the plot in a file
plt.savefig('mac_sin.png', bbox_inches='tight',transparent=True)
plt.show()


