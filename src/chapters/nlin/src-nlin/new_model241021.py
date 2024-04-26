#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 10:01:32 2019

@author: ah
"""
#%%
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gammainc
from scipy.optimize import curve_fit
from scipy import stats
import codecs
from pathlib import Path, PurePosixPath
import os
import itertools

print(pathlib.Path.cwd())
global YY_,WW_,NN_

def df_npd(excel_file='field_production_gross_monthly.xlsx', folder = ['data','NCS'],index_col=None):
    """
    returnd a data frame given excel file in 
    the data filelocated in ../data folder
    """
    dd = pathlib.Path.cwd().parent
    for fol in folder:
        dd = dd / fol
    filename = dd.joinpath(excel_file)
    df = pd.read_excel(filename,index_col=index_col)
    return df

def get_production_data(df,fname):
    """ 
    returns production data, given data frame
    and field name 
    """
    df = df[df[df.columns[0]] == fname]
    Year    = df[df.columns[1]]
    Month   = df[df.columns[2]]
    Oe = df[df.columns[6]] # Oil equivalents
    O  = df[df.columns[3]] # Oil 
    G  = df[df.columns[4]] # Gas 
    #Assume 30 days in each month and 365 in year
    Year    = Year + Month*30/365
    return Year, Oe,O,G

def get_total_resources(fname):
    """ 
    returns estimated HC volemes, given data frame
    and field name(s) 
    """
    df=df_npd(excel_file='field_reserves.xlsx',index_col=0)
    df=df.loc[fname]
    O  = np.array(df[df.columns[4]])
    
    return O
def get_well_data(df,fname):
    """ 
    returns well data, given data frame, and name of field
    """
    df=df[df[df.columns[14]] == fname]
 #   year = df['Completed year']  # alternatively: fetch by index (32)
    grouped_data = df.groupby('Completed year')

    years = []
    well_count = []
    total_well_count = 0
    # Store number of wells at the end of a given year:
    for yr, dff in grouped_data:
        if yr > 0:
            n_prod = np.count_nonzero(dff['Purpose']=='PRODUCTION')
            #n_inj = np.count_nonzero(dff['Purpose']=='INJECTION')
            #n_obs = np.count_nonzero(dff['Purpose']=='OBSERVATION')
            # etc.
            if(n_prod>0):
                years.append(yr)
                total_well_count = n_prod
                well_count.append(total_well_count)
    return np.array(years),np.array(well_count)

def wellmod(ti,tau,n,shut_down=False):
    """
    ti: time
    tau: time constant
    n : tank model, n=1 exponential model
    """
    l=n*ti/tau
    oprod=1.-gammainc(n,l)
    shut=False
    if(oprod<5e-2 and shut_down ):
        oprod=0.
        shut=True
    return shut,oprod
 

    
def modelfunc(time, tau,q,pr=False,shut_down=False):
    """
    time : array of times to evaluate the model
    tau : time constant of each well
    q : average well rate
    pr: additional print information
    """
    global YY_ # Year at which a well was drilled
    global WW_ # Number of wells that year
    global NN_ # tanke model NN_ = 1 exponential model
    F=[]
    for ti in time:
#remove all wells started later than time ti
        YN = list(filter(lambda a: a <= ti, YY_))
#          print("ti=",ti,"YN=",YN)
        Fi=0.
#       nw is the well interference 
        nw=sum(WW_[:len(YN)]) 
        if(pr): 
            print(nw)
        taui = tau/nw
        for idx, y in enumerate(YN):
            shut,qw=wellmod(ti-y,taui,NN_,shut_down=shut_down)

            Fi += WW_[idx]*qw
        F.append(Fi*q)
    return F

def infill_well(time, Ti,tau,q,pr=False,shut_down=True):
    """
    time : array of times to evaluate the model
    Ti   : time at which new infill well was drilled
    tau : time constant of each well
    q : average well rate
    pr: additional print information
    """
    global YY_ # Year at which a well was drilled
    global WW_ # Number of wells that year
    global NN_ # tanke model NN_ = 1 exponential model
    F=[]
    for ti in time:
#remove all wells started later than time ti
        YN = list(filter(lambda a: a <= ti, YY_))
#          print("ti=",ti,"YN=",YN)
#       nw is the well interference 
        nw=sum(WW_[:len(YN)]) 
        if(pr): 
            print(nw)
        taui = tau/nw
        if(ti<Ti):
            F.append(0.)
        else:
            shut,qw=wellmod(ti-Ti,taui,NN_,shut_down=shut_down)
            F.append(q*qw)
    return F

def find_model_params(fname,df_prod,df_well,part=False):
    """
    fits observed production and well data to model
    fname   : field name
    df_prod : data frame production
    df_well : data frame wells
    returns fitted values
    """
    global YY_ # Year at which a well was drilled
    global WW_ # Number of wells that year
    global NN_ # tank model NN_ = 1 exponential model
    yp,o,oil,gas=get_production_data(df_prod,fname)
    if(part): # only use some of the data to fit oil production
        o=o.values
        yp=yp.values
        y_ind=np.where(o==max(o))[0][0]
        y_ind=len(yp)//2
        ymmi=yp[y_ind]
        val=yp<=ymmi
        o=o[val]
        yp=yp[val]
    print(fname, ' at time', max(yp))
    if(len(yp)==0):
    # No production data
        return [-1,-1]
    YY_,WW_=get_well_data(df_well,fname)
    if(fname =='SKARV'):
        YY_ += 2
    if(len(WW_)==0):
#   No well data
        return [-3,-3]
    try:
        popt, pcov = curve_fit(modelfunc, yp, o, p0=(800,1))
    except:
#   curve_fit did not find a solution
        print(yp,o)
        return [-2,-2]
    return popt

def plot_model_prod_data(fname,df_prod,tau=-1,q=-1,well_fact=1,dpi=100,show=True,o_g=False):
    """
    fname : field name
    df_prod : data frame from NPD
    tau : time constant in model,  dimension year
    q : average well production in model, dimension production per month
    well_fact : if well_fact = 2, we double number of wells after half time production
    Must be called directly after find_model_parameters
    """
    global YY_ # Year at which a well was drilled
    global WW_ # Number of wells that year
    global NN_ # tanke model NN_ = 1 exponential model
# --- following code is to test out scenarios ----
# if well_fact = 2, we double number of wells after half time production    
    w1 = np.ones(len(WW_))
    w1[len(w1)//2:]=w1[len(w1)//2:]*well_fact
    WW_=WW_*w1
# make sure that there is only whole wells
    WW_=np.round(WW_)
# ------------------------------------------------
    lw=2
    Y,Oe,oil,gas = get_production_data(df_prod_,fname)
    if(tau>0):
        O   = modelfunc(Y, tau,q)
        if(fname == 'SINDRE'):
            print('**',np.array(Y),np.array(O))
            print(YY_,WW_)
    
    WWc = np.cumsum(WW_)

    fig, ax1 = plt.subplots()
    xmin = min(Y); xm = max(Y); 
    ymax= max(Oe); ymin=0.
    y2max=max(WWc); y2min=0.

    name_p = fname 
    if(tau>0):
        name_p += '\n($\\tau$=' + str(format(tau,'.3f'))+ r' year'
        name_p += ', q=' + str(format(q*12,'.3f')) + r'$\cdot$10$^6$Sm$^3$/year )'
    else:
        name_p += '\n'
    plt.title(name_p)
    ax1.set_ylabel(r'Production rate  [10$^6$Sm$^3$/month]')
    
    ax1.grid(b=True, which='major', color='k', linestyle='--')
    ax1.minorticks_on()
    ax1.set_xlabel('Years')
    ax1.set_xlim(xmin-2,xm)
    ax1.set_ylim(ymin,ymax*1.2)
    
    ax1.plot(Y, Oe, '-r', lw=lw, label='Oil Equivalents')
    if o_g:
        ax1.plot(Y, oil, '-y', lw=lw, label='Oil')
        ax1.plot(Y, gas, '-g', lw=lw, label='Gas')
    ax2 = ax1.twinx()
    ax2.set_ylabel(r'Number of Wells')
    ax2.set_ylim(y2min,y2max*1.4)
    
    if(tau>0):
        ax1.plot(Y, O, '--b', lw=lw, label='Model')
    
    wp = ':k'

    ax2.plot(YY_, WWc, wp, lw=lw+1, label='No Wells')
    # just to get legend
    ax1.plot(np.nan, wp, lw=lw+1, label = 'No Wells')
    ax1.legend(loc=1,ncol=2)
    plt.minorticks_on()
    new_name = fname
    new_name = new_name.replace(" ", "_")
    new_name = new_name.replace("Å", "AA")
    new_name = new_name.replace("Ø", "O")
    new_name = new_name + 'NN_' + str(NN_)
    new_name = new_name + 'Wf_' + str(well_fact)
    if(tau<0):
        new_name = new_name + '_XX'
    dd = pathlib.Path.cwd().parent
    dd = dd / 'PNG'
    filenm  = new_name + '.png'
    filenm  = dd.joinpath(filenm)  
    print(filenm)
    plt.savefig(filenm, bbox_inches='tight',transparent=True,dpi=dpi)
    #plt.grid(b=True, which='major', color='k', linestyle='--')
    if(show):
        plt.show()
    plt.close()
    if(tau>0):
        Amodel=abs(np.trapz(O,Y))
    else:
        Amodel=0.
    Afield=abs(np.trapz(Oe,Y))
    Afact=(Amodel-Afield)/Afield
#    print('Amodel= ', Amodel, 'Afield= ', Afield, 'Afact = ', Afact) 
    return new_name, Amodel*12, Afield*12, Afact, sum(WW_)
    
#gen_plot2tex('field.tex',1e5,0.1)
def combine_img(dd2,no_row=3,no_col=6):
    command = 'doconce combine_images png -' +str(no_col) +str(' ')
    command = 'ubuntu run /home/ah/anaconda3/bin/doconce combine_images png -' +str(no_col) +str(' ')
    
    
    dd = dd2.copy()
    iter=0
    while(len(dd)>=no_row*no_col):
        files =""
        outfname= "combined"+str(iter)+".png"
        outf = '../PNG/'
        outf = outf+outfname
        for i in range(no_row*no_col):
            files += str('../PNG/')+str(dd.pop(0)) + " "
        os.system(command + files + str(outf))
        iter += 1
        print('11'+ command + files + str(outf))
    if(len(dd)>0):
        outfname= "combined"+str(iter)+".png"
        outf = '../PNG/'
        outf = outf+outfname
        files = [str('../PNG/'+f+'.png') for f in dd]
        files = " ".join(files)
        print('22'+command + str(files) + ' ' + str(outf))
        os.system(command + str(files) + ' ' + str(outf))

def fit_model(field_names,df_prod_,df_well_,well_fact=1,dpi=100,NO=[1],fit_res_f='model_fit.dat',fit_res_f2='model_fit2.dat',show=True,o_g=False):
    global NN_
    fitf= codecs.open(fit_res_f,'w','utf-8')
    fitf2= codecs.open(fit_res_f2,'w','utf-8') 
    fitf.write('FieldName')
    fitf2.write('FieldName')
    for n in NO:
        fitf.write('\ttau_'+str(n)+'\tq_'+str(n))
        fitf2.write('\tAmod_'+str(n)+'\tAField_'+str(n)+'\tFrac'+'\tNoWells')
    fitf.write('\n')
    fitf2.write('\n')
    
    names=[]
    bad_fit=[]
    for idx,fn in enumerate(field_names):
        namei = []
#     fn3=modelprod_pl(fn,1e5,0.1)
        fitf.write(fn)
        fitf2.write(fn)
        print(fn)
#     namei.append(fn3)
        for n in NO:
            NN_=n
            result=find_model_params(fn,df_prod_,df_well_)
            if(result[0]==-1):
                print('No production data for ' + str(fn))
                fitf.write('\t-1\t-1')
                fitf2.write('\t0\t0\t0\t0')
                break
            elif(result[0]==-2):
                print('Curve fit failed for ' + str(fn))
                fitf.write('\t-2\t-2')
                fitf2.write('\t0\t0\t0\t0')
            elif(result[0]==-3):
                print('No production data for ' + str(fn))
                fitf.write('\t-3\t-3')
                fitf2.write('\t0\t0\t0\t0')
                break
            fitf.write('\t'+str(result[0])+'\t'+str(result[1]))
            fn2, Wm, Wf, fr,totW=plot_model_prod_data(fn,df_prod_, result[0],result[1],well_fact=well_fact,dpi=dpi,show=show,o_g=o_g)
            fitf2.write('\t'+str(Wm)+'\t'+str(Wf)+'\t'+str(fr)+'\t'+str(totW))
            namei.append(fn2)
            print(idx,fn, fn2)
            print('Amodel= ', Wm, 'Afield= ', Wf, 'Afact = ', fr) 
            if(result[0]>3e3):
                bad_fit.append(fn)
        fitf.write('\n')
        fitf2.write('\n')
        names.append(namei)
        
    fitf.close()
    fitf2.close()  
    
    flat_list = [item for sublist in names for item in sublist]
#    combine_img(flat_list,no_row=5,no_col=5)
    return bad_fit,flat_list

def cross_plot(fieldname,fname='model_fit.dat',dpi=600,meth=0):
    Oe  = get_total_resources(field_names)
    a   = np.genfromtxt(fname,delimiter='\t',skip_header=1)
    tau = a[:,1]
    q   = a[:,2]*12 # per year
    if(meth==0):
        Vp   = np.array(tau*q)
        limi = 1000
    else:
        Vp   = tau
        Oe   = Oe/q
        limi=2500
    
    #skip elements that are unphysical
    sk_elem=np.where(Vp>2000)
    Vp=np.delete(Vp,sk_elem)
    Oe=np.array(Oe)
    Oe=np.delete(Oe,sk_elem)
    fieldname=np.array(fieldname)
    print('Delete following fields:', fieldname[sk_elem])
    fieldname=np.delete(fieldname,sk_elem)
    
    slope, intercept, r_value, p_value, std_err= stats.linregress(Oe[Oe<limi],Vp[Oe<limi])
    
    line = slope*Oe+intercept
    print('R-value=',r_value)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.minorticks_on()
#    ax.set_xlim([0,800])
#    ax.set_ylim([0,800])
    if(meth==0):
        ax.set_ylabel(r'Model Estimate [$10^6$Sm$^3$]')
        ax.set_xlabel(r'Original Recoverable Oil Equivalents in Place [$10^6$Sm$^3$]')
    else:
        ax.set_ylabel(r'$\tau$ [year]')
        ax.set_xlabel(r'Original Recoverable Oil Equivalents in Place/q [year]')
#    fig.tight_layout()
    fig.subplots_adjust(bottom=0.57, top=1)
    marker = itertools.cycle(('.',',','o','v','^','<','>','1','2','3','4','8',
                              's','p','P','*','h','H','+','x','X','D','d','|',
                              '_')) 
    color = itertools.cycle(('b','g','r','c','m','y','k'))
    for idx, field in enumerate(fieldname):
        if(Vp[idx]>500000):
            y=0
        else:
            y=Vp[idx]
            ax.scatter(Oe[idx], y, label=field, marker=next(marker),color=next(color), edgecolors='none')
    l1,=ax.plot(Oe,line,'k:')
    if(intercept<0):
        l1_t2=str(format(intercept,'.3f'))
    else:
        l1_t2=r' + '+str(format(intercept,'.3f'))
    l1_t= r'$y$ = ' + str(format(slope,'.3f'))+ r'x '+l1_t2 +r' $, R^2$ = ' + str(format(r_value,'.3f') + r'$^{(*)}$')
    legend1=plt.legend([l1], [l1_t], loc=2)
    plt.title('Norwegian Oil Fields - Comparison Model and Data')
    plt.gca().add_artist(legend1)
    ax.legend(loc='upper center', ncol=6, bbox_to_anchor=(0.5,-0.2),prop={'size': 7})
    ax.grid(True)
 #   ax.set_xscale('log')
    plt.text(-20,-170,r'$^{(*)}$ Troll field is left out')
    plt.savefig('analyseOe_'+str(meth)+'.png', bbox_inches='tight',transparent=True,dpi=dpi)
    plt.show()

def cross_plot2(fieldname,fname='model_fit2.dat',dpi=600):
    a   = np.genfromtxt(fname,delimiter='\t',skip_header=1)
    frac = a[:,3]
    Oe  = get_total_resources(fieldname)
 
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.minorticks_on()
#    ax.set_xlim([0,1800])
#    ax.set_ylim([0,.4])
    ax.set_ylabel(r'$\frac{V_{model}-V_{field}}{V_{field}}$ [$\%$]')
    ax.set_xlabel(r'Fields')
    ax.set_xlabel(r'Original Recoverable Oil Equivalents in Place [$10^6$Sm$^3$]')
#    fig.tight_layout()
    fig.subplots_adjust(bottom=0.57, top=1)
    marker = itertools.cycle(('.',',','o','v','^','<','>','1','2','3','4','8',
                              's','p','P','*','h','H','+','x','X','D','d','|',
                              '_'))
    color = itertools.cycle(('b','g','r','c','m','y','k'))
    for idx, field in enumerate(fieldname):
        y=frac[idx]
        ax.scatter(Oe[idx], y*100, label=field, marker=next(marker), color=next(color), edgecolors='none')
    ax.legend(loc='upper center', ncol=6, bbox_to_anchor=(0.5,-0.2),prop={'size': 7})
    ax.grid(True)
    plt.savefig('analyseA.png', bbox_inches='tight',transparent=True,dpi=dpi)
    plt.show()

def cross_plot3(fieldname,fnames,dpi=600):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.minorticks_on()
#        ax.set_xlim([0,1800])
#        ax.set_ylim([0,.4])
#    ax.set_ylabel(r'Model Recovery')
#    ax.set_xlabel(r'Field Recovery')
    ax.set_xlabel(r'Original Recoverable Oil Equivalents in Place [$10^6$Sm$^3$]')
    ax.set_ylabel(r'Change in Recovery Factor [$\%$]')
#        fig.tight_layout()
    fig.subplots_adjust(bottom=0.57, top=1)
    
    lines = itertools.cycle(('-r',':g', '--b'))
    Oe  = get_total_resources(fieldname)
    for idf,fname in enumerate(fnames):
        marker = itertools.cycle(('.',',','o','v','^','<','>','1','2','3','4','8',
                                  's','p','P','*','h','H','+','x','X','D','d','|',
                                  '_'))
        color = itertools.cycle(('b','g','r','c','m','y','k'))
        a   = np.genfromtxt(fname,delimiter='\t',skip_header=1)
        Wm = a[:,1]
        Wf = a[:,2]
        Nw = a[:,4]
        if(idf==0):
            Wm_base=np.copy(Wm)
            Nw_base=np.copy(Nw)
        
     #   slope, intercept, r_value, p_value, std_err= stats.linregress(Wf,Wm)
     #   line = slope*Wf+intercept
     #   print('R-value=',r_value)
        
        if(idf>0):
            for idx, field in enumerate(fieldname):
                if(Nw_base[idx]>0):
                    tmp=100*(Wm[idx]-Wm_base[idx])/Wm_base[idx]
                    if(idf==1):
                        ax.scatter(Oe[idx], tmp, label=field, marker=next(marker), color=next(color), edgecolors='none')
                    else:
                        ax.scatter(Oe[idx], tmp, marker=next(marker), color=next(color), edgecolors='none')
                    if(abs(tmp)>100):
                        print(field,tmp,Wm[idx],Wm_base[idx],Nw[idx])
#        ax.plot(Wf,line,next(lines))
#        for i in range(len(Wm)):
#            print(fieldname[i],Wm_base[i],Wm[i])
    ax.legend(loc='upper center', ncol=6, bbox_to_anchor=(0.5,-0.2),prop={'size': 7})
    ax.grid(True)
    plt.savefig('analyse_Wells.png', bbox_inches='tight',transparent=True,dpi=dpi)
    plt.show()
    

def cross_plot4(fieldname,fname='model_fit2.dat',dpi=600):
    a   = np.genfromtxt(fname,delimiter='\t',skip_header=1)
    noW = a[:,4]
    sF = a[:,2]
 
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.minorticks_on()
    ax.set_xlim([0,200])
    ax.set_ylim([0,200])
    ax.set_ylabel(r'Number of Wells')
    ax.set_xlabel(r'Original Recoverable Oil Equivalents in Place [$10^6$Sm$^3$]')
#    fig.tight_layout()
    fig.subplots_adjust(bottom=0.57, top=1)
    marker = itertools.cycle(('.',',','o','v','^','<','>','1','2','3','4','8',
                              's','p','P','*','h','H','+','x','X','D','d','|',
                              '_'))
    color = itertools.cycle(('b','g','r','c','m','y','k'))
    for idx, field in enumerate(fieldname):
        ax.scatter(sF[idx], noW[idx], label=field, marker=next(marker), color=next(color), edgecolors='none')
    ax.legend(loc='upper center', ncol=5, bbox_to_anchor=(0.5,-0.2))
    ax.grid(True)
    plt.savefig('analyse_Well_Field.png', bbox_inches='tight',transparent=True,dpi=dpi)
    plt.show()

def cross_plot5(fieldname,fname='model_fit.dat',dpi=600,meth=0):
    Oe  = get_total_resources(field_names)
    a   = np.genfromtxt(fname,delimiter='\t',skip_header=1)
    tau = a[:,1]
    q   = a[:,2]*12 # per year

    a   = np.genfromtxt('model_fit2.dat',delimiter='\t',skip_header=1)
    noW = a[:,4]

    fieldname=np.array(fieldname)
    
 
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.minorticks_on()
    ax.set_ylabel(r'$q$ [$10^6$Sm^3/year]')
    ax.set_xlabel(r'Original Recoverable Oil/Total number of wells [$10^6$Sm^3]')
#    fig.tight_layout()
    fig.subplots_adjust(bottom=0.57, top=1)
    marker = itertools.cycle(('.',',','o','v','^','<','>','1','2','3','4','8',
                              's','p','P','*','h','H','+','x','X','D','d','|',
                              '_')) 
    color = itertools.cycle(('b','g','r','c','m','y','k'))
    for idx, field in enumerate(fieldname):
        y=q[idx]
        ax.scatter(Oe[idx]/noW[idx], y, label=field, marker=next(marker),color=next(color), edgecolors='none')
    plt.title('Norwegian Oil Fields - Comparison Model and Data')
    ax.legend(loc='upper center', ncol=6, bbox_to_anchor=(0.5,-0.2),prop={'size': 7})
    ax.grid(True)
    plt.savefig('analyseqqq_'+str(meth)+'.png', bbox_inches='tight',transparent=True,dpi=dpi)
    plt.show()

def infell_well_cp(field_names,year,df_prod,df_well,fit_name,dpi=200,frac=True,well_pl=False):

    ydata=[]
    Oe  = get_total_resources(field_names)
    for field in field_names:
        abs_oil,frac_oil=well_impact_on_recovery(field,df_prod_,df_well_,fit_name,[year],shut_down=False,well_pl=well_pl)
        if frac:
            ydata.append(frac_oil[0])
        else:
            ydata.append(abs_oil[0])

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.minorticks_on()
    if frac:
        ax.set_ylabel(r'Additional Oil Infell Well  [fraction of total recover]')
    else:
        ax.set_ylabel(r'Additional Oil Infell Well  [$10^6$Sm^3]')

    ax.set_xlabel(r'Original Recoverable Oil Equivalents in Place [$10^6$Sm$^3$]')
#    fig.tight_layout()
    fig.subplots_adjust(bottom=0.57, top=1)
    marker = itertools.cycle(('.',',','o','v','^','<','>','1','2','3','4','8',
                              's','p','P','*','h','H','+','x','X','D','d','|',
                              '_')) 
    color = itertools.cycle(('b','g','r','c','m','y','k'))
    for idx, field in enumerate(field_names):
        ax.scatter(Oe[idx], ydata[idx], label=field, marker=next(marker),color=next(color), edgecolors='none')
    plt.title('Effect of infell well ' + str(year)+ ' years after startup')
    ax.legend(loc='upper center', ncol=6, bbox_to_anchor=(0.5,-0.2),prop={'size': 7})
    ax.grid(True)
    plt.savefig('analys_wel_'+str(year)+'.png', bbox_inches='tight',transparent=True,dpi=dpi)
    plt.show()

def write_head(name, mode):
     with codecs.open(name,mode,'utf-8') as ftex:
          ftex.write('%Generated from plot2.py\n')
          ftex.write('\\begin{figure*}[!tb]\n')
          ftex.write('\\centering\n')
          ftex.close()
def write_end(name,mode):
     with codecs.open(name,mode,'utf-8') as ftex:
          ftex.write('\\end{figure*}\n')
          ftex.close()

def gen_plot2tex(fn2,texnm='../doc/report/field3.tex'):
     write_head(texnm, 'w')
     for idx,fn in enumerate(fn2):
          print(idx,fn)
          with codecs.open(texnm,'a','utf-8') as ftex:
               ftex.write('\\subfigure[]{\\label{'+fn+'}\\includegraphics[width=0.49\\textwidth]{../../PNG/'+fn+'}}')
               ftex.write('\n')
               ftex.close()
          if((idx+1)%6 == 0 and idx >0):
               write_end(texnm,'a')
               write_head(texnm,'a')
     write_end(texnm,'a')       

def write_data_files(field_names,df_prod,df_well):
    for field in field_names:
        new_name = field
        new_name = new_name.replace(" ", "_")
        new_name = new_name.replace("Å", "AA")
        new_name = new_name.replace("Ø", "O")
        Y,Oe,oil,gas = get_production_data(df_prod_,field)
        Yw,Ww=get_well_data(df_well,field)
        X=np.array([Y,oil,gas,Oe])
        Xw=np.array([Yw,Ww])
        fn = pathlib.Path.cwd().parent
        fn = fn / 'data' / 'jarle'
        np.savetxt(fn.joinpath(new_name+'_PROD.txt'),np.transpose(X),header='year\tOil\tGas\tOilEquivalents',delimiter='\t')
        np.savetxt(fn.joinpath(new_name+'_WELL.txt'),np.transpose(Xw),header='year\tProductionWell',delimiter='\t')
        
def well_impact_on_recovery(name,df_prod,df_well,fit_name,Ti,pr=False,shut_down=True,well_pl=False):
    """
    fname : field name
    df_prod : data frame from NPD
    tau : time constant in model,  dimension year
    q : average well production in model, dimension production per month
    well_fact : if well_fact = 2, we double number of wells after half time production
    Must be called directly after find_model_parameters
    """
    global YY_ # Year at which a well was drilled
    global WW_ # Number of wells that year
    global NN_ # tanke model NN_ = 1 exponential model
# --- following code is to test out scenarios ----
# if well_fact = 2, we double number of wells after half time production 

    well_tot_oil=[]
    well_frac_recovery=[]
    YY_,WW_=get_well_data(df_well,name)
    NN_=1
    
    WW0=np.copy(WW_)
    YY0=np.copy(YY_)
    #get fitted values from previous run
    try:
        a=pd.read_csv(fit_name,sep='\t')
        b=a[a['FieldName']==name]
        tau=b['tau_1'].values[0]
        q=b['q_1'].values[0]
    except:    
        result=find_model_params(name,df_prod,df_well) 
        tau=result[0]
        q=result[1]
        print('Data not found, had to make new fit...\n')
    
    Y=np.arange(YY_[0],YY_[-1]+10,1./12)
    O=[]
    Ow=[]
    O.append(modelfunc(Y, tau,q,pr=pr,shut_down=shut_down))
    print('Total number of wells: ', sum(WW_))
    a=[];col=[]
    a.append(Y)
    col.append('Years')
    fig, ax1 = plt.subplots()
    plt.title(name)
    color = itertools.cycle(('b','g','r','c','m','y','k'))
    for idx,ti in enumerate(Ti):
        if ti < 1000: # assume years after startup
            ti += YY_[0]
        WW_=np.copy(WW0)
        YY_=np.copy(YY0)
        if pr:
            print(YY_)
            print(WW_)
        wyy=np.searchsorted(YY_, ti)
        well_exists=False
        if(wyy < len(YY_)):
            if(YY_[wyy]==ti):
                well_exists=True
        if(well_exists):
            print('already a well at time', ti, ' wells ', WW_[wyy])
            WW_[wyy]+=1
        else:
            print('insert new well at time', ti)
            WW_=np.insert(WW_,wyy,1)
            YY_=np.insert(YY_,wyy,ti)
            if pr:
                print(YY_)
        if pr:
            print(WW_)
        print('Total number of wells: ', sum(WW_))
        O.append(modelfunc(Y, tau,q,pr=pr,shut_down=shut_down))
        Ow.append(infill_well(Y, ti,tau,q))
        
    

        ax1.set_ylabel(r'Production rate  [10$^6$Sm$^3$/month]')
        ax1.grid(b=True, which='major', color='k', linestyle='--')
        ax1.minorticks_on()
        ax1.set_xlabel('Years')
        oo=np.array(O[-1])-np.array(O[0])
        cc=next(color)
        if (idx==0):
            ax1.plot(Y,oo,c=cc,label='Net production change')
            ax1.plot(Y,Ow[-1],'--',c=cc,label='Infill well production')
            ax1.plot(Y,oo-Ow[-1],':',c=cc,label='Well interference')
        else:
            ax1.plot(Y,oo,c=cc)
            ax1.plot(Y,Ow[-1],'--',c=cc)
            ax1.plot(Y,oo-Ow[-1],':',c=cc)

        print('Net volume produced value: '+str(name), np.sum(oo), '10^6Sm^3')
        print('Net volume produced value: '+str(name), np.sum(oo)/0.159, '10^6bbl')

        well_tot_oil.append(np.sum(oo))
        well_frac_recovery.append(np.sum(oo)/np.sum(O[0]))

        if well_pl:
            ax2 = ax1.twinx()
            ax2.set_ylabel(r'Number of Wells')
            try:
                ww=np.array(WW_)-np.array(WW0)
                ax2.plot(YY_, ww,'--')
            except:
                print('Could not plot well')
            
        a.append(oo)
        col.append('Infill-Well-Drilled-'+ str(ti)+'1MMSm3/month')
    
    if shut_down:
        fend='_shut_down'
    else:
        fend=''
    ddf=pd.DataFrame(np.transpose(a),columns=col)
    ddf.to_csv(str(name)+fend+'_infell.csv')
    b=[]
    b.append(Y)
    col.insert(1,'No-infell')
    for oi in O:
        b.append(oi)
    ddf=pd.DataFrame(np.transpose(b),columns=col)
    ddf.to_csv(str(name)+fend+'_infell_field.csv')
    plt.legend()
    plt.savefig(name+'.png', bbox_inches='tight',transparent=True)
    plt.show()

    return well_tot_oil,well_frac_recovery
    
    
    
   
    
if __name__ == '__main__':
    with codecs.open('field_conv.txt','r','utf-8') as f:
        field_names = f.readlines()
    field_names = [x.strip() for x in field_names]
    field_names.remove('TROLL')
    field_names.remove('VEGA')
    df_prod_=df_npd()
    df_well_=df_npd(excel_file='wellbore_development_all.xlsx')
    
    dd=get_total_resources(field_names)
#    find_model_params('OSEBERG',df_prod_,df_well_) #MUST BE CALLED BEFORE MODELPLOT
#    plot_model_prod_data('OSEBERG',df_prod_,dpi=1200)
    
#    fit_model(['DRAUGEN'],df_prod_,df_well_,dpi=1200,NO=[1,4,10,100])

#    bad_fit,dd=fit_model(field_names,df_prod_,df_well_,dpi=200,NO=[1],o_g=True)
#    combine_img(dd,no_row=5,no_col=3)

# ############## Run all fields #########################
    
#    fit_scenario=['modw.dat','modw2.dat','modw05.dat']
#    fit_scenario1=['modw_db1.dat','modw_db2.dat','modw_db3.dat']
#    fit_scenario2=['modw_db1_2.dat','modw_db2_2.dat','modw_db3_2.dat']
#    well_fact=[1,2,0.51]
    
#    for idx,ftt in enumerate(fit_scenario1):
#        bad_fit,dd=fit_model(field_names,df_prod_,df_well_,well_fact=well_fact[idx],fit_res_f=fit_scenario1[idx],fit_res_f2=fit_scenario2[idx],show=False)

#    field_names=['OSEBERG','GULLFAKS','SNORRE','EMBLA']
#    field_names=['GAUPE','FRAM H-NORD']
#    field_names=['GULLFAKS']
#    field_names=['YTTERGRYTA','ATLA','BRYNHILD']
#    field_names=['BALDER','TORDIS','STATFJORD ØST', 'OSEBERG ØST', 'NORNE']
#    bad_fit,dd=fit_model(field_names,df_prod_,df_well_,o_g=True)
#    combine_img(dd,no_row=5,no_col=3)
#    gen_plot2tex(dd)
#    write_data_files(field_names,df_prod_,df_well_)
#########################################################
 #   a = np.genfromtxt('model_fit_final.dat',delimiter='\t',skip_header=1)
#    a = a[:,1:]
#    fit_model(['EKOFISK'],df_prod_,df_well_,dpi=200,NO=[1],fit_res_f='tull.dat',fit_res_f2='tull2.dat')
#    cross_plot(field_names)
#    plot_infill_data('GRANE',[2008,2010,2012],df_well_,dt=0.1)
#    plot_infill_data('BALDER',[2007,2009,2012],df_well_,dt=0.1)
#    bad_fit,dd=fit_model(['HEIDRUN'],df_prod_,df_well_,o_g=True)
    well_impact_on_recovery('GRANE',df_prod_,df_well_,'infill_model_fit2.dat',[2007,2009],shut_down=False)
#    well_impact_on_recovery('EKOFISK',df_prod_,df_well_,'infill_model_fit2.dat',[1980],shut_down=True)
    well_impact_on_recovery('BALDER',df_prod_,df_well_,'infill_model_fit2.dat',[2007,2009,2012],shut_down=False)
    well_impact_on_recovery('BALDER',df_prod_,df_well_,'infill_model_fit2.dat',[10,12,15],shut_down=False)

    infell_well_cp(field_names,1,df_prod_,df_well_,'infill_model_fit2.dat',dpi=200,frac=True,well_pl=False)
#    infell_well_cp(['SKIRNE'],1,df_prod_,df_well_,'infill_model_fit2.dat',dpi=200,frac=True,well_pl=False)

#    cross_plot2(field_names)
#    cross_plot(field_names)
#    cross_plot4(field_names)
#    cross_plot5(field_names)

    

#    df_npd_=df_npd(excel_file='npd.xls')

 #   NN_=1
    
 #   i=0
 #   popt=find_model_params(field_names[i],df_prod_,df_well_)
 #   plot_model_prod_data(field_names[i],df_prod_,popt[0],popt[1])
    #yp,o=get_production_data(df_prod_,field_names[i])
    
    #m = modelfunc(yp, popt[0],popt[1])
    #plt.plot(yp,m)
    #plt.plot(yp,o)
    #plt.show()

# %%
