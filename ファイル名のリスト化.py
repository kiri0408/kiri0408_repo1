import glob
import pandas as pd
from pathlib import Path
import datetime

#指定フォルダから ファイル名の一覧を取得 
path = r"C:\py\56_ファイル名リスト化\fol\*.txt"
list2 = glob.glob(path)

files=[]
for file in list2:
    filename = Path(file).name  #ファイル名の取り出し
    str1 = filename.split('_')  #ファイル名を分割  a
    files.append(str1)          #リスト化

df = pd.DataFrame(files, columns=('a','b','c','d','e'))
df['count']=''

for i in range(len(df)):
    try:
        df.loc[i,'date'] = datetime.datetime.strptime( df.loc[i,'b'] , '%Y-%m-%d')
        df.loc[i,'month'] = df.loc[i,'date'].strftime('%Y%m')
    except:
        False

#df2 = df[['a','month','count']].groupby(['a','month'], as_index=False).count()
df2 = pd.pivot_table(df,index='a',columns='month',values='count',aggfunc='count')
#pd.pivot_table(df, index=’日付’, columns=’商品名’,values=’販売数量’,aggfunc=’sum’)
print(df)
print(df2)
