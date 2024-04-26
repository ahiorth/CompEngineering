#%%
# Import the packages we plan to use
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import newton_rapson as nr

df = pd.read_csv('../data/corona_data.dat', sep='\t')

def get_corona_data(location, data_file='../data/corona_data.dat'):
    """
    Extracts COVID-19 data for a specific location.

    :param location: The name of the location (case-sensitive).
    :param data_file: Path to file holding the COVID-19 data.
                      It is expected that columns of data are
                      separated by tabs, and that there is a
                      column called "LOCATION" with names of
                      each country, region, etc.
    :return: A pandas DataFrame with COVID-19 data for the
             input location.
    """
    df = pd.read_csv(data_file, sep='\t')
    try:
        df = df[df['LOCATION'] == location]
    except:
        print(f'Could not find data for location {location}...')
        return None
    return df

def calc_SI_model_old(t, S0, I0, beta):
    """
    :param t: An array of times.
    :param S0: The initial number of susceptible people.
    :param I0: The initial number of infected people.
    :param beta: The disease transmission rate parameter.
    :return: A tuple of arrays holding S(t) and I(t).
    """
    I = (S0+I0)/(1.0 + S0*np.exp(-beta*t)/I0)
    S = S0 + I0 - I
    return S, I

# We replace the old function "calc_SI_model" by this:
def calc_SI_model(t, S0, I0, beta, lam):
    """
    :param t: An array of times.
    :param S0: The initial number of susceptible people.
    :param I0: The initial number of infected people.
    :param beta: The disease transmission rate parameter.
    :param lam: Decline parameter for exponential decline
                of beta (default: 0.0).
    :return: A tuple of arrays holding S(t) and I(t).
    """
    bt = (beta/lam)*(1.0 - np.exp(-lam*t)) if lam > 0 else beta*t
    I = (S0+I0)/(1.0 + S0*np.exp(-bt)/I0)
    S = S0 + I0 - I
    return S, I

def SI_db(beta,t,S0,I0):
    """
    calculates the derivative of the SI model with respect to beta
    """
    n=1+S0/I0*np.exp(-beta*t)
    return t*(S0+I0)*S0/I0*np.exp(-beta*t)/n/n

def SI_db_num(x,t,I0=1,N=10000):
    beta=x[0]
    l=x[1]
    dh=1e-5 # step size
    S0=N-I0
    SI=calc_SI_model(t,S0,I0,beta,l)[0]
    SI_db=calc_SI_model(t,S0,I0,beta+dh,l)[0]
    SI_dn=calc_SI_model(t,S0,I0,beta,l+dh)[0]
    return (SI_db-SI)/dh,(SI_dn-SI)/dh
    


def plot_confirmed_cases(location, data_file='../data/corona_data.dat'):
    """
    Plots the number of confirmed COVID-19 cases for a specific
    location.

    :param location: The name of the location (case-sensitive).
    :param data_file: Path to file holding the COVID-19 data.
                      It is expected that columns of data are
                      separated by tabs, and that there is a
                      column called "LOCATION" with names of
                      each country, region, etc.
    :return: A matplotlib.pyplot.figure object.
    """
    # Get data
    df = get_corona_data(location, data_file)
    time = df['ELAPSED_TIME_SINCE_OUTBREAK'].to_numpy()
    confirmed = df['CONFIRMED'].to_numpy()

    # Make plot
    fig, ax = plt.subplots()
    ax.set_title(location)
    ax.grid()
    ax.set_xlabel('Time since initial outbreak (days)')
    ax.set_ylabel('Number of confirmed cases')
    ax.scatter(time, confirmed, color='black')
    return fig

def compare_confirmed_cases_with_model(location, S0, I0, beta,lam,
                                       data_file='../data/corona_data.dat'):
    """
    Plots the number of confirmed COVID-19 cases for a specific
    location.

    :param location: The name of the location (case-sensitive).
    :param S0: The initial number of susceptibles in the model.
    :param I0: The initial number of infected people in the model.
    :param beta: The model disease transmission rate parameter.
    :param data_file: Path to file holding the COVID-19 data.
                      It is expected that columns of data are
                      separated by tabs, and that there is a
                      column called "LOCATION" with names of
                      each country, region, etc.
    :return: A matplotlib.pyplot.figure object.
    """
    # Calculate S(t) and I(t) from the analytical solution
    t = np.linspace(0, 250, 251)
    St, It = calc_SI_model(t, S0, I0, beta,lam)

    # Plot the data, and return the data
    fig = plot_confirmed_cases(location, data_file)
    # Add modelled I(t) to the same figure
    ax = fig.axes[0]
    ax.plot(t, It)
    return fig



def least_square(beta,location,data_file='../data/corona_data.dat'):
    df = get_corona_data(location, data_file)
    time = df['ELAPSED_TIME_SINCE_OUTBREAK'].to_numpy()
    confirmed = df['CONFIRMED'].to_numpy()
    N = df['CONFIRMED'].iloc[-1]
    St, It = calc_SI_model(time, N-1, 1, beta)

    lsq=np.sum((confirmed-It)**2)

    return lsq



