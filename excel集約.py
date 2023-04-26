# -*- coding:utf-8 -*-
import pandas as pd
import glob
import os

count =0 
df_all = pd.DataFrame


dir_path = r"C:\Users\arwml\py1\48_excel集約\data\kobe1"
files = glob.glob(dir_path + "\*.xlsx")

for file in files:
    print(file)
    try:
        df=pd.read_excel(file)
    except:
        print("ファイルを読み込めません",file)
        continue

    df = df.fillna('')
    df['filename'] = os.path.basename(file)  #ファイル名を追加
    #print(df)

    if count == 0:
        df_all = df
    else:
        df_all = pd.concat([df_all,df]) 
    count+=1

print(df_all)






