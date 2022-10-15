# coding: utf-8

import pyodbc
import pandas as pd
import datetime

DB = {'servername': "RTX3070TI\TEST1" ,   'database': 'master'}

# DB検索 
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + DB['servername'] + ';DATABASE=' + DB['database'] + ';Trusted_Connection=yes')
sql = 'select * from table1 '
df_daisu = pd.read_sql(sql, conn)
conn.close()
# print(df_daisu.dtypes)

#DB検索結果のソート 
df_daisu = df_daisu.sort_values(['keycode', 'kotei_cd','keikaku_bi'])
df_daisu = df_daisu.reset_index(drop=True ) 
#print(df_daisu)  

data_all = []
keycode_mae =''
kotei_cd_mae=''
suryo_sum = 0

for i in range(len( df_daisu )):

    #先頭行は オーダ・工程内のsuryo_sum をリセット
    if df_daisu.loc[i,'keycode'] != keycode_mae or df_daisu.loc[i,'kotei_cd']  != kotei_cd_mae :  
        keycode_mae =  df_daisu.loc[i,'keycode'] 
        kotei_cd_mae =  df_daisu.loc[i,'kotei_cd']
        suryo_sum = 0 

    #台数を号機に分解し、SQL作成する 
    for j in range(df_daisu.loc[i,'suryo'] ):
        #sql1 = df_daisu.loc[i,'keycode'] + '  '  + df_daisu.loc[i,'kotei_cd']  + '  '  + str(df_daisu.loc[i,'keikaku_bi'] )  + '  ' +  str( suryo_sum + 1  + j   )
        data = (  df_daisu.loc[i,'keycode'] , df_daisu.loc[i,'kotei_cd'] , str(df_daisu.loc[i,'keikaku_bi']) ,   str(suryo_sum + 1  + j)  )
        data_all.append(data)
        

    #オーダ・工程内のsuryo_sum を加算
    suryo_sum += df_daisu.loc[i,'suryo']   
            

for i in range(len(data_all)):
    print(data_all[i])

# DB検索 
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + DB['servername'] + ';DATABASE=' + DB['database'] + ';Trusted_Connection=yes')

# カーソルを定義
cursor = conn.cursor()

print('一旦クリア')
cursor.execute("delete  from table2 where keycode in ( select keycode from table1 ) ")  #一旦クリア

print('インサート') 
for i in range(len(data_all)):
    print(data_all[i])
    cursor.execute("INSERT INTO table2(keycode, kotei_cd, keikaku_bi, goki ) VALUES (?, ?, ?,?);", data_all[i])

print('コミット') 
cursor.commit()

cursor.close()
conn.close()

