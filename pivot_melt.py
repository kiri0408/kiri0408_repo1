import polars as pl


df         = pl.read_excel('pivot_melt.xlsx',sheet_name='a')
df_keikaku = pl.read_excel('pivot_melt.xlsx',sheet_name='b')

#実績をpivotして合計値の計算
df = df.pivot(index=['BU','年月'],columns='項目',values='実績')
df = df.with_columns(
    (pl.col('仕掛進行基準A') + pl.col('仕掛進行基準B') + pl.col('仕掛進行基準C')).alias('仕掛進行基準')
    ,(pl.col('仕掛進行除くA') + pl.col('仕掛進行除くB') + pl.col('仕掛進行除くC')).alias('仕掛進行除く')
)

#計画とjoinするため、実績を一旦melt
df = df.melt(id_vars=['BU','年月'] 
             ,value_vars=['仕掛進行基準A','仕掛進行基準B','仕掛進行基準C','仕掛進行除くA','仕掛進行除くB','仕掛進行除くC', '仕掛進行基準', '仕掛進行除く']
             ,variable_name='項目'
             ,value_name='実績'
             )

#計画をjoin
df = df.join(df_keikaku,on=['BU','年月','項目'] ,how='left')

#計画差を計算
df = df.with_columns((pl.col('実績') - pl.col('計画')).alias('計画差'))

#計画、実績、計画差をmelt
print(df.columns)
df = df.melt(
    id_vars=['BU','年月','項目']
    ,value_vars=[ '実績', '計画', '計画差']
    ,variable_name='計画実績'
    ,value_name='値'
).with_columns(
    pl.col('値').round(5)
)

df.write_csv('df.tsv',separator='\t')

print(df)



