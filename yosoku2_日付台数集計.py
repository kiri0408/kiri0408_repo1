import polars as pl
from datetime import datetime, timedelta
import calendar

df_data = pl.read_excel('a.xlsx',sheet_name='Sheet2')

print(df_data)


df_data = df_data.with_columns( pl.col("日付").str.to_datetime("%m-%d-%y").alias("date") )
df_data = df_data.with_columns( pl.col("date").dt.strftime("%Y%m").alias("年月") )
df_data = df_data.select(pl.col('年月'),pl.col('台数'))
df_data = df_data.group_by('年月').sum()
print(df_data)


ls_month =[]

start_date = datetime(2014, 5, 10)
ls_month.append(start_date)
for i in range(120):
    # 現在の年と月を取得
    current_year = start_date.year
    current_month = start_date.month
    
    # 現在の月の日数を取得
    days_in_month = calendar.monthrange(current_year, current_month)[1]
    
    # 終了日を計算
    end_date = start_date + timedelta(days=days_in_month)
   
    ls_month.append(end_date)
    # 開始日を更新（次の月へ）
    start_date = end_date

df_month = pl.DataFrame(ls_month)


df_month = df_month.with_columns(pl.col('column_0').dt.strftime('%Y%m').alias("年月"))
df_month = df_month.select(pl.col('年月'))
print(df_month)

df_data2 = df_month.join(df_data,on='年月',how='left')
df_data2 = df_data2.fill_null(0)
print(df_data2)