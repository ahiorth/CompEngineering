import numpy as np 
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
print(pathlib.Path.cwd())
folder = pathlib.Path.cwd().parent.joinpath('data')
filename = folder.joinpath('field_production_gross_monthly.xls')
df = pd.read_excel(filename)
columns = df.columns


fields = ['DRAUGEN']
#for field in fields:
#for i, field in enumerate(fields):
#    #field = fields[i]
for field in fields:
    df2 = df[df[df.columns[0]] == field]
    Year = df2['Year']
    Month = df2['Month']
    OilProd=df2[columns[3]]
    
    #Assume 30 days in each month and 365 in year
    Year = Year + Month*30/365
    ProdStart = Year.iloc[0]

    #Year now starts at 0
    Year = Year-ProdStart
    #print(Year)

    #Calculate the cumulative oil production
    CumOilProd = np.cumsum(OilProd)

    fig, ax1 = plt.subplots()
    plt.scatter(Year, OilProd)

    ax1.set_ylabel(r'MSm$^3$/month')
    ax1.set_xlabel('Years of production')

    ax1.plot(Year,OilProd, 'b--o')
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




