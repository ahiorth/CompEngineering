import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt

def OLS(x, y): 
    # returns regression coefficients
    # in ordinary least square
    # x: observations
    # y: response
    # R^2: R-squared
    n = np.size(x) # number of data points 
  
    # mean of x and y vector 
    m_x, m_y = np.mean(x), np.mean(y) 
  
    # calculating cross-deviation and deviation about x 
    SS_xy = np.sum(y*x) - n*m_y*m_x 
    SS_xx = np.sum(x*x) - n*m_x*m_x 
  
    # calculating regression coefficients 
    b_1 = SS_xy / SS_xx 
    b_0 = m_y - b_1*m_x

    #R^2
    y_pred = b_0 + b_1*x
    S_yy   = np.sum(y*y) - n*m_y*m_y
    y_res  = y-y_pred  
    S_res  = np.sum(y_res*y_res)
  
    return(b_0, b_1,1-S_res/S_yy) 

def plot_regression_line(x, y, b): 
    # plotting the actual points as scatter plot 
    plt.scatter(x, y, color = "m", 
               marker = "o", s = 30) 
  
    # predicted response vector 
    y_pred = b[0] + b[1]*x
  
    # plotting the regression line
    if(len(b)>2):
        plt.plot(x, y_pred, color = "g", label = "R-squared = {0:.3f}".format(b[2]))
        plt.legend()
    else:
        plt.plot(x, y_pred, color = "g")
  
    # putting labels 
    plt.xlabel('x') 
    plt.ylabel('y') 
  
    # function to show plot 
    plt.show() 

def OLSM(x, y): 
    # returns regression coefficients
    # in ordinary least square using solve function
    # x: observations
    # y: response

    XT = np.array([np.ones(len(x)),x],float)
    X  = np.transpose(XT)
    B = np.dot(XT,X)
    C = np.dot(XT,y)
    return solve(B,C)
  
def main(): 
    # observations 
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) 
    y = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12]) 
  
    # estimating coefficients 
    b = OLS(x, y) 
    print("Estimated coefficients:\nb_0 = {}  \n nb_1 = {}".format(b[0], b[1]))
    print("R-squared ", b[2])

    # plotting regression line 
    plot_regression_line(x, y, b)

    # estimating coefficients 
    b = OLSM(x, y) 
    print("Estimated coefficients:\nb_0 = {}  \n nb_1 = {}".format(b[0], b[1]))

    # plotting regression line 
    plot_regression_line(x, y, b)


    
  
if __name__ == "__main__": 
    main() 
