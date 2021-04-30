# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:43:53 2021

@author: 49151
"""
def df_builder(dataframe,LC_data,FC_data,corporates):
    import time
    import SQB_4_functions as func
    import numpy as np
    import pandas as pd 
    from datetime import datetime
    tic = time.time()
    df=dataframe
    df2=df.iloc[5:,:]
    df2.columns=df2.iloc[0,:] # rename the columns 
    df2=df2.iloc[1:,:]
    obs_date=datetime.strptime(df.iloc[3,0].strip('за '), '%d.%m.%Y')
    #obs_date=obs_date.strftime("%Y-%m-%d")
    df2['MFO_schet']=df2["МФО"].astype(str) + df2["Кредитный счет"].astype(str)
    
    df2['тип']= df2['БалансСчет'].apply(lambda x: func.cat(x)) 
       
    df2["КодВал2"] =np.where(df2["КодВал"]=='000', '000','840').astype(str)
    df2['Уникал']=df2['Кредитный счет'].str[9:17]
    df2['МФО+уникал']= df2['МФО']+df2['Уникал']
    df2['КлассКачества1']=df2['КлассКачества'].str[0]
    df2['NPL']=np.where((df2['КлассКачества1']=="3") | (df2['КлассКачества1']=="4")\
       | ( df2['КлассКачества1']=="5") ,1 ,0)
     
    df2['otr']=df2['СекторКлиентаДляОтчетов'].str[0].astype(int)
    df2['Отрасль_eng']=df2['otr'].apply(lambda x: func.cat_industr(x))
    
    df2['Баланс2']=df2['БалансСчет'].str[0:3]+'00' 
    df2['ОстатокСудеб2']=df2['ОстатокСудеб'].astype(str).apply(lambda x: x.strip())
    df2['Баланс х/р']=np.where(df2['ОстатокСудеб2']!='nan','15700',df2['Баланс2'])
    df2['ОстатокРезерв2']=df2['ОстатокРезерв'].astype(str).apply(lambda x: x.strip())
    df2['ВсегоЗадолженность2']=df2['ВсегоЗадолженность'].astype(str).apply(lambda x: x.strip())
    df2['Резерв%2']=(df2['ОстатокРезерв']/df2['ВсегоЗадолженность'])    
    df2['Резерв%2']=df2['Резерв%2'].astype(float).map(lambda x: '{:.2%}'.format(x))
    
    df2['Резерв%']=np.where((df2['Резерв%2']=='nan%'),0,df2['Резерв%2'])
    
    #%%
    #df2['тип2']=np.where(df2['тип']=="Физические лица",1,0)
    dz=df2[df2['тип']=="Физические лица"]
    d1=df2[df2['тип']!="Физические лица"]
    #%%
    d11 = d1[(d1.БалансСчет!= "15001")]
    d11=d11[(d11.БалансСчет != "15021")]
    d11['zzz']=d11['НаименКлиента'].str.startswith(('ДХ','Dx','DX','ФЕРМЕР','F/X','F.X','F.x','FX','FERMER','fermer','фермер','ФХ','Ф/Х','Ф.Х','Ф.х','Ф/Х','Ф.Х','ф/х','ф.х','fx','f/x'))
    d11['zzz2']=d11['НаименКлиента'].str.endswith(('FERMER XO`JALIGI','JALIGI','xo`jaligi','jaligi','ДХ','Dx','DX','F/X','F.X','F.x','FX','ХЕЗЯЙСТВА','ФЕРМЕР ХУЖАЛИГИ','фермер хужалиги','ФХ','Ф/Х','Ф.Х','Ф.х','ДХ','Ф/Х','Ф.Х','Ф.х','ф/х','ф.х','fx','f/x'))
    
    d11['zzq']=d11['НаименКлиента'].str.contains('jaligi|ФЕРМЕР|ХЕЗЯЙСТВА|ФЕРМЕР ХУЖАЛИГИ|фермер хужалиги|Ф/Х|Ф.Х|Ф.х|Ф/Х|Ф.Х| Ф.х|ф/х|ф.х|FERMER XO`JALIGI|JALIGI|xo`jaligi|jaligi|ФЕРМЕР|ХЕЗЯЙСТВА|МЕР|МЕР ХУЖАЛИГИ|фермер хужалиги|Ф/Х|Ф.Х|Ф.х|ф/х| ф.х',na=False)  
    
    d11['result'] = np.where((d11['zzz']==True)|(d11['zzz2']==True)|(d11['zzq']==True),"Фермерское хозяйство",'nan')
        
    #%%


    d11['z3']=d1['НаименКлиента'].str.contains('КХ|ХК|QK|КК|qo`shma korxonasi|o`shma korhona|СП|кушма корхона|кушма корхонаси|совместное|савмес|Совместное|rijiy', na=False)
    
    d11['z33']=d1['НаименКлиента'].str.startswith(('ХК.','КХ','ХК','QK','КК','СП','Совместное','Horijiy'))
    d11['z333']=d1['НаименКлиента'].str.endswith(('qo`shma korxonasi','qo`shma korhona','СП','кушма корхона','ХК','ХК.','Xorijiy Korxona','Xorijiy Korxonasi','кушма корхонаси','QOSHMA KORXONASI'))
     
    d11['тип клиента_3'] = np.where((d11['z3']==True)|(d11['z33']==True)|(d11['z333']==True),"Совместные и иностранные предприятия",'nan')
    d11['ress1']=np.where(d11['result']=="Фермерское хозяйство"
,d11['result'],np.where(d11['тип клиента_3']=="Совместные и иностранные предприятия",d11['тип клиента_3'],'nan'))
    d1['result2'] =d11['ress1']

#%%
    d1['qa2']=d1['НаименКлиента'].str.contains('mulkdorlari|мулкдорлари|мулкдорларининг|МУЛКДОРЛАРИ|MULKDORLARI|ХУЖМШ|XUJMSH|mulkdorlarining|xujmsh|хужмш|ТСЖ|ТЧСЖ', na=False)
    
    d1['qa22']=d1['НаименКлиента'].str.startswith(('ХУЖМШ','XUJMSH','xujmsh','хужмш','ТСЖ','ТЧСЖ','ТСЧЖ'))
    
    d1['qa222']=d1['НаименКлиента'].str.endswith(('ХУЖМШ','XUJMSH','xujmsh','хужмш','ТСЖ','ТЧСЖ','ТСЧЖ'))
       
    d1['result1'] = np.where((d1['qa2']==True)|(d1['qa22']==True)|(d1['qa222']==True), "Негосударственные некоммерческие организации",'nan')
    
    d1['тип клиента_2'] = np.where(d1['result1']!= "Негосударственные некоммерческие организации",d1['result2']," Негосударственные некоммерческие организации")
    
    d1['comb']=np.where(d1['тип клиента_2']!='nan',d1['тип клиента_2'],d1['тип'])
    
    df2['тип клиента1']= d1['comb'].combine_first(dz['тип'])

    #%%
    #first choose private person, then fill 3          
    
    dz['val_0']=np.where(dz['тип']=="Физические лица",3,None)
    dz['val_1']=dz['ВидКредитования'].str[0:2].astype(int)
    df2['val_1']=df2['ВидКредитования'].str[0:2].astype(int)
    df2['val_11']=dz['val_1']
    #df2['val_111']=np.where(df2['val_11']=='nan',df2['val_11'],df2['val_1'])
    
    dz['hip']=dz['val_1'].apply(lambda x: func.cat_private(x))
    #df2['hip']=df2['val_11'].apply(lambda x: func.cat_private(x))
    df2['Уникал2']=dz['val_0']
    
    df2['hip']=dz['hip']
    crp=corporates.iloc[:,0]
    d1['po_Уникал1']=d1['Уникал'].apply(lambda x: func.cat_corp_sme(x,crp))
    
    df2['po_Уникал1']=d1['po_Уникал1']
    df2['po_Уникал']=df2['po_Уникал1'].apply(lambda x: 3 if type(x)!=str else x)
    
    
    df2['p_7']=np.where(df2['po_Уникал']=="2","SME",              np.where(df2['po_Уникал']=='1','Corporate','nan'))
    df2['p_8']=np.where(df2['hip']!=None,df2['hip'],df2['p_7'])
    df2['7та мижоз тури']= df2['p_8'].combine_first(df2['p_7'])
    df2['3та мижоз тури']= df2['po_Уникал']    
    #%%
      # Дни просрочки основного долга
    df2['ДатаОбразПр']=pd.to_datetime(df2['ДатаОбразПрос'])-obs_date
    prosrochka = abs(df2['ДатаОбразПр'])/np.timedelta64(1, 'D')
    df2['Прос куни'] = prosrochka.fillna(0)  
    # Дни просрочки процентной задолженности
    #pros_procen = pd.to_datetime(df2['ДатаОбразПросПроц'])
    pros_procen = abs(pd.to_datetime(df2['ДатаОбразПросПроц'])-obs_date)/np.timedelta64(1, 'D')
    pros_procen = pros_procen.fillna(0)
    df2['ФОИЗ КУНИ']=pros_procen
    # Получение кода обеспечения
    df2['КодОбес'] = df2['Обеспечение'].str[:2]
    
    # Класс кредита
    df2['ракам клас'] = df2['КлассКачества'].str[:1]
    
    df2['Классификация'] = df2['КлассКачества'].astype(str).str[2:]
    
    df2['Отрасль'] = df2['СекторКлиентаДляОтчетов'].str[0]
    df2['ОКЭД'] = df2['ОКЭД клиента'].str[:5]
  #%%
    
    df2['ДатаДоговор']=df2['ДатаДоговора']
    df2['ДатаДоговора'] = pd.to_datetime(df2['ДатаДоговора']).dt.date.apply(lambda x: x.strftime('%d.%m.%Y'))
    df2['ДатаПогаш'] = pd.to_datetime(df2['ДатаПогаш']).dt.date.apply(lambda x: x.strftime('%d.%m.%Y'))
    df2['ДатаОбраз1'] = pd.to_datetime(df2['ДатаОбразПрос']).dt.date.fillna(0)
    df2['ДатаОбразПрос']=df2['ДатаОбраз1'].apply(lambda x: 'nan' if x==0 else x.strftime('%d.%m.%Y'))
    
    df2['ДатаОбразПрос1'] = pd.to_datetime(df2['ДатаОбразПросПроц']).dt.date.fillna(0)
    
    df2['ДатаОбразПросПроц']=df2['ДатаОбразПрос1'].apply(lambda x: 'nan' if x==0 else x.strftime('%d.%m.%Y')) 
    
    #%%
    df2['Maximum']=np.maximum(df2['Прос куни'],df2['ФОИЗ КУНИ'])  
    df2['PAR0']=df2['Maximum'].apply(lambda x: 1 if x>0 else 0)
    df2['PAR30']=df2['Maximum'].apply(lambda x: 1 if x>30 else 0)
    df2['PAR60']=df2['Maximum'].apply(lambda x: 1 if x>60 else 0)
    df2['PAR90']=df2['Maximum'].apply(lambda x: 1 if x>90 else 0)
    df2['PAR120']=df2['Maximum'].apply(lambda x: 1 if x>120 else 0)
    df2['PAR150']=df2['Maximum'].apply(lambda x: 1 if x>150 else 0)
    df2['PAR180']=df2['Maximum'].apply(lambda x: 1 if x>180 else 0)
      
    #%%
    
    ### finding preferential loans on LC and FC
    ##LC
    import_rates=LC_data
    rates=import_rates.iloc[2:,2:]
    rates.columns=import_rates.loc[1,2:4]
    rates=rates.fillna(datetime.now().strftime('%d.%m.%Y'))
    rates['Duration from']=pd.to_datetime(rates['Duration from'])
    rates['Duration end']=pd.to_datetime(rates['Duration end'])
    df2['ДатаД']= pd.to_datetime(df2['ДатаДоговор'])
    df2['rates']= df2['ДатаД'].apply(lambda x:func.cat_loan(x,rates)) 
    
    #%%
    #Separate the LC loans  from FC loans    
    ## On LC
    ratesdf=df2[df2['КодВал']=='000']
    ratesdf['delta']=(ratesdf['% кредита']-ratesdf['rates']).astype(float)
    ratesdf['preferential']= ratesdf.delta.apply(lambda x: 1 if x<=0 else 0)
    
    df2['Loan_type1']=ratesdf['preferential']
    #%%
    #On FC
    df3=FC_data
    FC_loan=df3.iloc[5:,:]
    FC_loan.columns=df3.loc[5,:]
    FC_loan=FC_loan.iloc[1:,:]
    FC_df=df2[df2['КодВал']!='000']
    
    FC_loan['za']=FC_loan.МФИ.str.startswith(('КТЭК','АБР','МБР','МБР','МАР','ЕБР' ), na=False)
    
    FC_loan['zaz']=np.where(FC_loan['МФИ']=='КТЭКС10','nan',FC_loan['za'])
    
    fc_hip=FC_loan[FC_loan['zaz']=='True']
    zz=[]
    for  i in fc_hip['Кредитный счет']:
        for d,z in FC_df['Кредитный счет'].iteritems():
            if z==i:
                zz.append(d)
    
    FC_df['for index']=FC_df.index           
    FC_df['compare']=FC_df['for index'].apply(lambda x: 1 if x in zz else 0)
    df2['Loan_type2']=FC_df['compare']
    df2['Льготный %']=df2['Loan_type2'].combine_first(df2['Loan_type1'])
    df2['compare']=df2['balance'].apply(lambda x: func.cat_by_balance(x))
    df2['тип клиента']=df2['compare'].combine_first(df2['тип клиента1'])
    #%%
    df3=df2[['MFO_schet','тип клиента','КодВал2','Прос куни','ФОИЗ КУНИ','Резерв%' ,'КодОбес','ОКЭД','Отрасль','ракам клас','Классификация','Баланс х/р','Уникал',
             'МФО+уникал', 'NPL','Maximum','PAR0','PAR30','PAR60','PAR90',
             'PAR120','PAR150', 'PAR180','Отрасль_eng','3та мижоз тури',\
             '7та мижоз тури','Льготный %']]
    dfz=pd.DataFrame(index=df3.index[0:5],columns=df3.columns)
    dfz=dfz.reset_index(drop=True)
    daf=pd.concat([dfz,df3],axis=0)
    print("------Computation is completed ------")  
    toc = time.time()
    hours, rem = divmod(toc-tic,3600)
    minutes,seconds=divmod(rem,60)
    print("Computation time " +"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))   
    return daf

def datetrim(df):
    import SQB_4_functions as func
    import pandas as pd
    dfs=df.iloc[5:,:]
    dfs.columns=df.loc[5,:]
    dfs=dfs.iloc[1:,:]
    dfs['ДатаДоговора'] = pd.to_datetime(dfs['ДатаДоговора']).dt.date.apply\
    (lambda x: x.strftime('%d.%m.%Y'))
    dfs['ДатаПогаш'] = pd.to_datetime(dfs['ДатаПогаш']).dt.date.apply\
    (lambda x: x.strftime('%d.%m.%Y'))
    dfs['ДатаОбраз1'] = pd.to_datetime(dfs['ДатаОбразПрос']).dt.date.fillna(0)
    dfs['ДатаОбразПрос']=dfs['ДатаОбраз1'].apply(lambda x: 'nan' if x==0 else\
       x.strftime('%d.%m.%Y'))
    dfs['ДатаОбразПрос1'] = pd.to_datetime(dfs['ДатаОбразПросПроц']).dt.date.\
    fillna(0)
    dfs['ДатаОбразПросПроц']=dfs['ДатаОбразПрос1'].apply(lambda x: 'nan' if x==0\
       else x.strftime('%d.%m.%Y'))
    
    
    #'СуммаДог(сум.экв)',
    for c in dfs[['СуммаДог(ном)',\
                  'ОстатокКредСчета','ОстатокПересм','ОстатокПроср',\
                  'ОстатокСудеб','ВсегоЗадолженность','ОстатокРезерв',\
                  'ОстатокНачПроц','ОстатокНачПросПроц',\
                  'Остаток пени','ОценкаОбеспечения','ОстатокВнебПроцентов']]:
        dfs[c] = dfs[c].apply(lambda x :func.int_float_none(x))
    
#        dfs[c] = dfs[c].apply(lambda x : '{0:,}'.format(x)) 
#        #dfs[c] = dfs[c].apply(lambda x : func.convert_float_int(x))
        #dfs[c] = dfs[c].apply(lambda x : x.replace(',', " "))
        #dfs[c] = dfs[c].apply(lambda x : x.replace('.', ","))
        #dfs[c] = dfs[c].fillna(0)
        
        
    
    return dfs.iloc[:,:-5]

def add_top_rows(df,dfs):
    import SQB_4_functions as func
    import time
    tic=time.time()
    dfs.NN[0:4]=df.iloc[0:4,0]
    dfs.ОстатокКредСчета.loc[2]=func.int_float_none(dfs['ОстатокКредСчета'][5:].sum())
    dfs['СуммаДог(ном)'][2]=func.int_float_none(dfs['СуммаДог(ном)'][5:].sum())
    #dfs['СуммаДог(сум.экв)'][2]=func.int_float_none(dfs['СуммаДог(сум.экв)'][5:].sum())
    dfs.ОстатокПересм.loc[2]=func.int_float_none(dfs['ОстатокПересм'][5:].sum())
    dfs.ОстатокПроср.loc[2]=func.int_float_none(dfs['ОстатокПроср'][5:].sum())
    dfs.ОстатокСудеб.loc[2]=func.int_float_none(dfs['ОстатокСудеб'][5:].sum())
    dfs.ВсегоЗадолженность.loc[2]=func.int_float_none(dfs['ВсегоЗадолженность'][5:].sum())
    dfs.ОстатокРезерв.loc[2]=func.int_float_none(dfs['ОстатокРезерв'][5:].sum())
    dfs.ОстатокВнебПроцентов.loc[2]=func.int_float_none(dfs['ОстатокВнебПроцентов'][5:].sum())
    dfs.iloc[4,:]=dfs.columns
    dfs.columns=range(0,len(dfs.columns))
    dfs=dfs.replace('nan',0)
    dfs.columns=dfs.columns=[None for i in dfs.columns]
    print("------Computation is completed ------")  
    toc = time.time()
    hours, rem = divmod(toc-tic,3600)
    minutes,seconds=divmod(rem,60)
    print("Computation time " +"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))  
    return dfs

def import_data(data_on_key_interest,dataframe):
    import pandas as pd 
    import time 
    tic=time.time()
    LC_data=pd.read_excel(data_on_key_interest,'stavka', header=None)
    print("------Importing the data------")  
    FC_data=pd.read_excel(data_on_key_interest,'valuta', header=None)  
    df=pd.read_excel(dataframe,header=None) 
    print("------Importing is completed ------")  
    toc = time.time()
    hours, rem = divmod(toc-tic,3600)
    minutes,seconds=divmod(rem,60)
    print("Computation time " +"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)) 
    return LC_data,FC_data,df

if __name__=="__main__":
    df_builder()
    datetrim()
    add_top_rows()
print("Completed.")
   
    
    
    
    
    
    
    