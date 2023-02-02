import pandas as pd
import os 

df = pd.read_excel('df_2.xlsx')

for i in range(len(df)):
    print('削除します',i,df.loc[i,'path'])
    os.remove(df.loc[i,'path'])