def dleast_square(beta,location='Hubei',data_file='../data/corona_data.dat'):
    df = get_corona_data(location, data_file)
    time = df['ELAPSED_TIME_SINCE_OUTBREAK'].to_numpy()
    confirmed = df['CONFIRMED'].to_numpy()
    N = df['CONFIRMED'].iloc[-1]
    St, It = calc_SI_model(time, N-1, 1, beta)
    r=(confirmed-It)
    dfb=SI_db(beta,time,N-1,1)
    return 2*np.sum(r*dfb)

def dleast_square_num(x,location='Hubei',data_file='../data/corona_data.dat'):
    beta=x[0]
    l=x[1]
    df = get_corona_data(location, data_file)
    time = df['ELAPSED_TIME_SINCE_OUTBREAK'].to_numpy()
    confirmed = df['CONFIRMED'].to_numpy()
    N = df['CONFIRMED'].iloc[-1]
    N=50e6
    St, It = calc_SI_model(time, N-1, 1, beta,l)
    r=(confirmed-It)
    dfb,dfn=SI_db_num(x,time,N=N)
    return np.array([2*np.sum(r*dfb),2*np.sum(r*dfn)])/1e5

def gradient_descent(x,df, *args, g=.001, prec=1e-8,MAXIT=10,**kwargs):
    '''Minimize f(x) by gradient descent.
    x   : starting point 
    df  : derivative of f(x)
    g   : learning rate
    prec: desired precision
    
    Returns x when it is closer than eps to the root, 
    unless MAXIT are not exceeded
    '''
    x_old = x
    for n in range(MAXIT):
        x_new = x_old - g*df(x_old,*args,**kwargs)   
        print(x_new)    
        if(abs(np.max(x_new-x_old))<prec):
            print('Found solution:', x_new, 
                  ', after:', n, 'iterations.' )
            return x_new
        x_old=x_new
    print('Max number of iterations: ', MAXIT, ' reached.') 
    print('Try to increase MAXIT or decrease prec')
    print('Returning best guess ',x_new)
    return x_new
def Jacobian(x,f,*args,dx=1e-5,**kwargs):
    N=len(x)
    x0=np.copy(x)
    f0=f(x,*args,**kwargs)
    J=np.zeros(shape=(N,N))
    for j in range(N):
        x[j] = x[j] +  dx
        for i in range(N):   
            J[i][j] = (f(x,*args,**kwargs)[i]-f0[i])/dx
        x[j] = x[j] -  dx
    return J




def newton_rapson(x,f,*args,J=None, jacobian=False, prec=1e-8,MAXIT=5,**kwargs):
    '''Approximate solution of f(x)=0 by Newtons method.
    The derivative of the function is calculated numerically
    f   : f(x)=0.
    J   : Jacobian
    x   : starting point  
    eps : desired precision
    
    Returns x when it is closer than eps to the root, 
    unless MAX_ITERATIONS are not exceeded
    '''
    MAX_ITERATIONS=MAXIT
    x_old = np.copy(x)
    for n in range(MAX_ITERATIONS):
        if not jacobian:
            J=Jacobian(x_old,f,*args,**kwargs)
            print(J)
            print(x_old)
        z=np.linalg.solve(J,-f(x_old,*args,**kwargs))
        x_new=x_old+z
        if(np.sum(abs(x_new-x_old))<prec):
            print('Found solution:', x_new, 
                  ', after:', n, 'iterations.' )
            return x_new
        x_old=np.copy(x_new)
        print(x_old)
    print('Max number of iterations: ', MAXIT, ' reached.') 
    print('Try to increase MAXIT or decrease prec')
    print('Returning best guess ', x_new,' value of function is: ', f(x_new,*args,**kwargs))
    return x_new
loc='Hubei'
df = get_corona_data(loc)
N = df['CONFIRMED'].iloc[-1]
print(N)
x0=np.array([.5,.05])
print(dleast_square_num(x0))
x0[0]=x0[0]+1e-5
print(dleast_square_num(x0))

x=newton_rapson(x0,dleast_square_num, location=loc)
fig_hubei_model = compare_confirmed_cases_with_model(loc, N-1, 1, x[0],x[1])

gradient_descent(x0,dleast_square_num, g=.1, prec=1e-8,MAXIT=10, location=loc)
"""
plt.close()
beta =np.arange(0.1,4,0.1)
lsq=[]
dlsq=[]
dlsq_n=[]

for b in beta:
    lsq.append(least_square(b,loc))
    dlsq.append(dleast_square(b,loc))
    db,dn=dleast_square_num(b,loc)
    dlsq_n.append(db)
    

plt.ylim(-0.1,.1)
plt.plot(beta,lsq/np.max(lsq))
plt.grid()
plt.plot(beta,dlsq/np.max(dlsq))
plt.plot(beta,dlsq_n/np.max(dlsq_n),'^')

plt.show()

"""
# %%
