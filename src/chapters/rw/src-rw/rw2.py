#%%
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
#Random walk in 1 dimension
N=1000
x=np.random.uniform(-0.5,0.5,size=N)

path=np.cumsum(x)

plt.plot(path)
plt.grid()
#%%
def rw1d(N):
    x=np.random.uniform(-0.5,0.5,size=N)
    return np.cumsum(x)

Ns=[100,1000,10000,1000000]
d=[]
for N in Ns:
    path=rw1d(N)
    d.append(np.std(path)**2)

plt.plot(Ns,d,'*')
plt.xscale('log')
plt.yscale('log')
# %%
# Random Walk 2Dimensions
N=10
u=np.array([[-1,0],[1,0],[0,1],[0,-1]])
x=np.random.randint(0,4,size=N)
path2d=u[x].cumsum(0)

plt.plot(path2d[:,0],path2d[:,1])
plt.grid()
np.sum(np.logical_and(path2d[:,0]==0,path2d[:,1]==0))
#%%

# %%
max=np.max(np.abs(path2d))
fig, ax = plt.subplots(1, 1, figsize = (6, 6))
plt.grid()
ax.set_xlim([-max,max]) # fix the x axis
ax.set_ylim([-max, max]) # fix the y axis

camera = Camera(fig)

for i in range(N):
    ax.plot(path2d[:i,0], path2d[:i,1],c='b')
    camera.snap()
animation=camera.animate()
animation.save('rw.gif')
# %%
N=10000
u=np.array([[1,0,0],[0,1,0],[0,0,1],
            [-1,0,0],[0,-1,0],[0,0,-1]])
x=np.random.randint(0,6,size=N)
path3d=u[x].cumsum(0)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(path3d[:,0],path3d[:,1],path3d[:,2])
np.sum(np.logical_and(path3d[:,0]==0,path3d[:,1]==0,path3d[:,2]==0))

# %%
