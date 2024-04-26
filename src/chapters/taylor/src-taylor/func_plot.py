#%%
import matplotlib.pyplot as plt
import numpy as np

x = []
x.append(np.arange(-np.pi,np.pi,1))
x.append(np.arange(-np.pi,np.pi,0.5))
x.append(np.arange(-np.pi,np.pi,0.1))
#Small spacing to evaluate the "true" function
x.append(np.arange(-np.pi,np.pi,0.001))

f = []
for i in range(0,4):
    f.append(np.sin(x[i]))


fig = plt.figure(dpi=150)
fig.subplots_adjust(hspace=0.4, wspace=0.4)
plt.subplot(1,2,1)
st = ['-o','-x','-*','-']
ll = ['$\Delta x=1$','$\Delta x=0.5$','$\Delta x=0.1$','$\sin x$']

for i in range(0,4):
    plt.plot(x[i], f[i], st[i])

plt.grid()

# Next plot side by side
plt.subplot(1,2,2)
plt.xlim(-2.2,-1)
plt.ylim(-1.2,-0.75)

for i in range(0,4):
    plt.plot(x[i], f[i], st[i], label = ll[i])
    
plt.grid()
plt.legend(loc='upper center', bbox_to_anchor=(-0.3, -0.05),
          ncol=4, fancybox=True, shadow=True)
# Save the plot in a file
plt.savefig('func_plot.png', bbox_inches='tight',transparent=True)
plt.show()



# %%
