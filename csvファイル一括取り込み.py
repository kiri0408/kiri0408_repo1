import os
import datetime
import glob
import shutil
import pandas as pd
from pathlib import Path
import pathlib

dir_taisho_oya = Path(r"C:\py\55_csvファイル一括取り込み\fol" )  #コピー元の親のフォルダパス

#親のフォルダパス から１階層下のフォルダパスを取得
dir_taisho =[]
for path in dir_taisho_oya.glob("*"):  
    if path.is_dir():
       dir_taisho.append(path) 

df_all = pd.DataFrame()  # 取得データ格納用df

#コピー実行 
for dir in dir_taisho:  
    
    # "fol"で始まるフォルダが対象
    # if dir.name[:3] != 'fol' :   
    # "fol"を含むフォルダが対象
    if   'fol' not in dir.name :   
        continue

    files =  glob.glob( str(dir) +  '\*.csv' )  #csvのファイルパスを取得 
    for file in files:

        # # "1"から始まるファイルが対象
        # p_file = pathlib.Path(file)  
        # if p_file.name[:1] != "1" :
        #     continue

        # "1"を含むファイルが対象
        p_file = pathlib.Path(file)  
        if  "1" not in p_file.name :
            continue

        #csvファイルの取り込み 
        df = pd.read_csv(file)  # 一旦、csv を df へ取り込む  （concatでカラム名を揃えるため）
        df_all = pd.concat([df_all,df])  #concatによりカラム名が揃う。 


df_all = df_all.reset_index(drop=True)      
print(df_all)


