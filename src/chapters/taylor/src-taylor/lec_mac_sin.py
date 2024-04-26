import matplotlib.pyplot as plt
import numpy as np

#Maclaurin Serie of sin(x) at the power n
def mac_sin(x,n):
    f = 0.
    for i in range(0,n+1):
        p  = 2*i+1
        f += (-1)**i*pow(x,p)/np.math.factorial(p)
    return f

def mac_log(x,n):
    f=0.
    for i in range(0,n+1):
        f += (-1)**(i)*pow(x,i+1)/(i+1)
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
LL2 = ['$X$','$x-\frac{1}{3!}x^3$','$x-\frac{1}{3!}x^3+\frac{1}{5!}x^5$',
       '$x-\frac{1}{3!}x^3+\frac{1}{5!}x^5-\frac{1}{7!}x^7$-']

plt.ylim(-1.1,1.5)
plt.plot(x, f, '-', label='$\sin (x)$')
plt.grid()
plt.savefig('mac_sin.png', bbox_inches='tight',transparent=True)
# Fancy legend
#plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#          ncol=6, fancybox=True, shadow=True)
# Save the plot in a file

for i in range(0,4):
    plt.plot(x, P[i], st[i], label=ll[i])
    plt.savefig('mac_sin'+str(i)+'.png', bbox_inches='tight',transparent=True)
plt.show()

plt.close()
fig = plt.figure(dpi=150)
x = np.arange(-2,3,0.001)
P=[]
P.append(list(map(mac_log,x,[0]*len(x))))
P.append(list(map(mac_log,x,[1]*len(x))))
P.append(list(map(mac_log,x,[2]*len(x))))
P.append(list(map(mac_log,x,[3]*len(x))))
P.append(list(map(mac_log,x,[4]*len(x))))

x2 = np.arange(-0.9,4,0.001)
f = np.log(x2+1)
plt.ylim(-3,3)
plt.xlim(-2,4)
plt.plot(x2, f, '-', label='$\log (x+1)$')
plt.grid()
plt.savefig('mac_log.png', bbox_inches='tight',transparent=True)
# Fancy legend
#plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#          ncol=6, fancybox=True, shadow=True)
# Save the plot in a file

for i in range(0,5):
    plt.plot(x, P[i], st[i], label=ll[i])
    plt.savefig('mac_log'+str(i)+'.png', bbox_inches='tight',transparent=True)
plt.show()
