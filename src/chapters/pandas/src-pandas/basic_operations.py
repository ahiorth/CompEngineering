#%%
import pandas as pd
import numpy as np

my_dict={'Field name':5*['Glitne (Equinor energy as)']+5*['Ula (Aker bp asa)'], 
'Year':[2010,2011,2012,2013,2014,1997,1998,1999,2000,2001],
'Yearly emmision to air':[23.007249,33.175011,44.655462,12.728508,3.420579,120.965740,188.130557,173.742075,156.330527,170.557604],
'Unit':10*['1000 tonn']}
df=pd.DataFrame(my_dict)
df.to_excel('co2_emmision.xlsx',index=False)
print(df)
# %%
df = pd.DataFrame({'foo':np.random.random(), 'index':range(10000)})
df_with_index = df.set_index(['index'])
# %%
my_dict1={'Field name':5*['Glitne (Equinor energy as)'], 
'Year':[2010,2011,2012,2013,2014],
'Yearly emmision to air':[23.007249,33.175011,44.655462,12.728508,3.420579],
'Unit':5*['1000 tonn']}
my_dict2={'Field name':5*['Ula (Aker bp asa)'], 
'Year':[1997,1998,1999,2000,2001],
'Yearly emmision to air':[120.965740,188.130557,173.742075,156.330527,170.557604],
'Unit':5*['1000 tonn']}
df1=pd.DataFrame(my_dict1)
df2=pd.DataFrame(my_dict2)

df=pd.concat([df1,df2])

# %%
a=np.random.uniform(0,1,size=1000000)
b=np.random.uniform(0,1,size=100000)
df=pd.DataFrame()
df['a']=a
df['b']=b
%timeit df['a']*df['a']
%timeit a*a
%timeit np.square(df['a'])
%timeit np.square(a) 
# %%
df=pd.DataFrame()
df['a']=[0,1,2,3]
df['b']=[4,5,6,7]
df['c']=['hammer','saw','rock','nail']
# %%
import os
print(os.getcwd())
df=pd.read_excel('../data/file2.xlsx')
df['Field name'] == 'Glitne (Equinor energy as)'
# %%
import numpy as np
import pandas as pd
N=100
a=np.random.uniform(0,1,size=N)
df=pd.DataFrame()
df['a']=a
df['b']=df['a']*df['a']
df['c']=np.sin(df['a'])

# %%
import matplotlib.pyplot as plt
plt.plot(df['a'],df['b'], '*', label='$a^2$')
plt.plot(df['a'],df['c'], '^', label='$\sin(a)$')
plt.legend()
plt.grid()
plt.show()

# %%
df=df.set_index('a')
df.plot()
# %%
df.plot(subplots=True)
df=df.reset_index()
#%%
df.plot.scatter(x='a',y='b',alpha=0.5)
df.plot.scatter(x='a',y='c')

# %%
my_d1={'time':[0,1,2,3],'water':[2,2,2,2]}
my_d2={'time':[0,2,3],'oil':[2,2,2]}
df1=pd.DataFrame(my_d1)
df2=pd.DataFrame(my_d2)
# %%
import datetime as dt
a=dt.datetime.combine(dt.datetime(2020,2,24),dt.time(23,59))
my_dict={'LOCATION':7*['Afghanistan'], 
'TIME':[a+dt.timedelta(days=i) for i in range(7)],
'ELAPSED_TIME_SINCE_OUTBREAK':[0, 1, 2, 3, 4, 5, 6],
'CONFIRMED':[1, 1, 1, 1, 1, 1, 1],
'DEATHS':[0, 0, 0, 0, 0, 0, 0],
'RECOVERED':[0, 0, 0, 0, 0, 0, 0]}
df=pd.DataFrame(my_dict)
# %%
import datetime as dt
import pandas as pd
a=dt.datetime.combine(dt.datetime(2020,2,24),dt.time(23,59))
b=dt.datetime.combine(dt.datetime(2020,2,7),dt.time(23,59))
my_dict={'LOCATION':7*['Afghanistan'] + 6*['Diamond Princess'], 
'TIME':[a+dt.timedelta(days=i) for i in range(7)] +
[b+dt.timedelta(days=i) for i in range(6)],
'ELAPSED_TIME_SINCE_OUTBREAK':[0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5],
'CONFIRMED':7*[1]+[61, 61, 64, 135, 135, 175],
'DEATHS':13*[0],
'RECOVERED': 13*[0]}
df=pd.DataFrame(my_dict)
print(df.describe()) # to view
dfi.export(df,'../fig-pandas/df.png',table_conversion='matplotlib',max_rows=20,max_cols=10)

df=df.groupby('LOCATION').sum()
dfi.export(df,'../fig-pandas/group.png',table_conversion='matplotlib',max_rows=20,max_cols=10)

