import numpy as np 
import pandas as pd
import pathlib
import matplotlib.pyplot as plt

# A function to return a dataframe containin only a specific field
def df_field(name,datafile='field_production_gross_monthly.xls',col=0):
    folder = pathlib.Path.cwd().parent.joinpath('data')
    filename = folder.joinpath(datafile)
    df = pd.read_excel(filename)
    columns = df.columns
    return columns, df[df[df.columns[col]] == name]

def prod_data(name):
    columns, df2 = df_field(name)
    Year = df2['Year']
    Month = df2['Month']
    OilProd=df2[columns[3]]
    #Assume 30 days in each month and 365 in year
    Year = Year + Month*30/365
    return Year, OilProd

def well_data(name, datafile='wellbore_development_all.xls'):
    columns, df2 = df_field(name,datafile,col=14)
    Year = df2[columns[32]]
    Nowells=[]
    NewY=[]
    wells=1
    y_old=0
    for y in Year:
        try:
            index = NewY.index(y)
            Nowells[index] += 1
        except:
            NewY.append(y)
            Nowells.append(1.)
    NewY,Nowells = zip(*sorted(zip(NewY, Nowells)))
    
    return NewY, np.cumsum(Nowells)

name='OSEBERG'
#columns, df2 = df_field(name,datafile='wellbore_development_all.xls',col=14)
#print(columns)

Ny,Nw=well_data(name)
    
#print(df_field('OSEBERG'))
      

def plot_prod_data(name,well=False):
    Year,OilProd=prod_data(name)
    fig, ax1 = plt.subplots()
    plt.title(name)

    ax1.set_ylabel(r'MSm$^3$/month')
    ax1.set_xlabel('Years of production')


    lns=ax1.plot(Year,OilProd, 'b--o', label='Oil Production')
    if(well):
        Yw,Nw=well_data(name)
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel(r'Number of Wells')
        lns2=ax2.plot(Yw,Nw, 'r--o', label='No wells')
        lns =  lns+lns2
    ax1.set_xlim(min(Year),max(Year))
    # added these three lines
    
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)
 #   plt.grid()
    plt.show()
    plt.close()

def plot_cum_data(name):
    Year,OilProd=prod_data(name)
    fig, ax1 = plt.subplots()
    plt.title(name)

    ax1.set_ylabel(r'Cummulative production MSm$^3$')
    ax1.set_xlabel('Number of wells')

    Year,OilProd=prod_data(name)
    Yw,Nw=well_data(name)

    Nw = np.interp(Year,Yw,Nw)
    CumOil=np.cumsum(OilProd)

    ax1.plot(Nw,CumOil, 'r--o')

    plt.grid()
    plt.show()
    plt.close()
    
plot_prod_data(name,True)
plot_cum_data(name)

name = 'DRAUGEN'
Year,OilProd=prod_data(name)

from scipy.optimize import curve_fit

def exp_decline(x,A,D):
    return A*np.exp(-D*x)

#start at 0
ProdStart = Year.iloc[0]
Year = Year-ProdStart
# only choose data from the decline phase (i.e. after approx. 8 years)
T0 = 8
# extract indexes 
ind = Year > T0;
# cooresponding X and Y-value
NewY = Year[ind]-T0; #important to start at 0
NewP = OilProd[ind];

CumOilProd = np.cumsum(OilProd)
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
plt.show()




