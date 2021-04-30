# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 09:35:22 2021

@author: 49151
"""

def cat(x):
    state=['12701','12704', '15101','15104']
    non_bank=['15401']
    non_commerc=['15201']
    intl=['15301','12901','15321','15609']
    private=['12501','12503','12521','14901','14902','14903','14921']
    tov=['15001','15021']
    #farmer =['%.'] 
    for e in private:
        if e==x:
            return "Физические лица"   
    for i in state:
        if i==x:
            return "Государственные предприятия"    
    for w in intl:
        if w ==x:
            return "Совместные и иностранные предприятия"
    for z in tov:
        if z==x:
            return 'Частные товарищества и корпорации' 
    for j in non_bank:
        if j==x:
            return "Небанковские финансовые институты"
    for q in non_commerc:
        if q==x:
            return "Негосударственные некоммерческие организации"         
    return "Частные товарищества и корпорации" 


def cat_by_balance(x):
    state=['20210']
    non_bank=['20216']
    non_commerc=['20212']
    intl=['20214']
    #private=['12501','12503','12521','14901','14902','14903','14921']
    tov=['20218']
    # farmer =['20208'] 
    for i in state:
        if i==x:
            return "Государственные предприятия"    
    for j in non_bank:
        if j==x:
            return "Небанковские финансовые институты"
    for q in non_commerc:
        if q==x:
            return "Негосударственные некоммерческие организации"
    for w in intl:
        if w ==x:
            return "Совместные и иностранные предприятия"
    # for e in farmer:
    #     if e==x:
    #         return "Фермерское хозяйство"        
    for z in tov:
        if z==x:
            return 'Частные товарищества и корпорации'       
    
    return None

def int_float_none(x):
    # it may be already int or float 
    if isinstance(x, (int, float,)):
        return x
    # all int like strings can be converted to float so int tries first 
    try:
        return int(x)
    except (TypeError, ValueError):
        pass
    try:
        return float(x)
    except (TypeError, ValueError):
        return None



#"1 = Manufacturing'
#'2=Agriculture'
#'6= Construction'
#'10= Other'
#'8= Service'
#'7 =Trade'
#'5= Transport and Communication'
#'9=Utilities'
def cat_industr(x):
    if x==1:
        return 'Manufacturing'
    if x==2:
        return 'Agriculture'
    if x==3:
        return 'Transport and Communication'
    if x==4:
        return 'Construction'
    if x==5:
        return 'Trade'
    if x==6:
        return 'Service'
    if x==7:
        return 'Utilities'
    if x==8:
        return 'Other'
       
    
def cat_private(x):
    micro=[25,54,32,58]
    consumer=[30,59]
    mortgage=[24]
    vehicle=[34]
    other= [33]
    
    for i in micro:
        if x==i:
            return ' Micro'
    for i in consumer:
        if x==i:
            return ' Consumer'
    for i in mortgage:
        if x==i:
            return ' Mortgage'
    for i in vehicle:
        if x==i:
            return ' Vehicle'
    for i in other:
        if x==i:
            return ' Other'
        
def cat_corp_sme(x,corps):

    for s in corps:
        if x==s:
            return '1'
#    for i in sme:
#        if x==i:
#            return '2'
    else:
        return '2'


def cat_loan(x,rates):
    for i ,b in rates.iterrows():
        if  b[0] < x < b[1]:
            return b[2]
     
def convert_float_int(x):
    f = float(x)
    i = int(x)
    return i if i == f else f
        
def save_to_excel(df):
    import tkinter as tk
    df=df
    root= tk.Tk()
    canvas1 = tk.Canvas(root, width = 300, height = 300, \
                        bg = 'lightsteelblue2', relief = 'raised')
    canvas1.pack()
    def exportExcel():
        from tkinter import filedialog
        export_file_path =\
        filedialog.asksaveasfilename(defaultextension='.xlsx')
        df.to_excel(export_file_path,startrow = 6, index = False,\
                    header=True, engine='xlsxwriter')
    
    saveAsButtonExcel = \
    tk.Button(text='Save to Excel', command=exportExcel,\
              bg='green', fg='white', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 150, window=saveAsButtonExcel)
    root.mainloop()
    print('Exporting completed')   
    
def export_to_excel(dataset,name):
    import time
    tic=time.time()       
    print("------Exporting  to Excell------")  
    import pandas as pd
    
    export_1=name
    writer = pd.ExcelWriter(export_1, engine='xlsxwriter')
    dataset.to_excel(writer, sheet_name='Sheet1',startrow= 0, header=True, index=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    cellFormat = workbook.add_format({'num_format': '###, ###, ###, ###, ###.00'})
    cellFormat_2 = workbook.add_format({'bold': True, 'font_color': 'black'})
    worksheet.set_column('A:BY', 12)                                  
    worksheet.set_column('H:H', 15, cellFormat)
    worksheet.set_column('R:R', 15, cellFormat)
    worksheet.set_column('J:J', 15, cellFormat)
    worksheet.set_column('S:U', 15, cellFormat)
    worksheet.set_column('W:AA', 15, cellFormat)
    worksheet.set_column('AD:AD', 15, cellFormat)
    worksheet.set_column('AC:AC', 15, cellFormat)
    worksheet.set_column('AW:AX', 25)
    worksheet.set_column('D:D', 25)
    worksheet.set_column('H:H', 25)
    worksheet.set_column('J:J', 25)
    worksheet.set_column('R:R', 25)
    worksheet.set_column('S:S', 25)
    worksheet.set_column('U:U', 25)
    worksheet.set_column('X:X', 25)
    worksheet.set_column('Y:Y', 25)
    worksheet.set_row(5, None, cellFormat_2)
    worksheet.set_column('AN:AN', 25,cellFormat)
    
    #worksheet.set_column('K:L', 17, cellFormat2)
    #worksheet.set_column('T:T', 17, cellFormat2)
    #worksheet.set_column('V:V', 17, cellFormat2)
    #worksheet.set_column('AB:AB', 17, cellFormat2)
    writer.save()
    print("------Loading is completed ------")  
    print("------Exporting  to Excell completed------")  
    toc = time.time()
    print(" Computation is completed...")
    hours, rem = divmod(toc-tic,3600)
    minutes,seconds=divmod(rem,60)
    print("Computation time " +"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))                  
def put_names(x):
    if x=='35':
        return 'Республика Каракалпакстан'
    if x=='03':
        return 'Андижанская область'
    if x=='06':
        return 'Бухарская область'
    if x=='08':
        return 'Джизакская область'
    if x=='10':
        return 'Кашкадарьинская область'
    if x=='12':
        return 'Навоийская область'
    if x=='14':
        return 'Наманганская область'
    if x=='18':
        return 'Самаркандская область'
    if x=='22':
        return 'Сурхандарьинская область'
    if x=='24':
        return 'Сырдарьинская область'
    if x=='27':
        return 'Ташкентская область'
    if x=='30':
        return 'Ферганская область'
    if x=='33':
        return 'Хорезмская область'
    if x=='26':
        return 'г. Ташкент'
    else:
         None

def index_orders(x):
    x=['Республика Каракалпакстан','Андижанская область','Бухарская область',\
       'Джизакская область','Кашкадарьинская область','Навоийская область',\
       'Наманганская область','Самаркандская область','Сурхандарьинская область',\
       'Сырдарьинская область','Ташкентская область','Ферганская область',\
       'Хорезмская область','г. Ташкент']
    return x

def add_zeros(df):
    import numpy as np
    import pandas as pd
    zeros = np.where(np.empty_like(df.values), 0, 0)
    data = np.hstack([df.values, zeros]).reshape(-1, df.shape[1])
    df_ordered = pd.DataFrame(data, columns=df.columns)
    return df_ordered

def main():
    cat()
    cat_industr()
    int_float_none()
    add_zeros()
    cat_private()
    cat_loan()
    cat_corp_sme()
    convert_float_int()
    save_to_excel()
if __name__=="__main__":
    main()
print("Completed.")