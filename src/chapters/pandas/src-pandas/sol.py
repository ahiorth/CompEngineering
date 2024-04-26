#%%
import os
print(os.getcwd())

import pandas as pd
df=pd.read_csv('../data/field_production_monthly.csv',sep=',')

def read_data_frame(file_name):
    try:
        df=pd.read_csv(file_name,sep=',')
        return df
    except:
        print('Could not open file: ', file_name)
        return pd.DataFrame() 

df_snorre=df[df['prfInformationCarrier']=='SNORRE']
x=df_snorre['prfYear']+df_snorre['prfMonth']/12
y=df_snorre['prfPrdOeNetMillSm3']
import matplotlib.pyplot as plt
plt.plot(x,y)
df_snorre['time']=x
df_snorre.plot(x='time',y='prfPrdOeNetMillSm3')
#%%
df_snorre_year=df_snorre.groupby('prfYear').sum()
df_snorre_year['prfYear']=df_snorre_year.index
df_snorre_year.plot(x='prfYear',y='prfPrdOeNetMillSm3')
# or a barplot
df_snorre_year.plot.bar(x='prfYear',y='prfPrdOeNetMillSm3')
# %%
df_full=pd.read_csv('../data/field_production_monthly.csv',sep=',')

def get_field_data_frame(field_name,df=df_full):
    '''
    Returns a dataframe given a field name, 
    returns empty dataframe if field does not exist 
    '''
    FIELD_NAME=field_name.upper()
    all_fields=df['prfInformationCarrier'].unique()
    if FIELD_NAME in all_fields:
        return df[df['prfInformationCarrier']==FIELD_NAME]
    else:
        print('Field name ', field_name, ' does not exists')
        print('Available field names are: ')
        print(all_fields)
        return pd.DataFrame()
df=get_field_data_frame('snore') # Wrong name
df=get_field_data_frame('snorRe')

def plot_field_prod_data(df,y='prfPrdOeNetMillSm3'):
    name=df['prfInformationCarrier'].iloc[0] 
    df['time']=df['prfYear']+df['prfMonth']/12
    df.plot(x='time',y=y,title=name,grid=True,xlabel='Years',ylabel=r'Production per month [mill Sm$^3$]')

plot_field_prod_data(df)

#df=get_field_data_frame('snore')


# %%
