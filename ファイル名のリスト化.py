import glob
import pandas as pd
from pathlib import Path

#指定フォルダから ファイル名の一覧を取得 
path = r"C:\py\56_ファイル名リスト化\fol\*.txt"
list2 = glob.glob(path)

files=[]
for file in list2:
    filename = Path(file).name  #ファイル名の取り出し
    str1 = filename.split('_')  #ファイル名を分割
    files.append(str1)          #リスト化

df = pd.DataFrame(files, columns=('a','b','c','d','e'))
print(df)