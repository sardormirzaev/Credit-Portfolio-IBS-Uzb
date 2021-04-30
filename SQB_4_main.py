# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 13:34:50 2021

@author: Sardor Mirzaev
"""
import os
from datetime import date
today=str(date.today()) 
##################################################

#os.chdir("d:/SQB_val_prog/Script/") # Choose  the directory
import_1= 'sample_1.xlsx' # Choose  the data 
import_2='helper.xlsx'
export_1= 'export_' +str(today)+'.xlsx' # Choose name to save the file 

##################################################
import pandas as pd
import SQB_4_adds as sqb
import SQB_4_functions as func
corporates=pd.read_csv('corp2.txt',header=None, dtype=str) # Choose from for Corporates
##############################################  l
#%%
## Importing the data
LC_data,FC_data,df=sqb.import_data(import_2,import_1)

#%%
#### Execute the funtions and create a complete dataset
dataset=sqb.add_top_rows(df,pd.concat([sqb.datetrim(df),\
                                       sqb.df_builder(df,LC_data,FC_data,\
                                                      corporates)],axis=1))
#%%
##Export results to excell
func.export_to_excel(dataset,export_1)

#%%

cat=str('region') # target class. value
#new_dd=dataframe
total_cl=new_dd.groupby(by=[cat]).ВсегоЗадолженность.sum()
total_client_FC=new_dd[(new_dd['КодВал']!='000')]
total_cl_FC = total_client_FC.groupby(by=[cat]).ВсегоЗадолженность.sum()
cl=pd.DataFrame()   
unsecured_cl=pd.DataFrame()
FC_cl=pd.DataFrame()
FC_c3l=pd.DataFrame()
FC_c4l=pd.DataFrame()
reserves_cl=pd.DataFrame()
reserves_c3l=pd.DataFrame()
reserves_FC_cl=pd.DataFrame()
reserves_FC_c3l=pd.DataFrame()
for i in range(1,6):
    aaa=new_dd[new_dd['ракам клас']==str(i)]
    if i>=4:
        aa=new_dd[new_dd['ракам клас']==str(i)]
        reserves_cl[i]=aa.groupby(by=[cat]).ОстатокРезерв.sum()  
        stand22=new_dd[(new_dd['КодВал']!='000')&(new_dd['ракам клас']==str(i))]
        reserves_FC_cl[i]=stand22.groupby(by=[cat]).ОстатокРезерв.sum()
        stand3=new_dd[(new_dd['КодВал']!='000')&(new_dd['ракам клас']==str(i))]
        FC_c3l[i]=stand3.groupby(by=[cat]).ВсегоЗадолженность.sum()
    if i>=3:
        aa=new_dd[new_dd['ракам клас']==str(i)]
        reserves_c3l[i]=aa.groupby(by=[cat]).ОстатокРезерв.sum()  
        stand22=new_dd[(new_dd['КодВал']!='000')&(new_dd['ракам клас']==str(i))]
        reserves_FC_c3l[i]=stand22.groupby(by=[cat]).ОстатокРезерв.sum()
        stand3=new_dd[(new_dd['КодВал']!='000')&(new_dd['ракам клас']==str(i))]
        FC_c4l[i]=stand3.groupby(by=[cat]).ВсегоЗадолженность.sum()
    cl[i]=aaa.groupby(by=[cat])\
    .ВсегоЗадолженность.sum()
    stand2=new_dd[(new_dd['ракам клас']==str(i))&(new_dd['КодОбес']=='61')]
    unsecured_cl[i]=stand2.groupby(by=[cat]).ВсегоЗадолженность.sum()
    stand3=new_dd[(new_dd['КодВал']!='000')&(new_dd['ракам клас']==str(i))]
    FC_cl[i]=stand3.groupby(by=[cat]).ВсегоЗадолженность.sum()
#%%
c2l=pd.DataFrame()
unsecured_c2l=pd.DataFrame()
FC_c2l=pd.DataFrame()
reserves_c2l=pd.DataFrame()
reserves_FC_c2l=pd.DataFrame()
for i in range(2, 6):
    stand2=new_dd[new_dd['ракам клас']==str(i)]
    reserves_c2l[i]=stand2.groupby(by=[cat]).ОстатокРезерв.sum()    
    stand22=new_dd[(new_dd['КодВал']!='000')&(new_dd['ракам клас']==str(i))]
    reserves_FC_c2l[i]=stand22.groupby(by=[cat]).ОстатокРезерв.sum()
    
    aaa=new_dd[new_dd['ракам клас']==str(i)]
    c2l[i]=aaa.groupby(by=[cat])\
    .ВсегоЗадолженность.sum()    
    stand2=new_dd[(new_dd['ракам клас']==str(i))&(new_dd['КодОбес']=='61')]
    unsecured_c2l[i]=stand2.groupby(by=[cat]).ВсегоЗадолженность.sum()
    stand3=new_dd[(new_dd['КодВал']!='000')&(new_dd['ракам клас']==str(i))]
    FC_c2l[i]=stand3.groupby(by=[cat]).ВсегоЗадолженность.sum()
    
#%%
cl_joined=pd.concat([c2l,cl],axis=0)    
cl_joined = cl_joined[~cl_joined.index.duplicated(keep='last')]
unsecured_cl_joined=pd.concat([unsecured_c2l,unsecured_cl],axis=0)    
unsecured_cl_joined = unsecured_cl_joined[~unsecured_cl_joined.index.\
                                          duplicated(keep='last')]
reserves_cl_joined=pd.concat([reserves_cl,reserves_c3l,reserves_c2l],axis=0)
reserves_cl_joined=reserves_cl_joined\
[~reserves_cl_joined.index.duplicated(keep='last')]
reserves_FC_cl_joined=pd.concat([reserves_FC_cl,reserves_FC_c3l,reserves_FC_c2l],axis=0)
reserves_FC_cl_joined=reserves_FC_cl_joined\
[~reserves_FC_cl_joined.index.duplicated(keep='last')]
FC_cl_joined=pd.concat([FC_cl,FC_c4l,FC_c3l,FC_c2l],axis=0)
FC_cl_joined= FC_cl_joined[~FC_cl_joined.index.duplicated(keep='first')]
#%%
unt_client=pd.concat([total_cl,total_cl_FC,cl_joined,FC_cl_joined,\
                      reserves_cl_joined,reserves_FC_cl_joined],axis=1,sort=False)   
unt_client=unt_client.div(1000).fillna(0)
unt_client.sum()

#%%
unt_client.columns=[i for i in range(0,len(unt_client.columns))]
unt_client.sum()
unt_client.insert(3,7, unt_client.pop(7))
unt_client.insert(5,8, unt_client.pop(8))
unt_client.insert(6,12, unt_client.pop(12))
unt_client.insert(7,16, unt_client.pop(16))

unt_client.insert(5,8, unt_client.pop(8))
unt_client.insert(9,9, unt_client.pop(9))
unt_client.insert(10,13, unt_client.pop(13))
unt_client.insert(11,17, unt_client.pop(17))
unt_client.insert(13,10, unt_client.pop(10))
unt_client.insert(14,14, unt_client.pop(14))
unt_client.insert(15,18, unt_client.pop(18))
unt_client.insert(11,17, unt_client.pop(17))

#%%
colname2=['Общая сумма',   'из них, в иностранной валюте (в экв. в сумах)',\
          'Стандартные','из них, в иностранной валюте (в экв. в сумах)',\
          'Субстандартные','из них, в иностранной валюте (в экв. в сумах)',\
          'Специальные резервы (мин 10%)',\
          'из них, в иностранной валюте (в экв. в сумах)',\
          'Неудовлетворительные',\
          'из них, в иностранной валюте (в экв. в сумах)', \
          'Специальные резервы (мин 25%)',\
          'из них, в иностранной валюте (в экв. в сумах)',\
          'Сомнительные','из них, в иностранной валюте (в экв. в сумах)',\
          'Специальные резервы (мин 50%)',\
          'из них, в иностранной валюте (в экв. в сумах)',\
          'Безнадежные','из них, в иностранной валюте (в экв. в сумах)',
          'Специальные резервы (мин 100%)',
          'из них, в иностранной валюте (в экв. в сумах)']

unt_client.columns=colname2