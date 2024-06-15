"""

"""


import polars as pl

df         = pl.read_excel('pivot_melt.xlsx',sheet_name='a')
df_keikaku = pl.read_excel('pivot_melt.xlsx',sheet_name='b')

#合計値の計算
df = df.pivot(index=['BU','年月'],columns='項目',values='実績')    #pivot
df = df.with_columns(
     (pl.col('仕掛進行基準A') + pl.col('仕掛進行基準B') + pl.col('仕掛進行基準C')).alias('仕掛進行基準')     #合計値の計算
    ,(pl.col('仕掛進行除くA') + pl.col('仕掛進行除くB') + pl.col('仕掛進行除くC')).alias('仕掛進行除く')     #合計値の計算
)

#計画とjoinするため、実績を一旦melt
df = df.melt(id_vars=['BU','年月'] 
             ,value_vars=['仕掛進行基準A','仕掛進行基準B','仕掛進行基準C','仕掛進行除くA','仕掛進行除くB','仕掛進行除くC', '仕掛進行基準', '仕掛進行除く']
             ,variable_name='項目'
             ,value_name='実績'
             )

#計画に対して実績をjoin
df = df_keikaku.join(df,on=['BU','年月','項目'] ,how='left')

#計画差を計算
df = df.with_columns((pl.col('実績') - pl.col('計画')).alias('計画差'))

#ロング型に戻す。   計画、実績、計画差をmelt
print(df.columns)
df = df.melt(
    id_vars=['BU' ,'年月' ,'項目']
    ,value_vars=[ '実績' ,'計画' ,'計画差']
    ,variable_name='計画実績'
    ,value_name='値'
)

#値の調整
df= df.with_columns(
    pl.col('値').round(5)
    ,pl.col('年月').cast(pl.Utf8)
)


# import datetime
# now = datetime.datetime.now()
# print(str(now.year),str(now.month)) 


#対象年度の年月を作成
nend =2024
list_nengetu =[]
list_nengetu.append(str(nend)+'04')
list_nengetu.append(str(nend)+'05')
list_nengetu.append(str(nend)+'06')
list_nengetu.append(str(nend)+'07')
list_nengetu.append(str(nend)+'08')
list_nengetu.append(str(nend)+'09')
list_nengetu.append(str(nend)+'10')
list_nengetu.append(str(nend)+'11')
list_nengetu.append(str(nend)+'12')
list_nengetu.append(str(nend+1)+'01')
list_nengetu.append(str(nend+1)+'02')
list_nengetu.append(str(nend+1)+'03')


#年度末までの年月をNoneで追加する。 
df = df.pivot(index=['BU','項目','計画実績'],columns='年月',values='値')  #一旦 年月でpivotしワイドへ。
for nengetu in list_nengetu:
    if nengetu not in df.columns:
        print(nengetu)
        df = df.with_columns(pl.lit(None).alias(nengetu))   #存在しない年月をNoneで追加
df = df.melt(                                               # melt で ロングに戻す。
    id_vars=['BU','項目','計画実績']
    ,value_vars= list_nengetu
    ,variable_name='年月'
    ,value_name='値'
)

print(df)


df.write_csv('df.tsv',separator='\t')





