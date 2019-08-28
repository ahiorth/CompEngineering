import numpy as np
import matplotlib.pyplot as plt

B = np.loadtxt("draugen.txt")

Year = B[:,0]
Month = B[:,1]
OilProd = B[:,2]

#Assume 30 days in each month and 365 in year
Year = Year + Month*30/365
ProdStart = Year[0]

#Year now starts at 0
Year = Year-ProdStart

#Calculate the cumulative oil production
CumOilProd = np.cumsum(OilProd)

fig, ax1 = plt.subplots()

plt.title('Draugen production profile')
ax1.set_ylabel(r'MSm$^3$/month')
ax1.set_xlabel('Years of production')

ax1.plot(Year,OilProd, 'b--o')
#ax1.plot(OilProd, CumOilProd, 'b--o')
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel(r'Cumulative production [MSm$^3$]')
ax2.plot(Year,CumOilProd, 'r--o')
plt.savefig('../fig-decline/draugen.png', bbox_inches='tight',transparent=True)
plt.show()
plt.close()

from scipy.optimize import curve_fit

def exp_decline(x,A,D):
    return A*np.exp(-D*x)

# only choose data from the decline phase (i.e. after approx. 8 years)
T0 = 8
# extract indexes 
ind = Year > T0;
# cooresponding X and Y-value
NewY = Year[ind]-T0; #important to start at 0
NewP = OilProd[ind];

popt, pcov = curve_fit(exp_decline, NewY, NewP)

model = exp_decline(NewY,popt[0],popt[1])

#plt.clf()
fig, ax1 = plt.subplots()

plt.title('Draugen production profile')
ax1.set_ylabel(r'MSm$^3$/month')
ax1.set_xlabel('Years of production')

ax1.plot(Year,OilProd, 'b--o')
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel(r'Cumulative production [MSm$^3$]')
ax2.plot(Year,CumOilProd, 'r--o')
ax1.plot(NewY+T0,model, 'k-',lw='2',label="model")
ax1.legend(loc=(0.75,0.75))
plt.savefig('../fig-decline/draugen_fit.png', bbox_inches='tight'
            ,transparent=True)
plt.show()