# %%
df[(df['LOCATION'] == 'Afghanistan') & (df['ELAPSED_TIME_SINCE_OUTBREAK'] > 2)]
# %%
my_dict1={'LOCATION':7*['Afghanistan'], 
'TIME':[a+dt.timedelta(days=i) for i in range(7)],
'ELAPSED_TIME_SINCE_OUTBREAK':[0, 1, 2, 3, 4, 5, 6],
'CONFIRMED':7*[1],
'DEATHS':7*[0],
'RECOVERED': 7*[0]}
my_dict2={'LOCATION':6*['Diamond Princess'], 
'TIME':[b+dt.timedelta(days=i) for i in range(6)],
'ELAPSED_TIME_SINCE_OUTBREAK':[0, 1, 2, 3, 4, 5],
'CONFIRMED':[61, 61, 64, 135, 135, 175],
'DEATHS':6*[0],
'RECOVERED': 6*[0]}
df1=pd.DataFrame(my_dict1)
df2=pd.DataFrame(my_dict2)
df=pd.concat([df1,df2],axis=1)
#dfi.export(df,'../fig-pandas/concat2.png',table_conversion='matplotlib',max_rows=20,max_cols=10)

# %%
pd.concat([df1,df2],axis=1)
# %%
my_dict1={'Field name':4*['Ula (Aker bp asa)'], 
'Year':[1997,1998,1999,2000],
'Yearly emmision to air':[23.007249,33.175011,44.655462,12.728508],
'Unit':4*['1000 tonn']}
my_dict2={'Field name':5*['Ula (Aker bp asa)'], 
'Year':[1997,1998,1999,2000,2001],
'Yearly emmision to air':[120.965740,188.130557,173.742075,156.330527,170.557604],
'Unit':5*['1000 tonn']}
df1=pd.DataFrame(my_dict1)
df2=pd.DataFrame(my_dict2)

#df1.merge(df2,on=['Year','Field name','Unit'],how='outer')
# %%
a=dt.datetime.combine(dt.datetime(2020,2,24),dt.time(23,59))
b=dt.datetime.combine(dt.datetime(2020,2,7),dt.time(23,59))
my_dict={'LOCATION':13*['Afghanistan'], 
'TIME':[a+dt.timedelta(days=i) for i in range(7)] +
[b+dt.timedelta(days=i) for i in range(6)],
'ELAPSED_TIME_SINCE_OUTBREAK':[0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5],
'CONFIRMED':7*[1]+[61, 61, 64, 135, 135, 175],
'DEATHS':13*[0],
'RECOVERED': 13*[0]}
df=pd.DataFrame(my_dict)
print(df) # to view
# %%
import datetime as dt
a=dt.datetime(2020,2,24,23,59)
b=dt.datetime(2020,2,7,23,59)
my_dict={'LOCATION':7*['Afghanistan'] + 6*['Diamond Princess'], 
'TIME':[a+dt.timedelta(days=i) for i in range(7)] +
[b+dt.timedelta(days=i) for i in range(6)],
'ELAPSED_TIME_SINCE_OUTBREAK':[0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5],
'CONFIRMED':7*[1]+[61, 61, 64, 135, 135, 175],
'DEATHS':13*[0],
'RECOVERED': 13*[0]}
df=pd.DataFrame(my_dict)

print(df) # to view
# %%
import pandas as pd
import datetime as dt
a=dt.datetime(2020,2,24,23,59)
b=dt.datetime(2020,2,7,23,59)
my_dict1={'LOCATION':7*['Diamond Princess'], 
'TIME':[b+dt.timedelta(days=i) for i in range(7)],
'ELAPSED_TIME_SINCE_OUTBREAK':[0, 1, 2, 3, 4, 5, 6],
'CONFIRMED':7*[1],
'DEATHS':7*[0],
'RECOVERED': 7*[0]}
my_dict2={'LOCATION':2*['Diamond Princess'], 
'TIME':[b+dt.timedelta(days=i) for i in range(2)],
'ELAPSED_TIME_SINCE_OUTBREAK':[0, 1],
'CONFIRMED':[60, 60],
'DEATHS':2*[0],
'RECOVERED': 2*[0]}
df1=pd.DataFrame(my_dict1)
df2=pd.DataFrame(my_dict2)
df=df1.merge(df2,on=['LOCATION','TIME'],how='outer')
cols=['CONFIRMED','DEATHS', 'RECOVERED']
for col in cols:
    df[col]=df[[col+'_x',col+'_y']].sum(axis=1) # sum row elements
    df=df.drop(columns=[col+'_x',col+'_y']) # remove obsolete columns
# final clean up
df['ELAPSED_TIME_SINCE_OUTBREAK']=df['ELAPSED_TIME_SINCE_OUTBREAK_x']		
df=df.drop(columns=['ELAPSED_TIME_SINCE_OUTBREAK_y','ELAPSED_TIME_SINCE_OUTBREAK_x'])
dfi.export(df,'../fig-pandas/merge3.png',table_conversion='matplotlib',max_rows=20,max_cols=10)
# %%
import dataframe_image as dfi
df=df1.merge(df2,on=['LOCATION','TIME'],how='outer')
dfi.export(df,'../fig-pandas/merge1.png',table_conversion='matplotlib',max_rows=20,max_cols=10)
df=df1.merge(df2,on=['LOCATION','TIME'],how='inner')
dfi.export(df,'../fig-pandas/merge2.png',table_conversion='matplotlib',max_rows=20,max_cols=10)
# %%
