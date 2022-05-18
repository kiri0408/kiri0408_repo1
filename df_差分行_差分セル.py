import pandas as pd



###############################################################################
#2つのdfの差  （df1のみに存在する行。  df2は除外オーダシートの想定）
df1=pd.read_excel('df_test.xlsx',sheet_name='1')
df2=pd.read_excel('df_test.xlsx',sheet_name='2')

df3 = pd.merge(df1,df2,on='c2',how='inner')[['c2']]    # innerで共通する行のキー列を抽出 
df3['flg'] = df3['c2']                                 # マージで 列が消えないようにflg列追加
df1 = pd.merge(df1,df3,on='c2',how='left').fillna('')  # マージ。 共通する行にフラグを立てて fillna 
df1 = df1.drop(df1[df1['flg'] != '' ].index).reset_index(drop=True)  #共通フラグ行をdropし reset_index 

print('差分行：')
print(df1)



##################################################################################
#２つのdfの変更セル （最新：df1  変更前：df2）
df1=pd.read_excel('df_test.xlsx',sheet_name='1')
df2=pd.read_excel('df_test.xlsx',sheet_name='2')

df2['key'] = df2['c2']  # マージでずれないように 結合用のkey列を追加する 
df3=pd.merge(df1,df2,left_on='c2',right_on='key',how='left') #マージ。 横方向につながる。 
df3=df3.fillna('')

print('マージ：')
print(df3)

for i in range(len(df3)):
    for j in range(3):
        if df3.iloc[i,j] != df3.iloc[i,j+3]:
            print(f'異なります  i={i} j={j}')  




